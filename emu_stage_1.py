import emu_base

from unicorn.arm_const import *


PC = 0xd3cae214
SP = 0xceefe448
R0 = 0xd3cae214
R1 = 0x0
R2 = 0x2
R3 = 0x0
R4 = 0x0
R5 = 0x20
R6 = 0xe4d1db14
R7 = 0xceefe8d8
R8 = 0x20
R9 = 0xe4d1daf4
R10 = 0x0
R11 = 0x5c
R12 = 0xceefe8d8
LR = 0xf30b8673


mu = emu_base.get_emu()

mu.reg_write(UC_ARM_REG_R0, R0)
mu.reg_write(UC_ARM_REG_R1, R1)
mu.reg_write(UC_ARM_REG_R2, R2)
mu.reg_write(UC_ARM_REG_R3, R3)
mu.reg_write(UC_ARM_REG_R4, R4)
mu.reg_write(UC_ARM_REG_R5, R5)
mu.reg_write(UC_ARM_REG_R6, R6)
mu.reg_write(UC_ARM_REG_R7, R7)
mu.reg_write(UC_ARM_REG_R8, R8)
mu.reg_write(UC_ARM_REG_R9, R9)
mu.reg_write(UC_ARM_REG_R10, R10)
mu.reg_write(UC_ARM_REG_R11, R11)
mu.reg_write(UC_ARM_REG_R12, R12)
mu.reg_write(UC_ARM_REG_SP, SP)
mu.reg_write(UC_ARM_REG_PC, PC)
mu.reg_write(UC_ARM_REG_LR, LR)

print('starting emulation')
try:
    mu.emu_start(PC | 1, (emu_base.BASE + 0x2C06D8) | 1)
except Exception as e:
    print(e)
