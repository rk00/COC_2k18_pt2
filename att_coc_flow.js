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

                                scanBlock(base.add(0x154214 + 1))
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

function scanBlock(p) {
    var nSize = 0;
    var jump = 0;
    var checkJump = false;
    while(true) {
        var inst = Instruction.parse(p.add(nSize));
        nSize += inst.size;
        var g = inst.groups;

        if (inst.mnemonic === 'adr') {
            var adrAddr = inst.address;
            console.log('-> fucking adr -> ' + adrAddr.sub(base));
            Interceptor.attach(adrAddr.add(1), function () {
                console.log('-> inside adr. attaching +0x8 at ' + adrAddr.add(0xa).sub(base));
                Interceptor.detachAll();
                Interceptor.flush();
                this.context.pc = adrAddr.add(0xa);
                scanBlock(this.context.pc.add(1));
            });
            break;
        }

        if (g.indexOf('jump') >= 0) {
            jump += 1;
            var op = inst.opStr.substring(1);
            var n = ptr(op);

            console.log('attaching -> ' + n + " (" + n.sub(base) + ")");

            if (n.sub(base) !== 0x15433e) {
                n = n.add(1);
            }

            Interceptor.attach(n, function () {
                console.log("");
                console.log("jump into -> " + this.context.pc + " (" + this.context.pc.sub(base) + ")");
                console.log(JSON.stringify(this.context));
                console.log("");
                Interceptor.detachAll();
                Interceptor.flush();
                scanBlock(this.context.pc.add(1));
            });
        }
        if (checkJump) {
            if (jump === 2) {
                // print conditional jump the shit way. too lazy to parse inst
                console.log('>>> ' + inst.mnemonic + " " + inst.opStr);
            }
            break;
        }
        if (jump === 1) {
            checkJump = true;
        }
        console.log('>>> ' + inst.mnemonic + " " + inst.opStr);
    }
}