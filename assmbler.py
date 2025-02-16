from instructions import funcs, b_type, r_type, i_type, s_type, j_type
from torv32i import transl

inpPath = "input.txt"
outPath = "output.txt"

outFile = ""

labels={}

def main():
    try:
        with open(inpPath, 'r') as f:
            lines = f.readlines()
    except:
        error('file bot found\n'+f'please write input to {inpPath}')

    out = []
    pc = -1
    for line in lines:
        pc+=1
        ops = line.split()
        # print(*ops, sep=' - ')
        if ops[0][-1] == ':' and ops[0][0].isalnum:
            labels[ops[0][:-1:1]] = pc
            ops = ops[1:]
        if ops[0] not in funcs: 
            error(f'unknown operation on line : {pc}')
        out.append(transl(ops, labels, pc))
    print(*out, sep='\n')


def error(mssg):
    print('\n\n ---- ERROR ---- ')
    print(mssg)

def writeToDisk():
    with open(outPath, 'w') as f:
        f.write(outFile)

if __name__=='__main__':
    main()

