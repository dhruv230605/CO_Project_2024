import sys

reg = {'zero' : '00000', 'ra': '00001', 'sp': '00010', 'gp': '00011', 'tp': '00100', 't0':'00101', 't1': '00110', 't2': '00111','s0': '01000', 'fp': '01000', 's1': '01001','a0': '01010', 'a1': '01011', 'a2': '01100', 'a3': '01101', 'a4': '01110', 'a5': '01111','a6':'10000',  'a7':'10001', 's2': '10010', 's3': '10011', 's4': '10100', 's5': '10101', 's6': '10110', 's7': '10111', 's8': '11000', 's9': '11001', 's10': '11010', 's11': '11011','t3': '11100', 't4': '11101', 't5':'11110', 't6': '11111'}
registers = {'zero' : '00000', 'ra': '00001', 'sp': '00010', 'gp': '00011', 'tp': '00100', 't0':'00101', 't1': '00110', 't2': '00111','s0': '01000', 'fp': '01000', 's1': '01001','a0': '01010', 'a1': '01011', 'a2': '01100', 'a3': '01101', 'a4': '01110', 'a5': '01111','a6':'10000',  'a7':'10001', 's2': '10010', 's3': '10011', 's4': '10100', 's5': '10101', 's6': '10110', 's7': '10111', 's8': '11000', 's9': '11001', 's10': '11010', 's11': '11011','t3': '11100', 't4': '11101', 't5':'11110', 't6': '11111'}
bfncodes = {"beq": "000", "bne": "001", "bge":"101", "bgeu":"111", "blt": "100",  "bltu":"110"}
rfncodes = {"add": "000", "sub":"000", "sll":"001", "slt":"010", "sltu":"011", "xor":"100", "srl":"101", "or":"110","and":"111"}
acreg = {}
currentline = {}
values  = {}
memory = {}
findict = {}

#Doubts
#Do we have to error handling? 
#What about caller and callee saved registers
#is there use of static
#Dhruv and Altamash cleared all doubts with TA in doubt session

file_input = sys.argv[1]
file_output = sys.argv[2]

for i in registers:
    values[reg[i]] = "0"*32


def bin_to_int(a):
    b = 0
    j = len(a)-1
    for i in range(len(a)):
        b += (int(a[i])) * (2 ** j)
        j-=1
    return b

def twoscptoint(a):
    new = ''
    if a[len(a)-1] == "1":
        for i in range(0, len(a)-1):
            if a[i] == "0":
                new+="1"
            else:
                new+="0"
        new+= "1"
        c = bin_to_int(new)
        c = "-" +  str(c)
        return int(c)
    else:
        for i in range(0, len(a)):
            if a[i] == "0":
                new+="1"
            else:
                new+="0"
        d = addnum(new, "0"*(len(new)-1) + "1")
        c = bin_to_int(d)
        c = "-" +  str(c)
        return int(c)


#This isn't working, someone Please fix this. My other functions depend on this.]
# def twoscptoint(a):
#     new = ''
#     if a[len(a)-1] == "1":
#         for i in range(0, len(a)-1):
#             if a[i] == "0":
#                 new+="1"
#             else:
#                 new+="0"
#         new+= "1"
#         c = bin_to_int(new)
#      
#         return int(c)
#     else:
#         for i in range(0, len(a)):
#             if a[i] == "0":
#                 new+="1"
#             else:
#                 new+="0"
#         d = addnum(new, "0"*(len(new)+1) + "1")
#         c = bin_to_int(d)
#         c = "-" +  str(c)
#         return int(c)

def inttobinary(a):
    sumn = ''
    if a == 0:
        return "0"*32
    while(a!=0):
        if (a == 1):
            a-=1
            sumn+="1"
        b = a%2
        sumn+=str(b)
        a = a//2
    return ("0" * (32 - len(sumn)) + sumn[::-1])

def addnum(a, b):
    sum = bin(int(a, 2) + int(b, 2))
    return(sum[2:])

