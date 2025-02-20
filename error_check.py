def check_instruction(instruction):
    valid = {"add", "sub", "slt", "srl", "or", "and", "lw", "addi", "jalr", "sw", "beq", "bne", "jal"}
    return "Valid" if instruction.split()[0] in valid else f"Error: Invalid instruction '{instruction}'"

def check_register(register):
    valid = {f"x{i}" for i in range(32)}
    return "Valid" if register in valid else f"Error: Invalid register '{register}'"

def check_virtual_halt(instructions):
    if instructions.count("beq x0, x0, 0x00000000") != 1:
        return "Error: Invalid Virtual Halt"
    return "Valid" if instructions[-1] == "beq x0, x0, 0x00000000" else "Error: Virtual Halt not last"

def check_immediate(immediate):
    try:
        return "Valid" if -2048 <= int(immediate, 0) <= 2047 else f"Error: Immediate '{immediate}' out of range"
    except ValueError:
        return f"Error: Invalid immediate '{immediate}'"

def check_labels(instructions):
    labels = {line.split(":")[0] for line in instructions if ":" in line}
    for instr in instructions:
        words = instr.split()
        if words[0] in {"jal", "beq", "bne"} and words[-1] not in labels:
            return "Error: Label not found"
    return "Valid"

def run_tests():
    instr_tests = ["add x1, x2, x3", "mul x4, x5, x6", "invalid_instr x1, x2, x3"]
    reg_tests = ["x0", "x32", "a1"]
    imm_tests = ["1024", "-3000", "abcd"]
    prog_tests = [
        ["addi x1, x2, 10", "lw x3, 0(x4)", "beq x0, x0, 0x00000000"],
        ["addi x1, x2, 10", "lw x3, 0(x4)"]
    ]
    
    results = [check_instruction(i) for i in instr_tests]
    results += [check_register(r) for r in reg_tests]
    results += [check_immediate(i) for i in imm_tests]
    results += [check_virtual_halt(p) for p in prog_tests]
    results.append(check_labels(prog_tests[0]))
    
    return results

if __name__ == "__main__":
    for result in run_tests():
        print(result)
