class J_type:
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)
        self.instr=self.parse(self.instr,[20,25,32])
        self.imm = self.instr[0]
        self.rd=self.instr[1]
        #self.comp=(self.opcode,)
    def execute(self):
        print("j type")
        #a = (a >> 4) << 4
        registers[self.rd]=self.pc+4
        print('rd = ', self.rd, ' value at rd = ', registers[self.rd])
        #self.rd=self.pc+4
        #imm = imm[::-1]
        #imm = imm[20] + imm[10:0:-1] +imm[11] + imm[19:11:-1]
        print('unscrambled imm = ', self.imm)
        self.imm = self.imm[10:0:-1] + self.imm[11] + self.imm[19:11:-1] + self.imm[0]
        self.imm=self.imm[::-1] + '0'
        # self.imm = self.imm[0] + self.imm[13::] + self.imm[12] + self.imm[1:12]
        # self.imm=self.imm[20]+self.imm[10:0:-1]+self.imm[11]+self.imm[19:11:-1]
        # self.imm[::-1]
        print('imm binary = ', self.imm)
        if self.imm[0] == '0':
            self.pc=self.pc+int(self.imm,2)
            print('imm = ', int(self.imm,2))
        else:
            self.pc=self.pc-int(self.twoscomp(int(self.imm,2),20),2)
            print('imm = ', -int(self.twoscomp(int(self.imm,2),20),2))
        # self.pc=(self.pc>>1)<<1

class U_type(instr):
    def __init__(self,ins:str,pc:int) -> None:
        super().__init__(ins,pc)
        self.instr = self.parse(self.instr, [20,25,32])
        self.imm = self.instr[0]
        self.rd = self.instr[1]
        self.op = self.instr[2]
        print(self.instr)
        imm = self.imm + 12*'0'
        self.sextimm = int(imm,2) if imm[0]=='0' else -int(self.twoscomp(int(self.imm,2),32),2)
    def execute(self):
        print('u type')
        if self.op=='0110111': #lui
            registers[self.rd] = self.sextimm
        else:
            registers[self.rd] = self.pc+ self.sextimm
        self.pc+=4

# Replace typeJ function with J_type class
def typeJ(instruction):
    j_inst = J_type(instruction)
    j_inst.execute()

# Replace typeU function with U_type class
def typeU(instruction):
    u_inst = U_type(instruction)
    u_inst.execute()

def findTwoscomplement(str):
    n = len(str)
    i = n - 1
    while(i >= 0):
        if (str[i] == '1'):
            break
        i -= 1
    if (i == -1):
        return '1'+str
    k = i - 1
    while(k >= 0):
        if (str[k] == '1'):
            str = list(str)
            str[k] = '0'
            str = ''.join(str)
        else:
            str = list(str)
            str[k] = '1'
            str = ''.join(str)

        k -= 1
    return str

def decimal_to_binary(decimal_num):
    if(isinstance(decimal_num,str)):
        return decimal_num
    num_bits=32
    decimal_num=int(decimal_num)
    if decimal_num >= 0:
        binary_num = bin(decimal_num)[2:].zfill(num_bits)
    else:
        binary_num = bin(decimal_num & int("1"*num_bits, 2))[3:].zfill(num_bits - 1)
        binary_num = '1' + binary_num
    return binary_num

def dec_To_Binary_unsigned(n):
    return bin(n).replace("0b", "")

def sign_extend(val):
    bits=32
    return val[0]*(bits-len(val))+val

def binary_to_decimal_signed(binary_string):
    if binary_string[0] == '1':
        return -1 * (int(''.join('1' if b == '0' else '0' for b in binary_string), 2) + 1)
    else:
        return int(binary_string, 2)

def bin_to_dec_unsigned(binary_string):
    return int(binary_string, 2)

def add_func(rd,rs1,rs2):
    srs1=binary_to_decimal_signed(sign_extend(decimal_to_binary(value[rs1])))
    srs2=binary_to_decimal_signed(sign_extend(decimal_to_binary(value[rs2])))
    value[rd]=srs1+srs2