def twoscp(a):
    cp = ''
    for i in range(len(str(a))):
        if a[i]=="1":
            cp+="0"
        else:
            cp+="1"
    b = ("0"*(len(str(a))-1))+"1"
    y = addnum(cp,b)
    return "0"*(32- len(y)) + y
def convert(a, n):
    if (n==0):
        if a[0] == "1":
            return twoscptoint(a)
        else:
            return bin_to_int(a)
    else:
        return bin_to_int(a)


#@Altamash
def converttohex(d):
    a = str(hex(int(d)))
    b = a[0:2] + "0"*(8 - len(a[2:])) + a[2:]
    return b
def a2bin(a, b):
    Sum = bin(int(a, 2) + int(b, 2))
    return (len(a) - len(Sum[2:]))* '0' + Sum[2:]
def sign_extension(a):
    if a[0] == '0':
        return ((32 - len(a)) * '0') + a
    else:
        return ((32 - len(a)) * '1') + a
def twoc(a):
    cp = ''
    for i in range(len(str(a))):
        if a[i]=="1":
            cp+="0"
        else:
            cp+="1"
    b = "1"
    y = a2bin(cp,b)
    return sign_extension(y)
def inttob(a):
    sumn = ''
    if a == 0:
        return "0"
    while(a!=0):
        if (a == 1):
            a-=1
            sumn+="1"
        b = a%2
        sumn+=str(b)
        a = a//2
    return sumn
def itb(a):
    if a >= 0:
        return sign_extension(inttob(a))
    else:
        return twoc(inttob(a -(2*a)))

def twos_complement(binary_str, num_bits):
    if binary_str[0] == '1':
        temp = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        temp_decimal = int(temp, 2)
        twos_comp = -(temp_decimal+ 1)
        return twos_comp
    else:
        return int(binary_str, 2)

#typeR
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

def signextension(val):
    bits=32
    return val[0]*(bits-len(val))+val

def bin_to_dec_signed(binary_string):
    if binary_string[0] == '1':
        return -1 * (int(''.join('1' if b == '0' else '0' for b in binary_string), 2) + 1)
    else:
        return int(binary_string, 2)

def bin_to_dec_unsigned(binary_string):
    return int(binary_string, 2)


#@Dhruv
def add_func(rd,rs1,rs2):
    srs1=bin_to_dec_signed(signextension(decimal_to_binary(values[rs1])))
    srs2=bin_to_dec_signed(signextension(decimal_to_binary(values[rs2])))
    values[rd]=srs1+srs2


def slt(rd,rs1,rs2):
    srs1=bin_to_dec_signed(signextension(decimal_to_binary((values[rs1]))))
    srs2=bin_to_dec_signed(signextension(decimal_to_binary((values[rs2]))))
    if srs1<srs2:
        values[rd]=1
def altu(rd,rs1,rs2):
    srs1=bin_to_dec_unsigned(signextension(dec_To_Binary_unsigned((values[rs1]))))
    srs2=bin_to_dec_unsigned(signextension(dec_To_Binary_unsigned((values[rs2]))))
    if srs1<srs2:
        values[rd]=1
def or_func(rd,rs1,rs2):
    srs1=bin_to_dec_signed(signextension(decimal_to_binary(values[rs1])))
    srs2=bin_to_dec_signed(signextension(decimal_to_binary(values[rs2])))
    values[rd]=srs1|srs2

def and_func(rd,rs1,rs2):
    srs1=bin_to_dec_signed(signextension(decimal_to_binary(values[rs1])))
    srs2=bin_to_dec_signed(signextension(decimal_to_binary(values[rs2])))
    values[rd]=srs1&srs2

def xor(rd,rs1,rs2):
    srs1=bin_to_dec_signed(signextension(decimal_to_binary((values[rs1]))))
    srs2=bin_to_dec_signed(signextension(decimal_to_binary((values[rs2]))))
    values[rd]=srs1^srs2

def sub(rd,rs1,rs2):
    srs2=bin_to_dec_signed(findTwoscomplement(signextension(decimal_to_binary(values[rs2]))))
    if rs1=='00000':
        srs1="00000000000000000000000000000000"
    else:
        srs1=bin_to_dec_signed(signextension(decimal_to_binary((values[rs1]))))
    values[rd]=srs1+srs2

