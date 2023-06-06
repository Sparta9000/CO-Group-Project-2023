import sys

def bin_num(num, digits=16):
    if (type(num) == float):
        x = convert_float_8bit(num)
    else:
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

def format(num, n):
    x = bin(int(num))[2:]
    
    while len(x) != n:
        x = "0" + x
    
    return x

def convert_float_8bit(num):
    whole, dec = str(num).split(".")
    whole = bin(int(whole))[2:]
    t = ""
    dec = float(f"0.{dec}")

    for _ in range(9):
        t += str(int(dec*2))
        dec *= 2
        dec = dec - int(dec)

    c = 0
    if whole == "0":
        if float(num) != 0:
            while t[0] != "1" and c >= -3:
                c -= 1
                t = t[1:]
            c -= 1
            t = t[1:]
    elif float(num) != 0:
        while whole != "1":
            t = whole[-1] + t
            whole = whole[:-1]
            c += 1

    exp = format(3+c, 3)
    return str(exp) + t[:5]

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
            register["111"] = 8
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
            val = (register[r] >> 1) + (2**15)

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

    elif instruction == "10010":
        register["111"] = 0
        r = line[5:8]
        val = convert_float(line[8:16])
        register[r] = val

    elif instruction in ["10000", "10001"]:
        r1 = line[7:10]
        r2 = line[10:13]
        r3 = line[13:16]
        register["111"] = 0

        if instruction == "10000":
            t = register[r2] + register[r3]
        if instruction == "10001":
            t = register[r2] - register[r3]

        if not (0.125 <= t <= 31.5):
            register["111"] = 8
            t = 0

        register[r1] = t

    dump()
    pc = new_pc

mem_dump()