import sys

def bin_num(num, digits=16):
    x = str(bin(num))[2:]
    while len(x) != digits:
        x = '0' + x
    return x

def dump():
    s = bin_num(pc, 7) + "        "
    for i in register:
        s += bin_num(register[i]) + " "
    s = s[:-1]
    print(s)
    
def mem_dump():
    for i in lines:
        if "\n" in i:
            print(i[:-1])
        else:
            print(i)

    start = len(lines)
    while start in memory:
        print(bin_num(memory[start]))
        start += 1

    for i in range(start, 128):
        print("0"*16)

def convert_float(num):
    exp = to_num(num[:3]) - 3
    b = num[3:]
    a = "1"

    t = len(a) + exp - 1
    k = 0.0
    for i in a+b:
        k += (2**t)*int(i)
        t -= 1
    return k

def to_num(b):
    return int(b, 2)

def init_memory(mem):
    memory[mem] = 0

# with open("input.txt") as f:
#     lines = f.readlines()

lines = list(sys.stdin)

pc = 0
register = {"000": 0,
            "001": 0,
            "010": 0,
            "011": 0,
            "100": 0,
            "101": 0,
            "110": 0,
            "111": 0}
memory = {}
halted = False
MAX_INT = 65535

while not halted:
    line = lines[pc]
    instruction = line[:5]
    new_pc = pc + 1

    if instruction == "11010":
        halted = True

    elif instruction in ["00000", "00001", "00110", "01010", "01011", "01100", "10100"]:
        r1 = line[7:10]
        r2 = line[10:13]
        r3 = line[13:16]
        register["111"] = 0

        if instruction == "00000":
            x = register[r2] + register[r3]
        elif instruction == "00001":
            x = register[r2] - register[r3]
        elif instruction == "00110":
            x = register[r2] * register[r3]
        elif instruction == "01010":
            x = register[r2] ^ register[r3]
        elif instruction == "01011":
            x = register[r2] | register[r3]
        elif instruction == "01100":
            x = register[r2] & register[r3]
        elif instruction == "10100":
            x = register[r2] ** register[r3]

        if x > MAX_INT or x < 0:
            register["111"] = bin_num(8)
            x = 0

        register[r1] = x
    
    elif instruction in ["00010", "01000", "01001", "10110", "10111"]:
        r = line[6:9]
        val = to_num(line[9:16])
        
        if instruction == "01000":
            val = register[r] >> val
        elif instruction == "01001":
            val = register[r] << val
        elif instruction == "10110":
            val = (register[r] << 1) + val
        elif instruction == "10111":
            val = (register[r] >> 1) + (val*(2**len(bin(register[r])-3)))

        register[r] = val
        
    elif instruction in ["00011", "00111", "01101", "01110", "10011"]:
        r1 = line[10:13]
        r2 = line[13:16]

        if instruction == "00011":
            register[r1] = register[r2]
            register["111"] = 0
        elif instruction == "10011":
            register[r1] %= register[r2]
            register["111"] = 0
        elif instruction == "000111":
            if register[r2] == 0:
                register['000'] = 0
                register['001'] = 0
                register['111'] = 8
            else:
                register['000'] = register[r1] // register[r2]
                register['001'] = register[r1] % register[r2]
                register["111"] = 0
        elif instruction == "01101":
            register[r1] = ~register[r2]
            register["111"] = 0
        else:
            if register[r1] > register[r2]:
                register['111'] = 2
            elif register[r1] < register[r2]:
                register['111'] = 4
            else:
                register['111'] = 1
        
    elif instruction in ["00100", "00101"]:
        r = line[6:9]
        mem = to_num(line[9:16])
        register["111"] = 0

        if mem not in memory:
            init_memory(mem)
        
        if instruction == "00100":
            register[r] = memory[mem]
        else:
            memory[mem] = register[r]

    elif instruction in ["01111", "11100", "11101", "11111"]:
        mem = to_num(line[9:16])

        if instruction == "01111":
            new_pc = mem
        elif instruction == "11100":
            if register['111'] == 4:
                new_pc = mem
        elif instruction == "11101":
            if register['111'] == 2:
                new_pc = mem
        else:
            if register['111'] == 1:
                new_pc = mem
        
        register["111"] = 0

    elif instruction == "10101":
        register["111"] = 0
        

    dump()
    pc = new_pc

mem_dump()