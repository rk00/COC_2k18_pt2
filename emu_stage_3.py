import emu_base

from unicorn.arm_const import *


PC = 0xc61c62a4
SP = 0xc0afd338
R0 = 0xc0afd478
R1 = 0xc0afd3f8
R2 = 0xc0afd3f8
R3 = 0x0
R4 = 0xc0afd3f8
R5 = 0x0
R6 = 0xc0afd5f8
R7 = 0xc0afece0
R8 = 0x0
R9 = 0xc0afd4f8
R10 = 0x0
R11 = 0xc0afd674
R12 = 0x0
LR = 0xc5fbd52b


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
