from colorama import Fore, Back, Style
from instructions import r_type, i_type, b_type, s_type, reg_conv, j_type

prg_counter = -1

def toBin(x, size=3):
    global prg_counter, line
    if x < 0:
        return toNegBin(x, size)
    out = ""
    while x != 0:
        out += str(x%2)
        x//=2
    if len(out) > size:
        error(prg_counter, line, "immediate value's length is out of bounds")
    out = '0'*(size-len(out)) + out[-1::-1]
    return out

def error(pc,line, mssg):
    print(Fore.RED, Back.YELLOW)
    print('\n ---- ERROR ---- ')
    print(Style.RESET_ALL, Fore.RED)
    print(f"error at line {pc+1}:")
    print(line)
    print(mssg)
    print('\n')
    exit()

def toNegBin(x, size):
    s = toBin(-x-1, size)
    t = ""
    for i in s:
        if i == '1':
            t += '0'
        else:
            t += '1'
    return t

def getImmediate(x):
    n = 0
    while x[n].isdigit():
        n+=1
    return toBin(int(x[0:n]),12)

def getRegVal(x):
    n = 0
    while not x[n].isalpha():
        n+=1
    return toBin(reg_conv[x[n:-1]], 5)

def make_r(ops, registers):
    registers = registers.split(',')
    func7 = toBin(ops[2],7)
    rs2 = toBin(reg_conv[registers[2]],5)
    rs1 = toBin(reg_conv[registers[1]],5)
    func3 = toBin(ops[1],3)
    rd = toBin(reg_conv[registers[0]],5)
    opcode = toBin(ops[0], 7) 
    # print(func7, rs2, rs1, func3, rd, opcode, sep='\n')
    return func7 + rs2 + rs1 + func3 + rd + opcode

def make_i(ops, registers):
    registers = registers.split(',')
    if len(registers) == 3:
        imm = toBin(int(registers[2]), 12)
        rs1 = toBin(reg_conv[registers[1]], 5)
    else:
        imm = getImmediate(registers[1])
        rs1 = getRegVal(registers[1])
    func3 = toBin(ops[1],3)
    rd = toBin(reg_conv[registers[0]],5)
    opcode = toBin(ops[0], 7) 
    return  imm + rs1 + func3 + rd + opcode

def make_b(ops, registers, labels, pc):
    global line
    registers = registers.split(',')
    opcode = toBin(ops[0], 7) 
    func3 = toBin(ops[1], 3)
    rs1 = toBin(reg_conv[registers[0]], 5)
    rs2 = toBin(reg_conv[registers[1]], 5)
    try:
        imm = toBin(int(registers[2]), 12)
    except:
        val = registers[2]
        if val not in labels:
            print(f'label not found - {val}')
            print(f'labels - {labels}')
            raise TypeError('Using undefined label')
        imm = toBin(labels[val]-pc, 12)
    outval = imm[11] + imm[9:3:-1] + rs2 + rs1 + func3 + imm[3::-1]+ imm[10] + opcode
    return outval

def make_s(ops, registers):
    registers = registers.split(',')
    opcode = toBin(ops[0], 7)
    func3 = toBin(ops[1], 3)
    rs2 = toBin(reg_conv[registers[0]], 5)
    try:
        rs1 = toBin(reg_conv[registers[1]], 5)
    except:
        imm = getImmediate(registers[1])
        rs1 = getRegVal(registers[1])
    return imm[:7] + rs2 + rs1 + func3 + imm[7:] + opcode

def make_j(ops, registers, labels, pc):
    registers = registers.split(',')
    opcode = toBin(ops[0],7)
    rd = toBin(reg_conv[registers[0]],5)
    try:
        val = int(registers[1])
        imm = toBin(val,21)
    except:
        val = registers[1]
        if val not in labels:
            print(val)
            raise TypeError('label')
        imm = toBin(labels[val]-pc,21)
    return imm[20] + imm[10:0:-1][1:] + imm[11] + imm[19:11:-1] + rd + opcode

def transl(ins, labels, pc):
    global prg_counter, line
    prg_counter = pc
    line = " ".join(ins)
    cmd = ins[0]
    try:
        if cmd in r_type:
            return make_r(r_type[cmd], ins[1])
        if cmd in i_type:
            return make_i(i_type[cmd], ins[1])
        if cmd in b_type:
            return make_b(b_type[cmd], ins[1], labels, pc)
        if cmd in s_type:
            return make_s(s_type[cmd], ins[1])
        if cmd in j_type:
            return make_j(j_type[cmd], ins[1], labels, pc)
    except:
        error(pc, line, "Register not found")
    
if __name__=='__main__':
    #           tests
    print(f"binary of 421: {toBin(421)}")
    print(transl(['add', 'ra,sp,gp'], {}, 0))
    print(transl(['lw', 't0,32(gp)'], {}, 0))
    print(transl(['lw', 't0,gp,32'], {}, 0))
    print(transl(['bne', 'a0,a3,-8'], {}, 0))
    print(transl(['blt', 'a0,a3,start'], {'start': 0}, 8))
    print(transl(['sw', 'ra,32(sp)'],{},0))

