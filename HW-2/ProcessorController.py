def bit(x, len):
    return format(x, '0%db'%len)

width_reg = 32
width_mem = 32

# TODO MEM最小存储单元位宽需要再考虑（PC+=4）
class InstSetProcessotController:
    def __init__(self):
        self.REG = ['0'*width_reg]*32
        self.MEM = ['0'*width_mem]*1024
        self.PC = 0
        self.IR = 0
        self.A = 0
        self.B = 0
        self.r = 0
        self.wb = 0

    def Ifetch(self):
        self.IR = self.MEM[self.PC]
        self.PC += 4

    # TODO 还需要补全：通过funct3判断具体指令
    def opFetch_DCD(self):
        print('\nInstruction Code:', self.IR)
        # beq
        if self.IR[-7:]=='1100011':
            # B类型指令立即数为13位 https://www.zhihu.com/answer/3377319225
            imm = self.IR[-32] + self.IR[-8] + self.IR[-31:-25] + self.IR[-12:-8] + '0'
            rs1 = self.IR[-20:-15]
            rs2 = self.IR[-25:-20]
            self.A = int(self.REG[int(rs1, 2)], 2)
            self.B = int(self.REG[int(rs2, 2)], 2)
            self.BEQ(int(imm, 2))
            print('beq', '\n\timm value:', int(imm, 2), '\n\trs1 value:', int(self.REG[int(rs1, 2)], 2), 
                  '\n\trs2 value:', int(self.REG[int(rs2, 2)], 2), '\n\tPC:', self.PC)

        # jal
        elif self.IR[-7:]=='1101111':
            imm = self.IR[-32] + self.IR[-20:-12] + self.IR[-21] + self.IR[-31:-21]
            rd = self.IR[-12:-7]
            self.JAL(int(rd, 2), int(imm, 2))
            print('jal', '\n\timm value:', int(imm, 2), '\n\trd value:', int(self.REG[int(rd, 2)], 2), '\n\tPC:', self.PC)
        
        # add
        elif self.IR[-7:]=='0110011':
            rd = self.IR[-12:-7]
            rs1 = self.IR[-20:-15]
            rs2 = self.IR[-25:-20]
            self.A = int(self.REG[int(rs1, 2)], 2)
            self.B = int(self.REG[int(rs2, 2)], 2)
            self.ADD()
            self.R2WB()
            self.WB(int(rd, 2))
            print('add', '\n\trd value:', int(self.REG[int(rd, 2)], 2), '\n\trs1 value:', int(self.REG[int(rs1, 2)], 2), 
                  '\n\trs2 value:', int(self.REG[int(rs2, 2)], 2), '\n\tPC:', self.PC)

        # addi
        elif self.IR[-7:]=='0010011':
            rd = self.IR[-12:-7]
            rs1 = self.IR[-20:-15]
            imm = self.IR[-32:-20]
            self.A = int(self.REG[int(rs1, 2)], 2)
            self.ADDI(int(imm, 2))
            self.R2WB()
            self.WB(int(rd, 2))
            print('addi', '\n\trd value:', int(self.REG[int(rd, 2)], 2), '\n\trs1 value:', int(self.REG[int(rs1, 2)], 2), 
                  '\n\timm value:', int(imm, 2), '\n\tPC:', self.PC)

        # lb
        elif self.IR[-7:]=='0000011':
            rd = self.IR[-12:-7]
            rs1 = self.IR[-20:-15]
            imm = self.IR[-32:-20]
            self.A = int(self.REG[int(rs1, 2)], 2)
            self.ADDI(int(imm, 2))
            self.MEM2WB('b')
            self.WB(int(rd, 2))
            print('lb', '\n\trd binary value:', self.REG[int(rd, 2)], '\n\trs1 value:', int(self.REG[int(rs1, 2)], 2), 
                  '\n\timm value:', int(imm, 2), '\n\tmem[%d] binary value:'%(int(self.REG[int(rs1, 2)], 2)+int(imm, 2)), self.MEM[self.r], 
                  '\n\tPC:', self.PC)


        else:
            print('Unsuportted Instruction!')
            exit()

    def BEQ(self, imm):
        if self.A==self.B:
            # 指令手册里的PC+=imm是指当前指令的PC加imm，还是已经计算了PC+4之后再加imm？
            # 按照数据通路，应该是后者
            self.PC += imm
    
    def JAL(self, rd, imm):
        # TODO JAL指令手册里的rd=PC+4是指当前指令的PC加4（下一指令的地址），还是已经计算了PC+4之后再加4？
        # TODO 理应返回下一指令的地址，所以这里认为是前者。
        self.REG[rd] = bit(self.PC, width_reg)
        # self.REG[rd] = self.PC + 4
        self.PC += imm

    def ADD(self):
        self.r = self.A + self.B

    def ADDI(self, imm):
        self.r = self.A + imm

    def R2WB(self):
        self.wb = self.r

    def MEM2WB(self, width):
        if width=='b':
            self.wb = int(self.MEM[self.r][-8:], 2)

    def WB(self, rd):
        self.REG[rd] = bit(self.wb, width_reg)

    def run(self):
        # ======== initail ======== #
        self.PC = 100
        self.REG[2] = bit(5, width_reg)
        self.REG[3] = bit(5, width_reg)

        self.MEM[9] = '1'*32

        # 0000000 00011 00010 000 10000 1100011
        # beq    PC+=8 if REG[1]==REG[2]          ->      PC = 112
        self.MEM[100] = '00000000001100010000010001100011'

        # 00000000100000000000 00001 1101111
        # jal   rd=PC+4, PC+=4                    ->      PC = 120
        self.MEM[112] = '00000000100000000000000011101111'

        # 0000000 00011 00010 000 00001 0110011
        # add   rd = rs1 + rs2                    ->      PC = 124
        self.MEM[120] = '00000000001100010000000010110011'

        # 000000000001 00010 000 00001 0010011
        # addi  rd = rs1 + 1                      ->      PC = 128
        self.MEM[124] = '00000000000100010000000010010011'

        # 000000000100 00010 000 00001 0000011
        # lb    rd = MEM[rs1+4][0:7]
        self.MEM[128] = '00000000010000010000000010000011'

        while True:
            self.Ifetch()
            self.opFetch_DCD()


if __name__ == "__main__":
    ISPC = InstSetProcessotController()
    ISPC.run()
