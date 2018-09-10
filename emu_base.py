import binascii
import os
import shutil

from capstone import *
from hexdump import hexdump
from unicorn import *
from unicorn.arm_const import *


BASE = 0xc5f63000
MALLOC_MEM = 0x100000

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
mu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)

VFP = "4ff4700001ee500fbff36f8f4ff08043e8ee103a"


EMU_LOGS_PATH = 'emu_logs'


if os.path.exists(EMU_LOGS_PATH):
    shutil.rmtree(EMU_LOGS_PATH)
os.mkdir(EMU_LOGS_PATH)


trace = False
trace_dbg = []


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
    b_addr = address - BASE
    trace_dbg.append(hex(b_addr))
    if len(trace_dbg) > 10:
        trace_dbg.pop(0)

    if b_addr == 0x000443EC or b_addr == 0x000445D8:
        impl_memcpy()
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    elif b_addr == 0x00044434 or b_addr == 0x000444E8:
        impl_memclr()
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    elif b_addr == 0x000445C0:
        impl_malloc()
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    elif b_addr == 0x00045214:
        impl_gnu_ldivmod_helper()
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    elif b_addr == 0x000444A0:
        impl_memclr()
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    if not trace:
        return
    for i in md.disasm(bytes(uc.mem_read(address, size)), address):
        log("0x%x:\t%s\t%s" % (b_addr, i.mnemonic, i.op_str))


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


def impl_gnu_ldivmod_helper():
    mu.reg_write(UC_ARM_REG_R0, int(mu.reg_read(UC_ARM_REG_R0) / mu.reg_read(UC_ARM_REG_R2)))
    mu.reg_write(UC_ARM_REG_R2, mu.reg_read(UC_ARM_REG_R0) % mu.reg_read(UC_ARM_REG_R2))


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


def get_emu(stage):
    # Enable VFP instr
    mu.mem_map(0x1000, 1024)
    mu.mem_write(0x1000, binascii.unhexlify(VFP))
    mu.emu_start(0x1000 | 1, 0x1000 + len(VFP))
    mu.mem_unmap(0x1000, 1024)

    mu.mem_map(MALLOC_MEM, 1024 * 32)

    files = os.listdir(stage)
    for f in files:
        with open(stage + '/' + f, 'rb') as ff:
            mu.mem_map(int(f, 16), os.path.getsize(stage + '/' + f))
            mu.mem_write(int(f, 16), ff.read())

    mu.hook_add(UC_HOOK_CODE, hook_code)
    mu.hook_add(UC_HOOK_MEM_WRITE | UC_HOOK_MEM_READ, hook_mem_access)

    return mu


def run(mu, start, end):
    print('starting emulation')
    try:
        mu.emu_start(start, end)
    except Exception as e:
        print(e)
        print(trace_dbg)
