import sys

class errors():
    def checkLabel(inst, label_num, label_dict):
        label_num+=1
        if inst[1] in label_dict.keys():
            return
        else:
            sys.stdout.write(f'Error at line {label_num}: label not defined\n')
            sys.exit()
    def labelAlreadyExists(label, line_num, label_dict):
        line_num+=1
        if label in label_dict.keys():
            sys.stdout.write(f'Error at line {line_num}: label already exists\n')
            sys.exit()


    def check_reg(reg, rdict, line_num):
        line_num+=1
        if reg not in rdict:
            sys.stdout.write(f"Error: line {line_num}, register {reg} you are trying to access does not exist\n")
            sys.exit()


    def check_types(ins, opCode, line_num):
        line_num+=1
        if ins not in opCode:
            sys.stdout.write(f"Error: line {line_num}, instruction {ins} does not exist\n")
            sys.exit()
    def check_funct3(ins, opCode, line_num):
        line_num+=1
        if ins not in opCode:
            sys.stdout.write(f"Error: line {line_num}, instruction {ins} does not exist\n")
            sys.exit()
    def check_funct7(ins, opCode, line_num):
        line_num+=1
        if ins not in opCode:
            sys.stdout.write(f"Error: line {line_num}, instruction {ins} does not exist\n")
            sys.exit()
    def tooManyArguments(line_num):
        line_num+=1
        sys.stdout.write(f'Error at line {line_num}, too many arguments \n')
        sys.exit()

    def tooFewArguments(line_num):
        line_num+=1
        sys.stdout.write(f'Error at line {line_num}, too few arguments\n')
        sys.exit()
    def genError(line_num):
        line_num+=1
        sys.stdout.write(f'General Syntax Error at line {line_num}: something went wrong :( \n')
        sys.exit()
    def memOverflow():
        sys.stdout.write("Error: Memory overflow - too many instructions and/or variables provided.\n")
        sys.exit()
    def nohalt():
        sys.stdout.write("No halt at end of program\n")
        sys.exit()
    def wronghalt(line_num):
        sys.stdout.write(f'Wrong halt attempt at line {line_num} \n')
        sys.exit()
    def immediaterange(decimal_num):
        sys.stdout.write(f'Immediate value out of range: {decimal_num} \n')
        sys.exit()




#funct3
funct3={"add":"000","sub":"000","sll":"001","slt":"010","sltu":"011","xor":"100",
        "srl":"101","or":"110","and":"111","lw":"010","addi":"000","sltiu":"011",
        "jalr":"000","sw":"010",'beq':"000",'bne':"001",'blt':"100",'bge':"101",
        'bltu':"110",'bgeu':"111"}
funct7={"add":"0000000","sub":"0100000","sll":"0000000","slt":"0000000","sltu":"0000000","xor":"0000000",
        "srl":"0000000","or":"0000000","and":"0000000"}
opcode={"add":"0110011","sub":"0110011","sll":"0110011","slt":"0110011","sltu":"0110011","xor":"0110011",
        "srl":"0110011","or":"0110011","and":"0110011","lw":"0000011","addi":"0010011","sltiu":"0010011",
        "jalr":"1100111","sw":"0100011","beq":"1100011","bne":"1100011","blt":"1100011","bge":"1100011",
        "bltu":"1100011","bgeu":"1100011","lui":"0110111","jal":"1101111","auipc":"0010111"}
registers={"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110",
           "t2":"00111","s0":"01000","fp":"01000","s1":"01001","a0":"01010","a1":"01011","a2":"01100",
           "a3":"01101","a4":"01110","a5":"01111","a6":"10000","a7":"10001","s2":"10010","s3":"10011",
           "s4":"10100","s5":"10101","s6":"10110","s7":"10111","s8":"11000","s9":"11001","s10":"11010",
           "s11":"11011","t3":"11100","t4":"11101","t5":"11110","t6":"11111"}
types={"add":"R","sub":"R","sll":"R","slt":"R","sltu":"R","xor":"R",
        "srl":"R","or":"R","and":"R","lw":"I","addi":"I","sltiu":"I",
        "jalr":"I","sw":"S","beq":"B","bne":"B","blt":"B","bge":"B",
        "bltu":"B","bgeu":"B","lui":"U","jal":"J","auipc":"U"}