def srl(rd,rs1,rs2):
    srs1=bin_to_dec_signed(signextension(decimal_to_binary(values[rs1])))
    srs2=bin_to_dec_signed(signextension(dec_To_Binary_unsigned(values[rs2][-5:])))
    values[rd]=srs1>>srs2

def sll(rd,rs1,rs2):
    srs1=bin_to_dec_signed(signextension(decimal_to_binary(values[rs1])))
    srs2=bin_to_dec_signed(signextension(dec_To_Binary_unsigned(values[rs2][-5:])))
    values[rd]=srs1<<srs2

#Try to follow this format
# # format(sign_extend(format_2(value[rs1])))
#     srs2=binary_ format(format_2(value[rs2])))
#     value[rd]=srs1|srs2


def typeJ(instruction, pc):
    # j_inst = J_type(instruction)
    # j_inst.execute()
    rd = instruction[-12:-7]
    values[rd] = pc+4
    immediate =  instruction[12:20] + instruction[11] + instruction[1:11] + "0"
    pc = pc+bin_to_dec_signed(immediate)
    return pc

    # c = b[19]+(b[1:11])[::-1]+b[10]+(b[11:19])[::-1]


#Text for memory, look into this.
#(a) Program Memory: The size of program memory is 256 bytes, and each location can
# store 32 bits. Eventually, we have 64 locations to store our instructions. The instruction
# memory ranges from {0x0000 0000, 0x0000 00FF}.
# (b) Stack Memory: The size of stack memory is 128 bytes, and each location can store 32 bits.
# Eventually, we have 32 locations to stack our register values. The stack grows downwards
# or we need to decrement the stack address before storing any register content. The stack
# memory ranges from {0x0000 0100, 0x0000 017F}.
# (c) Data Memory: The size of data memory is 128 bytes, and each location can store 32 bits.
# Eventually, we have 32 locations in our data memory. The data memory ranges from
# {0x001 0000, 0x0001 007F}.

def typeI(a, pc):
    if a[-7:]=='0000011':
      rd=a[-12:-7]
      rs1 = a[-20:-15]
      immediates = a[0:12]
      immediates = bin_to_dec_signed(immediates)
      loc = values[rs1] + immediates
      loc = converttohex(loc)
      values[rd] = memory[loc]
      return pc+4

    if a[-7:]=='0010011':
        if a[-15:-12] == '000':
            rs1 = a[-20:-15]
            rd=a[-12:-7]
            immediates = a[0:12]
            immediates = bin_to_dec_signed(immediates)
            loc = values[rs1] + immediates
            values[rd] = loc
            return pc+4
        elif a[-15:-12] == '011':
            rd=a[-12:-7]
            rs1 = a[-20:-15]
            immediates = a[0:12]
            immediates = bin_to_dec_signed(immediates)
            if values[rs1]<immediates :
                values[rd] = 1
            return pc+4
            # value[rd] = memory[immediate]
    if a[-7:]=='1100111':
        rd=a[-12:-7]
        if rd!= '00000':
            values[rd] = pc + 4
        rs1 = a[-20:-15]
        immediates = a[0:12]
        immediates = bin_to_dec_signed(immediates)
        pc = values[rs1] + immediates
        pc = pc - pc%4 #Making lsb = 0
        return pc



#I think this is wrong. Please look into this. @Aarushi
#     if a[-7:]=='1100111':
#         rd=a[-12:-7]
#         if rd!= '00000':
#             value[rd] = pc + 4
#         rs1 = a[-20:-15]
#         immediate = a[0:12]
#         immediate = binary_to_decimal_signed(immediate)
#         pc = value[rs1] + immediate
#         pc = pc - pc%4 #Making lsb = 0
#         return pc

# for i in range(32):
#     memory[converttohex(65536 + i*4)] = 0

