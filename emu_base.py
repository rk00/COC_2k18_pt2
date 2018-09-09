import binascii
import os
import shutil

from capstone import *
from hexdump import hexdump
from unicorn import *
from unicorn.arm_const import *


BASE = 0xd3b5a000
MALLOC_MEM = 0x100000

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
mu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)

VFP = "4ff4700001ee500fbff36f8f4ff08043e8ee103a"

memcpy = [0x00208924, 0x00263382, 0x00246E5E, 0x00246E8E, 0x00267568, 0x001CB000,
          0x000AECAA, 0x0035A030, 0x0015264A, 0x0005D828, 0x002EC6E8, 0x002EC76C,
          0x00152674, 0x002C07EC]
memclr = [0x00208944, 0x00208950, 0x00208958, 0x002632C6, 0x0022D862, 0x001CAFF4,
          0x00359EF8, 0x00359FEE, 0x002EC586, 0x002EC590, 0x002EC60E, 0x002C07E2]
malloc = [0x0048E4A6]
memmove = [0x002C0732, 0x002C0740]

EMU_LOGS_PATH = 'emu_logs'


if os.path.exists(EMU_LOGS_PATH):
    shutil.rmtree(EMU_LOGS_PATH)
os.mkdir(EMU_LOGS_PATH)


trace = True


def log(what):
    logs_count = len(os.listdir(EMU_LOGS_PATH))
    if logs_count > 0:
        logs_count -= 1
    l_s = 0
    if os.path.exists(EMU_LOGS_PATH + '/log_' + str(logs_count)):
        l_s = os.path.getsize(EMU_LOGS_PATH + '/log_' + str(logs_count))
    if l_s > 2000000:
        logs_count += 1
    l_f = EMU_LOGS_PATH + '/log_' + str(logs_count)
    with open(l_f, 'a+') as f:
        f.write(what + '\n')


def hook_code(uc, address, size, user_data):
    global trace
    for i in md.disasm(bytes(uc.mem_read(address, size)), address):
        b_addr = i.address - BASE
        if trace:
            log("0x%x:\t%s\t%s" % (b_addr, i.mnemonic, i.op_str))
        if b_addr == 0x00154366:
            uc.reg_write(UC_ARM_REG_R0, 0x42000000)
        elif b_addr in malloc:
            impl_malloc()
        elif b_addr in memcpy:
            impl_memcpy()
        elif b_addr in memmove:
            impl_memcpy()
        elif b_addr in memclr:
            #impl_memclr()
            pass
        elif b_addr == 0x0005BA4A:
            uc.reg_write(UC_ARM_REG_R0, 0x2)
        elif b_addr == 0x0048E520 or b_addr == 0x002C084A:
            uc.reg_write(UC_ARM_REG_R0, 0x0)
        elif b_addr == 0x002A5EFC:
            uc.reg_write(UC_ARM_REG_R0, uc.reg_read(UC_ARM_REG_R0) % uc.reg_read(UC_ARM_REG_R1))


def impl_memcpy():
    dest = mu.reg_read(UC_ARM_REG_R0)
    src = mu.reg_read(UC_ARM_REG_R1)
    l = mu.reg_read(UC_ARM_REG_R2)
    data = mu.mem_read(src, l)
    log('memcpy dest 0x%x - src 0x%x - len %d' % (dest, src, l))
    log(hexdump(data, result='return'))
    mu.mem_write(dest, bytes(data))


def impl_malloc():
    global MALLOC_MEM
    size = mu.reg_read(UC_ARM_REG_R0)
    log('allocating %d at 0x%x' % (size, MALLOC_MEM))
    mu.reg_write(UC_ARM_REG_R0, MALLOC_MEM)
    MALLOC_MEM += size


def impl_memclr():
    mu.mem_write(mu.reg_read(UC_ARM_REG_R0),
                 binascii.unhexlify('00' * mu.reg_read(UC_ARM_REG_R1)))


def print_regs(uc):
    log("r0 " + hex(uc.reg_read(UC_ARM_REG_R0)))
    log("r1 " + hex(uc.reg_read(UC_ARM_REG_R1)))
    log("r2 " + hex(uc.reg_read(UC_ARM_REG_R2)))
    log("r3 " + hex(uc.reg_read(UC_ARM_REG_R3)))
    log("r4 " + hex(uc.reg_read(UC_ARM_REG_R4)))
    log("r5 " + hex(uc.reg_read(UC_ARM_REG_R5)))
    log("r6 " + hex(uc.reg_read(UC_ARM_REG_R6)))
    log("r7 " + hex(uc.reg_read(UC_ARM_REG_R7)))
    log("r8 " + hex(uc.reg_read(UC_ARM_REG_R8)))
    log("r9 " + hex(uc.reg_read(UC_ARM_REG_R9)))
    log("r10 " + hex(uc.reg_read(UC_ARM_REG_R10)))
    log("r11 " + hex(uc.reg_read(UC_ARM_REG_R11)))
    log("r12 " + hex(uc.reg_read(UC_ARM_REG_R12)))
    log("sp " + hex(uc.reg_read(UC_ARM_REG_SP)))
    log("pc " + hex(uc.reg_read(UC_ARM_REG_PC)))
    log("lr " + hex(uc.reg_read(UC_ARM_REG_LR)))


def hook_mem_access(uc, access, address, size, value, user_data):
    if trace:
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
    mu.mem_write(BASE + 0x00246E52, NOP)
    mu.mem_write(BASE + 0x00246E56, NOP * 2)
    mu.mem_write(BASE + 0x00246E96, NOP * 5)
    mu.mem_write(BASE + 0x0026755E, NOP * 3)
    mu.mem_write(BASE + 0x002676E2, NOP * 5)
    mu.mem_write(BASE + 0x00208DBE, NOP * 5)

    # memcpy
    for addr in memcpy:
        mu.mem_write(BASE + addr, NOP * 2)

    # memclr
    for addr in memclr:
        mu.mem_write(BASE + addr, NOP * 2)

    # malloc
    for addr in malloc:
        mu.mem_write(BASE + addr, NOP * 2)

    # memmov
    for addr in memmove:
        mu.mem_write(BASE + addr, NOP * 2)

    # jfree
    mu.mem_write(BASE + 0x0048E520, NOP * 2)

    # ldivmod
    mu.mem_write(BASE + 0x0005BA4A, NOP * 2)
    mu.mem_write(BASE + 0x002A5EFC, NOP * 2)


def get_emu():
    # Enable VFP instr
    mu.mem_map(0x1000, 1024)
    mu.mem_write(0x1000, binascii.unhexlify(VFP))
    mu.emu_start(0x1000 | 1, 0x1000 + len(VFP))
    mu.mem_unmap(0x1000, 1024)

    mu.mem_map(MALLOC_MEM, 1024 * 32)

    files = os.listdir('dumps')
    for f in files:
        with open('dumps/' + f, 'rb') as ff:
            mu.mem_map(int(f, 16), os.path.getsize('dumps/' + f))
            mu.mem_write(int(f, 16), ff.read())

    dafuckingpatches()

    mu.hook_add(UC_HOOK_CODE, hook_code)
    mu.hook_add(UC_HOOK_MEM_WRITE | UC_HOOK_MEM_READ, hook_mem_access)

    return mu