def sub_func(rd,rs1,rs2):
    srs2=binary_to_decimal_signed(findTwoscomplement(sign_extend(decimal_to_binary(value[rs2]))))
    if rs1=='00000':
        srs1="00000000000000000000000000000000"
    else:
        srs1=binary_to_decimal_signed(sign_extend(decimal_to_binary((value[rs1]))))
    value[rd]=srs1+srs2

def slt_func(rd,rs1,rs2):
    srs1=binary_to_decimal_signed(sign_extend(decimal_to_binary((value[rs1]))))
    srs2=binary_to_decimal_signed(sign_extend(decimal_to_binary((value[rs2]))))
    if srs1<srs2:
        value[rd]=1

def sltu_func(rd,rs1,rs2):
    srs1=bin_to_dec_unsigned(sign_extend(dec_To_Binary_unsigned((value[rs1]))))
    srs2=bin_to_dec_unsigned(sign_extend(dec_To_Binary_unsigned((value[rs2]))))
    if srs1<srs2:
        value[rd]=1

def xor_func(rd,rs1,rs2):
    srs1=binary_to_decimal_signed(sign_extend(decimal_to_binary((value[rs1]))))
    srs2=binary_to_decimal_signed(sign_extend(decimal_to_binary((value[rs2]))))
    value[rd]=srs1^srs2

def sll_func(rd,rs1,rs2):
    srs1=binary_to_decimal_signed(sign_extend(decimal_to_binary(value[rs1])))
    srs2=binary_to_decimal_signed(sign_extend(dec_To_Binary_unsigned(value[rs2][-5:])))
    value[rd]=srs1<<srs2

def srl_func(rd,rs1,rs2):
    srs1=binary_to_decimal_signed(sign_extend(decimal_to_binary(value[rs1])))
    srs2=binary_to_decimal_signed(sign_extend(dec_To_Binary_unsigned(value[rs2][-5:])))
    value[rd]=srs1>>srs2

def or_func(rd,rs1,rs2):
    srs1=binary_to_decimal_signed(sign_extend(decimal_to_binary(value[rs1])))
    srs2=binary_to_decimal_signed(sign_extend(decimal_to_binary(value[rs2])))
    value[rd]=srs1|srs2

def and_func(rd,rs1,rs2):
    srs1=binary_to_decimal_signed(sign_extend(decimal_to_binary(value[rs1])))
    srs2=binary_to_decimal_signed(sign_extend(decimal_to_binary(value[rs2])))
    value[rd]=srs1&srs2

def typeR(x):
    for j in registers.values():
        if j==x[-8:-13:-1]:
            rd=j
        if j==x[-16:-21:-1]:
            rs1=j
        if j==x[-21:-26:-1]:
            rs2=j
    for j in funct3.values():
        if j==x[-13:-16:-1]:
            funct3=j
            break
    for j in funct7.values():
        if j==x[-26:-33:-1]:
            funct7=j
            break
    if funct3=="000":
        if funct7=="0000000":
            add_func(rd,rs1,rs2)
        if funct7=="0100000":
            sub_func(rd,rs1,rs2)
    elif funct3=="001":
        sll_func(rd,rs1,rs2)
    elif funct3=="010":
        slt_func(rd,rs1,rs2)
    elif funct3=="011":
        sltu_func(rd,rs1,rs2)
    elif funct3=="100":
        xor_func(rd,rs1,rs2)
    elif funct3=="101":
        srl_func(rd,rs1,rs2)
    elif funct3=="110":
        or_func(rd,rs1,rs2)
    elif funct3=="001":
        and_func(rd,rs1,rs2)