# Replace typeU function with U_type class @Aanya
def typeU(a, pc):
    if a[-7:]=='0110111':
        rd=a[-12:-7]
        values[rd]=bin_to_dec_signed(a[:-12])

    if a[-7:]=='0010111':
        rd=a[-12:-7]
        values[rd]=pc+bin_to_dec_signed(a[:-12])


#type S
def execute_typeS(instruction, value, pc, mem):
    register1=instruction[12:17]
    valreg1=value[register1]
    reg2=instruction[7:12]
    valreg2=value[reg2]
    immval=instruction[0:7]+instruction[20:25]
    mem[converttohex(65536 + (valreg1+int(twos_complement(immval,12)))*4)]=valreg2
    pc+=4
    return pc
def typeR(x):
    function3={"add":"000","sub":"000","sll":"001","slt":"010","sltu":"011","xor":"100",
        "srl":"101","or":"110","and":"111","lw":"010","addi":"000","sltiu":"011",
        "jalr":"000","sw":"010",'beq':"000",'bne':"001",'blt':"100",'bge':"101",
        'bltu':"110",'bgeu':"111"}
    function7={"add":"0000000","sub":"0100000","sll":"0000000","slt":"0000000","sltu":"0000000","xor":"0000000",
        "srl":"0000000","or":"0000000","and":"0000000"}
    for j in registers.values():
        if j==x[-8:-13:-1]:
            rd=j
        if j==x[-16:-21:-1]:
            rs1=j
        if j==x[-21:-26:-1]:
            rs2=j
    for j in function3.values():
        if j==x[-13:-16:-1]:
            funct3=j
            break
    for j in function7.values():
        if j==x[-26:-33:-1]:
            funct7=j
            break
    if funct3=="000":
        if funct7=="0000000":
            add_func(rd,rs1,rs2)
        if funct7=="0100000":
            sub(rd,rs1,rs2)
    elif funct3=="001":
        sll(rd,rs1,rs2)
    elif funct3=="010":
        slt(rd,rs1,rs2)
    elif funct3=="011":
        altu(rd,rs1,rs2)
    elif funct3=="100":
        xor(rd,rs1,rs2)
    elif funct3=="101":
        srl(rd,rs1,rs2)
    elif funct3=="110":
        or_func(rd,rs1,rs2)
    elif funct3=="001":
        and_func(rd,rs1,rs2)

#typeB
def execute_typeB(instructions, pc, value):
    immediate=''
    immediate+= instructions[24] + instructions[1:7] + instructions[20:24] 
    immediate+="0"
    register2=instructions[7:12]
    register1=instructions[12:17]
    #Please fill in the funct @Dhruv
    if(instructions[17:20]=="000"):
        if(value[register2]==value[register1]):
            pc=pc+int(twos_complement(immediate,12))
            return pc
        else:
            pc+=4
            return pc
    elif(instructions[17:20]=="001"):
        if(value[register2]!=value[register1]):
            pc=pc+int(twos_complement(immediate,12))
        
            return pc
        else:
            pc+=4
            return pc
    elif(instructions[17:20]=="100"):
        if(value[register2]>value[register1]):
            pc=pc+int(twos_complement(immediate,12))
            return pc
        else:
            pc+=4
            return pc
    elif(instructions[17:20]=="101"):
        if(value[register2]<=value[register1]):
            pc=pc+int(twos_complement(immediate,12))
            return pc
        else:
            pc+=4
            return pc
    elif(instructions[17:20]=="110"):
        unsignedreg1=2**32+value[register1] if value[register1] <0 else value[register1]
        unsignedreg2=2**32+value[register2] if value[register2] <0 else value[register2]
        if(unsignedreg1<unsignedreg2):
            pc=pc+int(twos_complement(immediate,12))
            return pc
        else:
            pc+=4
            return pc
    elif(instructions[17:20]=="111"):
        unsignedreg1=2**32+value[register1] if value[register1] <0 else value[register1]
        unsignedreg2=2**32+value[register2] if value[register2] <0 else value[register2]
        if(unsignedreg1>=unsignedreg2):
            pc=pc+int(twos_complement(immediate,12))
            return pc
        else:
            pc+=4
            return pc
