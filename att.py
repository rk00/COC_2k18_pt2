import shutil

import frida
import os
import sys

from hexdump import hexdump

current_kang_path = ''


def on_message(message, data):
    global current_kang_path

    if 'payload' in message:
        what = message['payload']
    else:
        print(message)
        return

    if what.startswith('stage'):
        if os.path.exists(what):
            shutil.rmtree(what)
        os.mkdir(what)
        current_kang_path = what
    elif what.startswith('memcpy') or what.startswith('memmov'):
        parts = what.split('::')
        if not os.path.exists(parts[0]):
            os.mkdir(parts[0])

        with open(parts[0] + '/' + str(len(os.listdir(parts[0]))), 'w+') as f:
            hh = hexdump(data, result='return')
            f.write('dst: %s - src: %s\n\n%s' % (parts[1], parts[2], hh))
    elif what != '':
        with open(current_kang_path + '/' + message['payload'], 'wb') as f:
            f.write(data)


def run_cmd(cmd):
    os.system(cmd)


def cleanup_logs(path):
    if os.path.exists(path):
        shutil.rmtree(path)


cleanup_logs('memcpy')
cleanup_logs('memmove')

package_name = "com.supercell.clashofclans"

print("[*] Killing " + package_name)
run_cmd("adb shell am force-stop " + package_name)
print("[*] Starting " + package_name)

pid = frida.get_usb_device().spawn([package_name])
process = frida.get_usb_device().attach(pid)
print("[*] Frida attached.")
script = process.create_script(open('att_coc.js', "r").read())
print("[*] Script loaded.")
script.on('message', on_message)
frida.get_usb_device().resume(package_name)
script.load()
sys.stdin.read()