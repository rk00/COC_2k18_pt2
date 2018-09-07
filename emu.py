import binascii
import os
import shutil

from capstone import *
from hexdump import hexdump
from unicorn import *
from unicorn.arm_const import *

BASE = 0xd3bd5000
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
mu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)

VFP = "4ff4700001ee500fbff36f8f4ff08043e8ee103a"

memcpy = [0x00208924, 0x00263382]
memclr = [0x00208944, 0x00208950, 0x00208958, 0x002632C6]

EMU_LOGS_PATH = 'emu_logs'


if os.path.exists(EMU_LOGS_PATH):
    shutil.rmtree(EMU_LOGS_PATH)
os.mkdir(EMU_LOGS_PATH)


def log(what):
    logs_count = len(os.listdir(EMU_LOGS_PATH))
    if logs_count > 0:
        logs_count -= 1
    l_s = 0
    if os.path.exists(EMU_LOGS_PATH + '/log_' + str(logs_count)):
        l_s = os.path.getsize(EMU_LOGS_PATH + '/log_' + str(logs_count))
    if l_s > 1000000:
        logs_count += 1
    l_f = EMU_LOGS_PATH + '/log_' + str(logs_count)
    with open(l_f, 'a+') as f:
        f.write(what)


def hook_code(uc, address, size, user_data):
    for i in md.disasm(bytes(uc.mem_read(address, size)), address):
        b_addr = i.address - BASE
        log("0x%x:\t%s\t%s" % (b_addr, i.mnemonic, i.op_str))
        if b_addr == 0x00154366:
            uc.reg_write(UC_ARM_REG_R0, 0x42000000)
        if b_addr in memcpy:
            impl_memcpy()


def impl_memcpy():
    dest = mu.reg_read(UC_ARM_REG_R0)
    src = mu.reg_read(UC_ARM_REG_R1)
    l = mu.reg_read(UC_ARM_REG_R2)
    data = mu.mem_read(src, l)
    log('memcpy dest 0x%x - src 0x%x - len %d' % (dest, src, l))
    log(hexdump(data, result='return'))
    mu.mem_write(dest, bytes(data))


def print_regs(uc):
    print("r0 " + hex(uc.reg_read(UC_ARM_REG_R0)))
    print("r1 " + hex(uc.reg_read(UC_ARM_REG_R1)))
    print("r2 " + hex(uc.reg_read(UC_ARM_REG_R2)))
    print("r3 " + hex(uc.reg_read(UC_ARM_REG_R3)))
    print("r4 " + hex(uc.reg_read(UC_ARM_REG_R4)))
    print("r5 " + hex(uc.reg_read(UC_ARM_REG_R5)))
    print("r6 " + hex(uc.reg_read(UC_ARM_REG_R6)))
    print("r7 " + hex(uc.reg_read(UC_ARM_REG_R7)))
    print("r8 " + hex(uc.reg_read(UC_ARM_REG_R8)))
    print("r9 " + hex(uc.reg_read(UC_ARM_REG_R9)))
    print("r10 " + hex(uc.reg_read(UC_ARM_REG_R10)))
    print("r11 " + hex(uc.reg_read(UC_ARM_REG_R11)))
    print("r12 " + hex(uc.reg_read(UC_ARM_REG_R12)))
    print("sp " + hex(uc.reg_read(UC_ARM_REG_SP)))
    print("pc " + hex(uc.reg_read(UC_ARM_REG_PC)))
    print("lr " + hex(uc.reg_read(UC_ARM_REG_LR)))


def print_send(uc):
    hexdump(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)))


def hook_mem_access(uc, access, address, size, value, user_data):
    if access == UC_MEM_WRITE:
        log(">>> Memory is being WRITE at 0x%x, data size = %u, data value = 0x%x"
            % (address, size, value))
    else:
        log(">>> Memory is being READ at 0x%x, data size = %u, data value = 0x%s"
            % (address, size, binascii.hexlify(uc.mem_read(address, size)).decode('utf8')))


def dafuckingpatches():
    NOP = binascii.unhexlify('00bf')
    mu.mem_write(BASE + 0x00154366, NOP * 2)

    # stack check
    mu.mem_write(BASE + 0x001543D0, NOP * 5)
    mu.mem_write(BASE + 0x002632BC, NOP * 3)
    mu.mem_write(BASE + 0x00263396, NOP * 5)

    # memcpy
    for addr in memcpy:
        mu.mem_write(BASE + addr, NOP * 2)

    # memclr
    for addr in memclr:
        mu.mem_write(BASE + addr, NOP * 2)


def fuck_it():
    # Enable VFP instr
    mu.mem_map(0x1000, 1024)
    mu.mem_write(0x1000, binascii.unhexlify(VFP))
    mu.emu_start(0x1000 | 1, 0x1000 + len(VFP))
    mu.mem_unmap(0x1000, 1024)

    files = os.listdir('dumps')
    for f in files:
        with open('dumps/' + f, 'rb') as ff:
            mu.mem_map(int(f, 16), os.path.getsize('dumps/' + f))
            mu.mem_write(int(f, 16), ff.read())

    with open('libg.so', 'rb') as f:
        mu.mem_map(BASE, (1024 * 1024 * 8) + (1024 * (256 + 28)))
        mu.mem_write(BASE, f.read())

    mu.reg_write(UC_ARM_REG_R0, 0xd3d29214)
    mu.reg_write(UC_ARM_REG_R1, 0x0)
    mu.reg_write(UC_ARM_REG_R2, 0x2)
    mu.reg_write(UC_ARM_REG_R3, 0x0)
    mu.reg_write(UC_ARM_REG_R4, 0x0)
    mu.reg_write(UC_ARM_REG_R5, 0x20)
    mu.reg_write(UC_ARM_REG_R6, 0xec058014)
    mu.reg_write(UC_ARM_REG_R7, 0xce67e8d8)
    mu.reg_write(UC_ARM_REG_R8, 0x20)
    mu.reg_write(UC_ARM_REG_R9, 0xec057ff4)
    mu.reg_write(UC_ARM_REG_R10, 0x0)
    mu.reg_write(UC_ARM_REG_R11, 0x5e)
    mu.reg_write(UC_ARM_REG_R12, 0xce67e8d8)
    mu.reg_write(UC_ARM_REG_SP, 0xce67e448)
    mu.reg_write(UC_ARM_REG_PC, 0xd3d29214)
    mu.reg_write(UC_ARM_REG_LR, 0xf30b8673)

    dafuckingpatches()

    mu.hook_add(UC_HOOK_CODE, hook_code)
    mu.hook_add(UC_HOOK_MEM_WRITE | UC_HOOK_MEM_READ, hook_mem_access)

    print('starting emulation')
    mu.emu_start(0xd3d29214 | 1, 0xd36c7ff4)


fuck_it()