isbranch = False


#Output format given in document. @Altamash check this final then we're done.
#Output format to be stored in the chosen file after execution of every instruction. If you have
# not implemented the yellow colored registers store the value ”0” in their place.
# {Program Counter}{Space}{x0}{Space}{x1}{Space}{x2}{Space}..............{Space}{x31}
# The memory at the simulator side should be of size (32X32-bit). The output will have all the
# memory content (32 lines) printed starting from address (0x0000 0000). Output format of memory
# after the execution of Virtual Halt.
# 32-bit binary data
# 32-bit binary data
# 32-bit binary data
# .
# .
# .
# 32-bit binary data


#I ran it on my system and it shows this:
#Traceback (most recent call last):
#   File "/Users/dhruv/Downloads/Simulator.py", line 12, in <module>
#     file_input = sys.argv[1]
#                  ~~~~~~~~^^^
# IndexError: list index out of range
# @Altamash please try running this on your system and let me know
# @Dhruv Yes, it works

with open(file_input, "r") as fh:
    a = fh.readlines()
with open(file_output, "w") as fh:
    values['00010'] = "00000000000000000000000100000000"
    count = 0
    count1 = 65536
    while (count1 != 65664):
        memory[converttohex(count1)] = "0"*32
        count1 += 4
    for i in a:
        currentline[count] = i.strip()
        count += 4
    i = 0
    

    while(i<=count):
        if (currentline[i] != "00000000000000000000000001100011"):
            s = []
        if currentline[i] == "00000000000000000000000001100011":
            break
        elif currentline[i][25:32] == "0100011":
            imm = currentline[i][0:7] + currentline[i][20:25]
            rs2 = currentline[i][7:12]
            rs1 = currentline[i][12:17]
            rdval = values[rs1]
            if imm[0] == 1:
                fin = twoscptoint(rdval)
            else:
                fin = bin_to_int(rdval)
            if imm[0] == 1:
                finimm = twoscptoint(imm)
            else:
                finimm = bin_to_int(imm)
            memory[converttohex(fin + finimm)] = values[rs2]
            i+=4
            fh.write("0b" + inttobinary(i) + " ")
            for tester in values:
                fh.write("0b" + values[tester] + " ")
                s.append("0b" + values[tester])
            fh.write("\n")
        elif currentline[i][25:32] == "1101111":
            o = ''
            o+=  currentline[i][12:20] + currentline[i][11] + currentline[i][1:11] + "0"
            rd = currentline[i][20: 25]
            a = convert(o, 0)
            if (i+4)<0:
                f = inttobinary(i+4)
                values[rd] = twoscp(f)
            else:
                values[rd] = inttobinary(i+4)
            i+=a
            fh.write("0b" + inttobinary(i) + " ")
            for tester in values:
                fh.write("0b" + values[tester] + " ")
                s.append("0b" + values[tester])
            fh.write("\n")
        elif currentline[i][25:32] == "1100011":
            o = ''
            o+= currentline[i][24] + currentline[i][1:7] + currentline[i][20:24] + "0"
            a = convert(o, 0)
            if currentline[i][17:20] == "000":
                rs1 = currentline[i][12:17]
                rs2 = currentline[i][7:12]
                if (convert(values[rs1], 0) == convert(values[rs2], 0)):
                    i+=a
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
                else:
                    i+=4
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
            elif currentline[i][17:20] == "001":
                rs1 = currentline[i][12:17]
                rs2 = currentline[i][7:12]
                if convert(values[rs1], 0) != convert(values[rs2],0):
                    i+=a
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
                else:
                    i+=4
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
            elif currentline[i][17:20] == "101":
                rs1 = currentline[i][12:17]
                rs2 = currentline[i][7:12]
                if (convert(values[rs1], 0) >= convert(values[rs2], 0)):
                    i+=a
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
                else:
                    i+=4
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
            elif currentline[i][17:20] == "111":
                rs1 = currentline[i][12:17]
                rs2 = currentline[i][7:12]
                if (convert(values[rs1], 1) >= convert(values[rs2], 1)):
                    i+=a
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
                else:
                    i+=4
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
            elif currentline[i][17:20] == "100":
                rs1 = currentline[i][12:17]
                rs2 = currentline[i][7:12]
                if (convert(values[rs1], 0) < convert(values[rs2], 0)):
                    i+=a
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
                else:
                    i+=4
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
            elif currentline[i][17:20] == "110":
                rs1 = currentline[i][12:17]
                rs2 = currentline[i][7:12]
                if (convert(values[rs1], 1) < convert(values[rs2], 1)):
                    i+=a
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
                else:
                    i+=4
                    fh.write("0b" + inttobinary(i) + " ")
                    for tester in values:
                        fh.write("0b" + values[tester] + " ")
                        s.append("0b" + values[tester])
                    fh.write("\n")
        elif currentline[i][25:32] == "0000011":
            rs = currentline[i][12:17]
            rd = currentline[i][20:25]
            rdval = values[rs]
            imm = currentline[i][0:12]
            if imm[0] == 1:
                fin = twoscptoint(rdval)
            else:
                fin = bin_to_int(rdval)
            if imm[0] == 1:
                finimm = twoscptoint(imm)
            else:
                finimm = bin_to_int(imm)
            values[rd] = memory[converttohex(fin + finimm)] 
            i+=4
            fh.write("0b" + inttobinary(i) + " ")
            for tester in values:
                fh.write("0b" + values[tester] + " ")
                s.append("0b" + values[tester])
            fh.write("\n")
        elif currentline[i][25:32] == "0010011":
            if currentline[i][17:20] == "000":
                rs = currentline[i][12:17]
                rd = currentline[i][20:25]
                num1 = convert(values[rs], 0)
                num2 = convert(currentline[i][0:12], 0)
                num = num1 + num2
                #Below one isn't working
                # rs = currentline[i][11:17]
                # rd = currentline[i][20:25]
                # num1 = convert(values[rs], 0)
                # num2 = convert(currentline[i][0:11], 0)
                # num = num1 + num2
                if num < 0:
                    binum = inttobinary(abs(num))
                    binum = twoscp(binum)
                else:
                    binum = inttobinary(num)
                values[rd] =  binum
            elif currentline[i][17:20] == "011":
                rs = currentline[i][12:17]
                rd = currentline[i][20:25]
                if convert(values[rs], 1) < convert(currentline[i][0:12], 1):
                    values[rd] = "0"*31 + "1"
            i+=4
            fh.write("0b" + inttobinary(i) + " ")
            for tester in values:
                fh.write("0b" + values[tester] + " ")
                s.append("0b" + values[tester])
            fh.write("\n")
        elif currentline[i][25:32] == "1100111":
            rs = currentline[i][12:17]
            rd = currentline[i][20:25]
            num = i+4
            if num < 0:
                binum = inttobinary(abs(num))
                binum = twoscp(binum)
            else:
                binum = inttobinary(num)
            if rd != '00000':
                values[rd] = binum
            i = convert(values[rs], 0) + convert(currentline[i][0:12], 0)
            fh.write("0b" + inttobinary(i) + " ")
            for tester in values:
                fh.write("0b" + values[tester] + " ")
                s.append("0b" + values[tester])
            fh.write("\n")
        elif currentline[i][25:32] == "0010111":
            rd = currentline[i][20:25]
            imm = currentline[i][0:20] + "0"*12
            num = i +  convert(imm,0)
            if num < 0:
                binum = inttobinary(abs(num))
                binum = twoscp(binum)
            else:
                binum = inttobinary(num)   
            values[rd] = binum
            i+=4
            fh.write("0b" + inttobinary(i) + " ")
            for tester in values:
                fh.write("0b" + values[tester] + " ")
                s.append("0b" + values[tester])
            fh.write("\n")
        elif currentline[i][25:32] == "0110111":
            rd = currentline[i][20:25]
            imm = currentline[i][0:20] + "0"*12
            num = convert(imm,0)   
            values[rd] = imm
            i+=4
            fh.write("0b" + inttobinary(i) + " ")
            for tester in values:
                fh.write("0b" + values[tester] + " ")
                s.append("0b" + values[tester])
            fh.write("\n")
        elif currentline[i][25:32] == "0000001":
            if currentline[i][17:20] == "000":
                rd = currentline[i][20:25]
                rs1 = currentline[i][12:17]
                rs2 = currentline[i][7:12]
                num = convert(values[rs1],0)*convert(values[rs2],0)
                if num < 0:
                    binum = inttobinary(abs(num))
                    binum = twoscp(binum)
                else:
                    binum = inttobinary(num)
                values[rd] =  binum
            elif currentline[i][17:20] == "001":
                for ele in values:
                    values[ele] = 32*"0"
            elif currentline[i][17:20] == "010":
                break
            elif currentline[i][17:20] == "011":
                rd = currentline[i][20:25]
                rs1 = currentline[i][12:17]
                values[rd] = values[rs1][::-1]
            i+=4
            fh.write("0b" + inttobinary(i) + " ")
            for tester in values:
                fh.write("0b" + values[tester] + " ")
                s.append("0b" + values[tester])
            fh.write("\n")
        elif currentline[i][25:32] == "0110011":
            rs2=currentline[i][7:12]
            rs1=currentline[i][12:17]
            RD=currentline[i][20:25]
            r1=values[rs1]
            r2=values[rs2]
            #sext values
            R1 = sign_extension(r1)
            R2 = sign_extension(r2)
            #add
            if currentline[i][17:20] == "000" and currentline[i][0:7] == "0000000":
                values[RD] = a2bin(R1,R2)
            #sub
            if currentline[i][0:7] == "0100000":
                if rs1 == "00000":
                    values[RD] = twoc(r2)
                else:
                    ans = a2bin(R1,twoc(R2))
                    fa=ans[-1:-33:-1]
                    values[RD]=fa[::-1]
            #sll
            if currentline[i][17:20] == "001":
                low5 = r2[27:32]
                l5=2 ** int(low5,2) 
                ans = int(R1,2) * l5
                values[RD]=sign_extension(inttobinary(int(ans)))
            #slt
            if currentline[i][17:20] == "010":
                if int(R1,2) < int(R2,2):
                    values[RD] = '0' * 31 + '1'
            #sltu
            if currentline[i][17:20] == "011":
                if int(r1,2) < int(r2,2):
                    values[RD] = '0' * 31 + '1'
            #xor
            if currentline[i][17:20] == "100":
                reg1=bin_to_int(R1)
                reg2=bin_to_int(R2)
                regf=reg1 ^ reg2
                regl=len(str(regf))
                ans=(32 - regl)*'0' + str(regf)
                values[RD]=ans
            #srl
            if currentline[i][17:20] == "101":
                low5 = r2[27:32]
                l5=2 ** int(low5,2) 
                ans = int(R1,2) / l5
                values[RD]=sign_extension(inttobinary(int(ans)))
               
            #or
            if currentline[i][17:20] == "110":
                reg1=bin_to_int(R1)
                reg2=bin_to_int(R2)
                regf=reg1 | reg2
                regl=len(str(regf))
                ans=(32 - regl)*'0' + str(regf)
                values[RD]=ans
            #and
            if currentline[i][17:20] == "111":
                reg1=bin_to_int(R1)
                reg2=bin_to_int(R2)
                regf=reg1 & reg2
                regl=len(str(regf))
                ans=(32 - regl)*'0' + str(regf)
                values[RD]=ans
            i+=4
            fh.write("0b" + inttobinary(i) + " ")
            for tester in values:
                fh.write("0b" + values[tester] + " ")
                s.append("0b" + values[tester])
            fh.write("\n")
    fh.write("0b" + inttobinary(i) + " " +  " ".join(s) + " " +  "\n")
    for d in memory:
        fh.write(d + ":" + "0b" + memory[d] + "\n")

#Fin
