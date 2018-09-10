import emu_base

from unicorn.arm_const import *


PC = 0xd400b782
SP = 0xce8fe700
R0 = 0xd400b068
R1 = 0xd400b068
R2 = 0xfb4656b2
R3 = 0xd4549be0
R4 = 0xcf77da50
R5 = 0x0
R6 = 0xb4cba6b0
R7 = 0xce8feeb0
R8 = 0xcf928040
R9 = 0xd3564600
R10 = 0x0
R11 = 0xce8ff7cc
R12 = 0x0
LR = 0xd41596eb


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

emu_base.run(mu, PC | 1, (emu_base.BASE + 0x002A5E50) | 1)