class utils():
    def get_funct3(instr,line_num):
        errors.check_funct3(instr,funct3,line_num)
        return funct3[instr]


    #funct7
    def get_funct7(instr,line_num):
        errors.check_funct7(instr,funct7,line_num)
        return funct7[instr]

    #opcode
    def get_opcode(instr, line_num):

        return opcode[instr]

    #Register encoding
    def get_reg(instr,line_num):
        errors.check_reg(instr,registers,line_num)
        return registers[instr]

    def typechecker(instr,line_num):
        x=instr.split()
        errors.check_types(x[0],types,line_num)
        return types[x[0]]


    def decimal_to_binary_1(decimal_num, num_bits,type):
        if (type==2):
            if (int(decimal_num)<-(2**(num_bits-1)) or int(decimal_num)>(2**(num_bits-1)-1)):
                errors.immediaterange(decimal_num)
        else:
            if ( int(decimal_num)<0 or int(decimal_num)>(2**(num_bits)-1)):
                errors.immediaterange(decimal_num)
        decimal_num=int(decimal_num)
        if decimal_num >= 0:
            binary_num = bin(decimal_num)[2:].zfill(num_bits)
        else:
            binary_num = bin(decimal_num & int("1"*num_bits, 2))[3:].zfill(num_bits - 1)
            binary_num = '1' + binary_num

        return binary_num


label_dict={}
outputbinary=''

args = sys.argv
inp = args[1]
out = args[2]
reallinumber=0
linenumber=0
virtual_halt='beq zero,zero,0'
try:
    f=open(inp,'r')
    assembly = f.read().split('\n')
    for i in range(len(assembly)):
        linenumber+=1
        if assembly[i].strip()=='':

            continue
        if ':' in assembly[i]:
            labelseperator=assembly[i].split(':')

            if ' ' in labelseperator[0] or ',' in labelseperator[0]:
                errors.genError(linenumber)
            errors.labelAlreadyExists(labelseperator[0],i,label_dict)
            label_dict[labelseperator[0]]=reallinumber*4
            if labelseperator[1].strip()!='':
                assembly[i]=labelseperator[1].lstrip()
            else:
                assembly[i]=''

                continue
        else:
            assembly[i]=assembly[i].lstrip()


        reallinumber+=1
        if reallinumber>64:
            errors.memOverflow()

    f.close()
except SystemExit:
    print('Exiting')
    sys.exit()
except:
    errors.genError(linenumber)
linenumber=0


def typeR(instr, line_num):
  l2=instr.split(' ',1)
  l1=l2[1].lstrip().split(',')
  if len(l1)>3:
    errors.tooManyArguments(line_num)
  elif len(l1)<3:
    errors.tooFewArguments(line_num)
  opcode=utils.get_opcode(l2[0],line_num)
  funct3=utils.get_funct3(l2[0],line_num)
  funct7=utils.get_funct7(l2[0],line_num)
  rs2=utils.get_reg(l1[2],line_num)
  rs1=utils.get_reg(l1[1],line_num)
  rd=utils.get_reg(l1[0],line_num)
  return funct7+rs2+rs1+funct3+rd+opcode

def typeI(instr, line_num):
  l3=instr.split(' ',1)
  l1=l3[1].lstrip().split(',')
  opcode=utils.get_opcode(l3[0],line_num)
  funct3=utils.get_funct3(l3[0],line_num)
  if l3[0]=='lw':
     l2=l1[1].split('(')
     if len(l1)>2 or len(l2)>2:
      errors.tooManyArguments(line_num)
     elif len(l1)<2 or len(l2)<2:
      errors.tooFewArguments(line_num)
     imm=(utils.decimal_to_binary_1(l2[0],12,2))
     rs1=utils.get_reg(l2[1][:-1],line_num)
     rd=utils.get_reg(l1[0],line_num)
     return imm+rs1+funct3+rd+opcode
  else:
    if len(l1)>3:
      errors.tooManyArguments(line_num)
    elif len(l1)<3:
      errors.tooFewArguments(line_num)
    imm=(utils.decimal_to_binary_1(l1[2],12,2))
    rs1=utils.get_reg(l1[1],line_num)
    rd=utils.get_reg(l1[0],line_num)
    return imm+rs1+funct3+rd+opcode


#U Type Instruction set
def typeU(instr, line_num):

#Obtaining desired immediate value
    l1=instr.split(",")
    l2=instr.split(" ")
    l3 = l2[1].split(",")
    if len(l3)>2:
      errors.tooManyArguments(line_num)
    elif len(l3)<2:
      errors.tooFewArguments(line_num)
    a = utils.decimal_to_binary_1(int(l1[1]), 32,2)
    b = a[::-1]
    c = b[12:32]
    d = c[::-1]

