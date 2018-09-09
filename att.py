import shutil

import frida
import os
import sys


current_kang_path = ''


def on_message(message, data):
    global current_kang_path

    what = ''
    if 'payload' in message:
        what = message['payload']
    if what.startswith('stage'):
        if os.path.exists(what):
            shutil.rmtree(what)
        os.mkdir(what)
        current_kang_path = what
    elif what != '':
        with open(current_kang_path + '/' + message['payload'], 'wb') as f:
            f.write(data)


def run_cmd(cmd):
    os.system(cmd)


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