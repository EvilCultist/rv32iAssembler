
r_type = {
# instruction:  opcode  f3   f7
        "add": [ 51,     0,   0  ], 
        "sub": [ 51,     0,   32 ],  
        "slt": [ 51,     2,   0  ], 
        "srl": [ 51,     0,   0  ], 
        "or" : [ 51,     5,   0  ], 
        "and": [ 51,     7,   0  ], 
}

i_type = {
# instruction:   opcode  f3
        "lw"  : [ 3,     2 ], 
        "addi": [ 19,    0 ],  
        "jalr": [ 103,   0 ], 
}

b_type = {
# instruction:   opcode  f3
        "beq" : [ 99,     0 ], 
        "bne" : [ 99,     1 ],  
        "blt" : [ 99,     4 ], 
}

s_type = {
# instruction:   opcode  f3
    "sw": [ 35,     2 ],
    }

reg_conv = {
        "zero": 0,
        "ra": 1,
        "sp": 2,
        "gp": 3,
        "tp": 4,
        "t0": 5,
        "t1": 6,
        "t2": 7,
        "s0": 8,
        "fp": 8,
        "s1": 9,
}

for i in range(0,8):
    reg_conv['a'+str(i)] = 10 + i - 0
for i in range(2,12):
    reg_conv['s'+str(i)] = 18 + i - 2
for i in range(3,7):
    reg_conv['t'+str(i)] = 28 + i - 3


funcs = list(r_type.keys()) + list(i_type.keys()) + list(b_type.keys()) + list(s_type.keys())

if __name__=='__main__':
    print(funcs)
    print('\n\n ' + 10*'-' + ' \n\n')
    print(*reg_conv, sep='\n')

