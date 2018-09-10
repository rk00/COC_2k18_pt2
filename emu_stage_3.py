import emu_base

from unicorn.arm_const import *


PC = 0xd3d25608
SP = 0xceb7eeb8
R0 = 0xe7fcf400
R1 = 0x180
R2 = 0xd2aed4a0
R3 = 0x190
R4 = 0x180
R5 = 0xd354ee54
R6 = 0x190
R7 = 0xceb7f618
R8 = 0xd2aed480
R9 = 0xe7fcf580
R10 = 0xe7fcf400
R11 = 0x1b0
R12 = 0xf312dd58
LR = 0xd3e937dd


mu = emu_base.get_emu('stage3')

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
