# -- A16 Simulator --
# Author: Isacc Rojas
# Simulates the "A16" variable-"acculumator" based instruction set architecture. Details:
# - 8 general purpose registers
# - 16 instructions
# - dedicated PC value storage register
# - 128 memory addresses
# - immediate range of [-4, 3]

mem = [0] * 128         # initialize memory contents
registers = [0] * 8     # initialize general-purpose register contents
active_reg = 0
program_reg = 0
PC = 0
InstrCount = 0

def SAR(oper:int):  # SAR: sets active register.
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0):
        return -1
    active_reg = oper
    return 0

def ADD(oper:int):  # ADD: Ra = Ra + Rs
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0):
        return -1
    registers[active_reg] = registers[active_reg] + registers[oper]
    return 0

def MOV(oper:int):  # MOV: Ra = Rs
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0):
        return -1
    registers[active_reg] = registers[oper]
    return 0

def NAND(oper:int): # NAND: Ra = ~(Ra & Rs)
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0):
        return -1
    registers[active_reg] = ~(registers[active_reg] & registers[oper])
    return 0

def SLL(oper:int): # SLL: Ra = Ra << Rs
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0 or registers[oper] < 0):
        return -1
    registers[active_reg] = registers[active_reg] << registers[oper]
    return 0

def SRL(oper:int): # SRL: Ra = Ra >> Rs
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0 or registers[oper] < 0):
        return -1
    registers[active_reg] = registers[active_reg] >> registers[oper]
    return 0

def LOAD (oper:int): # LOAD: Ra = mem[Rs]
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0 or registers[oper] > 127 or registers[oper] < 0):
        return -1
    registers[active_reg] = mem[registers[oper]]
    return 0

def STOR (oper:int): # STOR: mem[Rs] = Ra
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0 or registers[oper] > 127 or registers[oper] < 0):
        return -1
    mem[registers[oper]] = registers[active_reg]
    return 0

def SUB(oper:int): # SUB: Ra = Ra - Rs
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0):
        return -1
    registers[active_reg] = registers[active_reg] - registers[oper]
    return 0

def MLT(oper:int): # MLT: Ra = Ra * Rs
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0):
        return -1
    registers[active_reg] = registers[active_reg] * registers[oper]
    return 0

def BSLT(oper:int): # BSLT: if (Ra < Rs) then PC = Rp
    global active_reg
    global program_reg
    global PC
    if (oper > 7 or oper < 0):
        return -1
    PC = program_reg if (registers[active_reg] < registers[oper]) else PC
    return 0

def MOVI(oper:int): # MOVI: Ra = imm
    global active_reg
    global program_reg
    global PC
    if (oper > 3):
        oper = oper - 8
    if (oper > 3 or oper < -4):
        return -1
    registers[active_reg] = oper
    return 0

def ADDI(oper:int): # ADDI: Ra = Ra + imm
    global active_reg
    global program_reg
    global PC
    if (oper > 3):
        oper = oper - 8
    if (oper > 3 or oper < -4):
        return -1
    registers[active_reg] = registers[active_reg] + oper
    return 0

def SPC(oper:int): # Rp = PC + Rs
    global program_reg
    global PC
    if (oper > 7 or oper < 0):
        return -1
    program_reg = PC + registers[oper]
    return 0

def B(oper:int): # PC = Rp
    global program_reg
    global PC
    PC = program_reg
    return 0

def STOP(oper:int): # Stops execution.
    return 0

op_to_instr = {
    '0000': 'SAR',
    '0001': 'ADD',
    '0010': 'MOV',
    '0011': 'NAND',
    '0100': 'SLL',
    '0101': 'SRL',
    '0110': 'LOAD',
    '0111': 'STOR',
    '1000': 'SUB',
    '1001': 'MLT',
    '1010': 'BSLT',
    '1011': 'MOVI',
    '1100': 'ADDI',
    '1101': 'SPC',
    '1110': 'B',
    '1111': 'STOP'
}
    
