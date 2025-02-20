from instructions import funcs, b_type, r_type, i_type, s_type, j_type
from torv32i import transl, error
from sys import argv

inpPath = "input.txt"
outPath = "output.txt"

virtual_halt = '00000000000000000000000001100011'

outFile = ""

labels={}

def main():
    if len(argv) != 3:
        print_help()
        exit()
    else:
        inpPath = argv[1]
        outPath = argv[2]
    try:
        with open(inpPath, 'r') as f:
            lines = f.readlines()
    except:
        error('file bot found\n'+f'please write input to {inpPath}')

    out = []
    pc = -1
    for i, line in enumerate(lines):
        pc+=1
        if line == '':
            continue
        ops = line.split()
        # print(*ops, sep=' - ')
        if len(ops) > 3:
            error(pc, line, f'Too many arguments,\nexpected at most 3, got {len(ops)}')
        if ops[0][-1] == ':' and ops[0][0].isalnum:
            if not ops[0][0].isalpha():
                error(pc, line, f'Label doesn\'t start with a letter')
            labels[ops[0][:-1:1]] = pc
            ops = ops[1:]
        if ops[0] not in funcs: 
            if len(ops) == 3:
                error(pc, line, f'Label is missing semicolon: {ops[0]}')
            error(pc, line, f'Instruction not found: {ops[0]}')
        if ops[0] == 'halt':
            out.append(virtual_halt)
        elif ops[0] == 'rst':
            out.append(transl(['addi', 'x0,x0,0'], labels, pc))
        else:
            # print(*ops, sep=' - ')
            out.append(transl(ops, labels, pc))
        if out[-1] == virtual_halt and i!=(len(lines)-1):
            error(pc, line, 'virtual halt before eof')
    if out[len(out)-1] != virtual_halt:
        error(pc, line, 'last instruction is not virtual halt')
    print(*out, sep='\n')
    with open(outPath, 'w') as f:
        f.write('\n'.join(out))

def print_help():
    print("\n\nusage:  python3 program [input_path] [output_path]\n\n")

def writeToDisk():
    with open(outPath, 'w') as f:
        f.write(outFile)

if __name__=='__main__':
    main()

