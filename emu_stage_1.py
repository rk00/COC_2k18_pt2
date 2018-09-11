import emu_base

from unicorn.arm_const import *


PC = 0xd3d27214
SP = 0xceb7e448
R0 = 0xd3d27214
R1 = 0x0
R2 = 0x2
R3 = 0x0
R4 = 0x0
R5 = 0x20
R6 = 0xd354ee94
R7 = 0xceb7e8d8
R8 = 0x20
R9 = 0xd354ee74
R10 = 0x0
R11 = 0x60
R12 = 0xceb7e8d8
LR = 0xf30b8673


mu = emu_base.get_emu('stage1')

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

emu_base.run(mu, PC | 1, (emu_base.BASE + 0x002C06D8) | 1)