instr_op = { # define hash table with instruction
    'SAR': SAR,
    'ADD': ADD,
    'MOV': MOV,
    'NAND': NAND,
    'SLL': SLL,
    'SRL': SRL,
    'LOAD': LOAD,
    'STOR': STOR,
    'SUB': SUB,
    'MLT': MLT,
    'BSLT': BSLT,
    'MOVI': MOVI,
    'ADDI': ADDI,
    'SPC': SPC,
    'B': B,
    'STOP': STOP
}
instr_op_desc = { # define hash table with instruction descriptions
    'SAR': 'select ra',
    'ADD': 'ra = ra + rs',
    'MOV': 'ra = rs',
    'NAND': 'ra = ~(ra&rs)',
    'SLL': 'ra = ra << rs',
    'SRL': 'ra = ra >> rs',
    'LOAD': 'ra = mem[rs]',
    'STOR': 'mem[rs] = ra',
    'SUB': 'ra = ra - rs',
    'MLT': 'ra = ra * rs',
    'BSLT': 'ra<rs ->PC=rp',
    'MOVI': 'ra = imm',
    'ADDI': 'ra = ra + imm',
    'SPC': 'rp = PC + rs',
    'B': 'PC = rp',
    'STOP': 'stop running'
}



with open("A16_example4_bin.txt", "r") as file:                 # open file and memory with guard
    with open("A16_example4_mem.txt", "r") as memory:           # load memory into local "stack"
        memorylines = memory.read().splitlines()                # separate each index into lines
        if (len(memorylines) < 128 or len(memorylines) > 128):  # if size is improper, use "default" 0 memory
            print("MEMORY ERROR: size is not 128. Using memory initialized to all 0.")
            mem = [0] * 128
        else:   # load memory
            n = 0
            for memoryline in memorylines:
                if (n < 128):
                    mem[n] = int(memoryline)
                n = n + 1
    filelines = file.read().splitlines()        # separate file into list of lines to iterate through it
    while (PC < len(filelines)):                # execute while PC is in range or STOP instruction is reached
        line = filelines[PC]                    # separate line into instructions and parameters
        if (op_to_instr[line[0:4]] == "STOP"):  # stop if STOP
            print("STOP instruction reached.")
            break
        elif (line[0:4] not in op_to_instr):    # stop if instruction is invalid
            print("ERROR: instruction '" + line[0:4] + "' not recognized. Ending execution.")
            break
        else:
            if (instr_op[op_to_instr[line[0:4]]](int(line[4:8], 2)) == -1):   # execute instruction with parameter; stop if parameter out of range
                print("ERROR: operand out of range for '" + op_to_instr[line[0:4]] + " " + str(int(line[4:8], 2)) + "'. Ending execution.")
                break
        PC = PC + 1                                     # increment PC
        InstrCount = InstrCount + 1                     # increment instruction count limit
        if (filelines[len(filelines) - 1] == "debug"):  # debug mode: dumps register file contents and special registers during execution
            Str = ""                                    # prepare parameter string if instruction has one, and print information
            if (line[0:4] != '1110' and line[0:4] != '1111'):
                n = int(line[4:8], 2)
                if ((line[0:4] == '1011' or line[0:4] == '1100') and (n > 3)):
                    n = n - 8
                Str = " " + str(n)
            print(op_to_instr[line[0:4]] + Str + " \t| " + instr_op_desc[op_to_instr[line[0:4]]] + "\t| reg. file = ", registers, " Ra = " + str(active_reg) + ", Rp = " + str(program_reg) + ",\t PC = " + str(PC))
        if (InstrCount > 1024):  # stop if instruction count limit reached
            print("ERROR: instruction count limit of " + str(InstrCount - 1) + " exceeded.")
            break
    with open("A16_example4_mem.txt", "w") as memory:   # store memory into file
        n = 0
        for memval in mem:
            if (n < 128):
                memory.write(str(memval) + '\n')
            n = n + 1