class I_type():
    def _init_(self,ins:str,pc:int) -> None:
        super()._init_(ins,pc)
        self.instr = self.parse(self.instr,[12,17,20,25,32])
        self.imm = self.instr[0] #signed or unsigned check
        self.rs1 = self.instr[1]
        self.rd = self.instr[3]
        self.comp = (self.opcode,self.instr[2],)
    def execute(self):
        if self.comp == I_['lw']:
            if self.imm[0] == '0': registers[self.rd] = mem[int(self.imm,2) + registers[self.rs1]]
            else: registers[self.rd] = mem[-int(self.twoscomp(int(self.imm,2),12),2)+ registers[self.rs1]]
            self.pc += 4

        elif self.comp == I_['addi']:
            sextimm = int(self.imm,2) if self.imm[0]=='0' else -int(self.twoscomp(int(self.imm,2),12),2)
            if self.imm[0] == '0': registers[self.rd] = int(self.imm,2) + registers[self.rs1]
            else: registers[self.rd] = -int(self.twoscomp(int(self.imm,2),12),2) + registers[self.rs1]
            self.pc += 4

        elif self.comp == I_['sltiu']:
            registers[self.rd] = 1 if int(self.imm,2) > registers[self.rs1] else 0
            self.pc += 4

        elif self.comp == I_['jalr']:
            registers[self.rd] = self.pc + 4
            if self.imm[0] == '0': self.pc = (registers[self.rs1] + int(self.imm,2))& ~1
            else: self.pc = (registers[self.rs1] - int(self.twoscomp(int(self.imm,2),12),2))& ~1
            if self.pc%2 != 0: self.pc -= 1
            if self.pc<0:
                self.pc = 2**32 + self.pc

def typeI(instruction):
    I_inst = I_type(instruction)
    I_inst.execute()


# Other code remains unchanged
registers = {'zero' : '00000', 'ra': '00001', 'sp': '00010', 'gp': '00011', 'tp': '00100', 't0':'00101', 't1': '00110', 't2': '00111','s0': '01000', 'fp': '01000', 's1': '01001','a0': '01010', 'a1': '01011', 'a2': '01100', 'a3': '01101', 'a4': '01110', 'a5': '01111','a6':'10000',  'a7':'10001', 's2': '10010', 's3': '10011', 's4': '10100', 's5': '10101', 's6': '10110', 's7': '10111', 's8': '11000', 's9': '11001', 's10': '11010', 's11': '11011','t3': '11100', 't4': '11101', 't5':'11110', 't6': '11111'}
value  = {}
for i in registers:
    value[registers[i]] = 0
memory={}
PC={}
types={'1100011':'B',"1101111":'J',"0110111":'U',"0010111":'U',"0100011":'S',"0000011":'I',"1100111":'I',"0110011":'R'}

def gettype(a):
    return types[a[-7:]]

def converttohex(d):
    a = str(hex(int(d)))
    b = a[0:2] + "0"*(8 - len(a[2:])) + a[2:]
    return b

def convertbin(decimal_num, num_bits):
        if decimal_num >= 0:
            binary_num = bin(decimal_num)[2:].zfill(num_bits)
        else:
            binary_num = bin(decimal_num & int("1"*num_bits, 2))[3:].zfill(num_bits - 1)
            binary_num = '1' + binary_num

        return binary_num

def printreg():
    for i in value:
        print('0b'+converttobin(value[i],32))

def printmemory():
    for i in memory:
        print(i+':'+'0b'+converttobin(memory[i],32))

for i in range(32):
    memory[converttohex(65536 + i*4)] = 0

f=open("input.txt",'r')
instructions=f.readlines()

count = 4
for i in instructions:
    PC[count] = i.strip()
    count+=4

pcount=4
while(pcount<=4*len(instructions)):
    currentinstruction=PC[pcount]
    typ=gettype(currentinstruction)
    if typ=='R':
        typeR(currentinstruction)
    elif typ=='B':
        typeB(currentinstruction)
    elif typ=='J':
        typeJ(currentinstruction)
    elif typ=='I':
        typeI(currentinstruction)
    elif typ=='S':
        typeS(currentinstruction)
    elif typ=='U':
        typeU(currentinstruction)
    printreg()

printreg()
printmemory()