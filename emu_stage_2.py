import emu_base

from unicorn.arm_const import *


PC = 0xd3cfe782
SP = 0xcea7e700
R0 = 0xd3cfe068
R1 = 0xd3cfe068
R2 = 0xfb4656b2
R3 = 0xd423cbe0
R4 = 0xec016020
R5 = 0x0
R6 = 0xb4cba6b0
R7 = 0xcea7eeb0
R8 = 0xcfa2e6c0
R9 = 0xd35f8780
R10 = 0x0
R11 = 0xcea7f7cc
R12 = 0x0
LR = 0xd3e4c6eb


mu = emu_base.get_emu('stage2')

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
    mu.emu_start(PC | 1, (emu_base.BASE + 0x2A5E50) | 1)
except Exception as e:
    print(e)