#Obtaining desired register encoding
    reg_x = instr.split(",")
    reg_y = reg_x[0].split()
    reg_z = reg_y[1]
    reg = utils.get_reg(reg_z, line_num) # get_reg function to be defined

#Obtaining desired opcode
    opcode_x = instr.split()
    opcode_y = opcode_x[0]
    opcode = utils.get_opcode(opcode_y, line_num) # get_opcode function to be defined

    return d + reg + opcode

def typeJ(instr, line_num):
    l1=instr.split(",")
    l2 = l1[1].split("(")
    if (l2[0].isnumeric() == False and l2[0][0] != "-"):
        imm=label_dict[l2[0]]-(line_num)*4
        imm=str(utils.decimal_to_binary_1(imm,20,2))
        b = imm[::-1]
        c = b[19]+(b[1:11])[::-1]+b[10]+(b[11:19])[::-1]
    else:
        a = utils.decimal_to_binary_1(int(l2[0]), 20,2)
        b = a[::-1]
        c = b[19]+(b[1:11])[::-1]+b[10]+(b[11:19])[::-1]
    l3 = instr.split()
    l4 = l3[1].split(",")
    if len(l4)>2:
      errors.tooManyArguments(line_num)
    elif len(l4)<2:
      errors.tooFewArguments(line_num)
    reg_x = instr.split(",")
    reg_y = reg_x[0].split()
    reg_z = reg_y[1]
    reg = utils.get_reg(reg_z, line_num)
    opcode_x = instr.split()
    opcode_y = opcode_x[0]
    opcode = utils.get_opcode(opcode_y, line_num)
    return c + reg + opcode

def typeS(instr, line_num):
    l3=instr.split(' ',1)
    l1=l3[1].lstrip().split(',')
    opcode=utils.get_opcode(l3[0], line_num)
    l2=l1[1].split('(')
    count=((len(l3)-1)+(len(l1)-1)+len(l2))
    if count>4:
      errors.tooManyArguments(line_num)
    if count<4:
      errors.tooFewArguments(line_num)
    imm=str(utils.decimal_to_binary_1(l2[0],12,2))
    immone=imm[0:7]
    rs2=utils.get_reg(l1[0],line_num)
    rs1=utils.get_reg(l2[1][:-1],line_num)
    funct3=utils.get_funct3(l3[0],line_num)
    immtwo=imm[7:]
    return immone+rs2+rs1+funct3+immtwo+opcode

def typeB(instr, line_num):
    l3=instr.split(' ',1)
    l1=l3[1].lstrip().split(',')
    count=(len(l3)-1)+(len(l1))
    if count>4:
      errors.tooManyArguments(line_num)
    if count<4:
      errors.tooFewArguments(line_num)
    opcode=utils.get_opcode(l3[0], line_num)
    funct3=utils.get_funct3(l3[0],line_num)
    if (l1[2].isnumeric()==False and l1[2][0]!="-"):
        imm=label_dict[l1[2]]-(line_num)*4

        imm=str(utils.decimal_to_binary_1(imm,12,2))
    else:
        imm=str(utils.decimal_to_binary_1(l1[2],12,2))
    immone=imm[0]+imm[1:7]
    rs2=utils.get_reg(l1[1],line_num)
    rs1=utils.get_reg(l1[0],line_num)
    immtwo=imm[7:-1]+imm[0]
    return immone+rs2+rs1+funct3+immtwo+opcode
# try:
for i in range(len(assembly)):
    linenumber+=1
    if assembly[i].strip()=='':
        continue
    type=utils.typechecker(assembly[i],i)
    if (type=='R'):

        outputbinary+=typeR(assembly[i],i)+'\n'
    elif (type=='I'):
        outputbinary+=typeI(assembly[i],i)+'\n'
    elif (type=='S'):
        outputbinary+=typeS(assembly[i],i)+'\n'
    elif (type=='B'):
        outputbinary+=typeB(assembly[i],i)+'\n'
    elif (type=='U'):
        outputbinary+=typeU(assembly[i],i)+'\n'
    elif (type=='J'):
        outputbinary+=typeJ(assembly[i],i)+'\n'
    if (i==len(assembly)-1 and assembly[i]!=virtual_halt):
            errors.nohalt()

# except SystemExit:
#     print('Exiting')
#     sys.exit()
# except:
#     errors.genError(linenumber)
f=open(out,'w')
f.write(outputbinary)

f.close()
