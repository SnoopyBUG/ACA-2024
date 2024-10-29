import numpy as np
import random

class CPU:
    '''
    Construct a Pyhton 3 program to simulate a virtual machine having
    1)Memory
    32-bit address space
    8-bit cell
    2)Register File
    32 32-bit registers, with 2 read ports and 1 write port

    using following test bench
    // Add the number in memory address 0 and 1 to address 3
    Load r1, #0
    Load r2, #1
    Add r3, r1, r2
    Store r3, #3
    '''

    def __init__(self):
        self.MEM = np.zeros(2**32, dtype=np.uint8)
        self.REG = np.zeros(32, dtype=np.uint32)

    def load(self, reg, mem):
        self.REG[reg] = self.MEM[mem]

    def store(self, reg, mem):
        self.MEM[mem]  = self.REG[reg] & 0xFF

    def add(self, reg3, reg1, reg2):
        self.REG[reg3] = self.REG[reg1] + self.REG[reg2]
        # 隐式体现2个读端口、1个写端口

    def run(self, insts):
        for inst in insts:
            inst = inst.split(' ')
            if inst[0] == "Load":
                self.load(eval(inst[1][1:-1]), eval(inst[2][1:]))
            elif inst[0] == "Add":
                self.add(eval(inst[1][1:-1]), eval(inst[2][1:-1]), eval(inst[3][1:]))
            elif inst[0] == "Store":
                self.store(eval(inst[1][1:-1]), eval(inst[2][1:]))

def print8bit(num):
    print(format(num, '08b'))

def print32bit(num):
    print(format(num, '032b'))

def test(insts, a, b):
    cpu = CPU()
    cpu.MEM[0] = a
    cpu.MEM[1] = b

    cpu.run(insts)
    print("MEM[0] = ", end = ''); print8bit(a)
    print("MEM[1] = ", end = ''); print8bit(b)
    print("MEM[3] = ", end = ''); print8bit(cpu.MEM[3])

if __name__ == "__main__":
    insts = [
        "Load r1, #0",
        "Load r2, #1",
        "Add r3, r1, r2",
        "Store r3, #3"
    ]

    print("===== test 0 =====")
    test(insts, 2**8-1, 2**8-1)
    print()

    for i in range(5):
        print("===== test %d =====" % (i+1))
        a = random.randint(0, 2**8-1)
        b = random.randint(0, 2**8-1)
        test(insts, a, b)
        print()
