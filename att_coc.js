var base;

setTimeout(function() {
    inject();
}, 500);

function inject() {
    base = Process.findModuleByName('libg.so').base;
    console.log("base -> " + base);
    attachSVC();
}

/**
 * sendto/recvfrom svc are outside arxan crc cycle :P
 * safely attachable
 */
function attachSVC() {
    var waitingHello = true;
    var nonce, key = null;

    // sendto
    Interceptor.attach(base.add(0x00478E7C), function () {
        console.log('send');
        console.log(Memory.readByteArray(this.context.r1, parseInt(this.context.r2)));

        if (waitingHello) {
            waitingHello = false;
            Interceptor.attach(Module.findExportByName('libc.so', 'open'), function () {
                var what = Memory.readUtf8String(this.context.r0);
                if (what.indexOf('urandom') >= 0) {
                    var readWhat;
                    var readLen;
                    var rInt = Interceptor.attach(Module.findExportByName('libc.so', 'read'), {
                        onEnter: function () {
                            readWhat = this.context.r1;
                            readLen = parseInt(this.context.r2);
                        },
                        onLeave: function () {
                            if (readLen < 32) {
                                nonce = Memory.readByteArray(readWhat, readLen);
                                console.log('nonce');
                                console.log(nonce);
                                rInt.detach();
                            } else if (readLen === 32) {
                                key = Memory.readByteArray(readWhat, parseInt(readLen));
                                console.log('key');
                                console.log(key);
                                Interceptor.detachAll();

                                Interceptor.attach(base.add(0x154214 + 1), function () {
                                    Interceptor.detachAll();

                                    kang('stage1', this.context);

                                    Interceptor.attach(base.add(0x2C06D8 + 1), function () {
                                        Interceptor.detachAll();

                                        kang('stage2', this.context);

                                        Interceptor.attach(base.add(0x478E7C), function () {
                                            Interceptor.detachAll();

                                            console.log('login');
                                            console.log(Memory.readByteArray(this.context.r1, parseInt(this.context.r2)));
                                        });
                                    });
                                });
                            }
                        }
                    });
                }
            });
        }
    });

    // recvfrom
    var buf;
    Interceptor.attach(base.add(0x00478E34), {
        onEnter: function () {
            buf = this.context.r1;
        },
        onLeave: function (ret) {
            console.log('recvfrom');
            console.log(Memory.readByteArray(buf, parseInt(ret)));
        }
    })
}

function kang(stage, context) {
    send(stage);

    var tdp = {};
    for (var reg in context) {
        try {
            var range = Process.findRangeByAddress(context[reg]);
            if (range !== null) {
                if (typeof range["file"] !== 'undefined') {
                    continue;
                }
                if (typeof tdp[range['base']] !== 'undefined') {
                    continue;
                }

                tdp[range['base']] = range;
            }
        } catch (e) {
            continue;
        }
    }

    var sp = Process.findRangeByAddress(context.sp);
    var spbase = ptr(sp['base']);
    for (var i=0;i<sp['size'];i+=4) {
        try {
            var pp = Memory.readPointer(spbase.add(i));
            if (parseInt(pp) === 0) {
                continue;
            }
            var p = Process.findRangeByAddress(pp);
            if (p !== null) {
                if (typeof p["file"] !== 'undefined') {
                    var f = p['file'];
                    if (f["path"].indexOf("system") >= 0 ||
                        f["path"].indexOf("libg") >= 0 ||
                        f["path"].indexOf("ashmem") >= 0) {
                        continue;
                    }
                }
                if (typeof tdp[p['base']] !== 'undefined') {
                    continue;
                }
                tdp[p['base']] = p;
            }
        } catch (e) {
            continue;
        }
    }

    for (reg in context) {
        console.log(reg.toUpperCase() + " = " + context[reg]);
    }

    for (var r in tdp) {
        var range = tdp[r];
        Memory.protect(ptr(range['base']), range['size'], 'rwx');
        send(range['base'],
            Memory.readByteArray(range['base'], range['size']));
    }

    var libg = Process.findModuleByName('libg.so');
    send(libg.base,
        Memory.readByteArray(libg.base, libg.size));
}