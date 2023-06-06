import sys

output = ""

vars = []
vars_done = False
labels = {}

commands = ["add", "sub", "movimm", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "addf", "subf", "movf", "mod", "pow", "nop", "asl", "asr", "jlt", "jgt", "je", "hlt"]

def check_3_reg(line):
    return len(line) == 4

def check_2_reg(line):
    return len(line) == 3

def check_1_reg(line):
    return len(line) == 2

def is_register(r):
    if len(r) != 2:
        return False
    if r[0] != "R":
        return False
    if "0" <= r[1] <= "6":
        return True
    
def to_register(r):
    if r == "FLAGS":
        error(counter, "invalid use of flags register")
    if not is_register(r):
        error(counter, "Invalid register name")
    return format(r[1], 3)

def valid_var(var):
    return var in vars

def to_address(var):
    if var in labels:
        error(counter, f"{var} is a label not a variable")
    if not valid_var(var):
        error(counter, "undefined variable")
    return format(offset + vars.index(var), 7)

def format(num, n):
    x = bin(int(num))[2:]

    if len(x) > n:
        error(counter, "out of range")
    
    while len(x) != n:
        x = "0" + x
    
    return x

def convert_float_8bit(num):
    try:
        if float(num) >= 32:
            error(counter, "out of range float")
    except:
        error(counter, "floating point number expected")

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
    
    if (c < -3) or (c > 7):
        error(counter, "out of range")

    exp = format(3+c, 3)
    return str(exp) + t[:5]

def error(counter, message):
    print(f"error at line {counter}: {message}")
    exit()

hlt = False

lines = list(sys.stdin)

to_remove = []
counter = 0
for i in range(len(lines)):
    line = lines[i]
    line = line.strip()
    if line == "":
        continue
    if ":" in line:
        t = line.split(":")
        if t[0].count(" ") > 0:
            error(counter, "Invalid label name")
        if t[1] != "":
            labels[t[0]] = format(counter, 7)
            lines[i] = t[1]
        else:
            labels[t][0] = format(counter+1, 7)
            to_remove.append(i)
            continue
    if line.split()[0] == "var":
        continue
    counter += 1

counter = 0
for k in range(len(lines)):
    line = lines[k]
    counter += 1
    line = line.strip()
    if line == "":
        continue

    if k in to_remove:
        continue
    
    line = line.split()

    if not vars_done:
        if line[0] == "var":
            vars.append(line[1])
            continue
        else:
            vars_done = True
            offset = len(lines) - len(vars)

    if line[0] == "var":
        error(counter, "declaration of variable after start of program")

    elif line[0] == "hlt":
        if not hlt:
            hlt = True
            output += "1101000000000000"
            continue
    if hlt:
        error(counter, "commands after hlt")
    
    elif line[0] in ("add", "sub", "mul", "xor", "or", "and", "addf", "subf", "pow"):
        if not check_3_reg(line):
            error(counter, "wrong number of arguments")
        output += format(commands.index(line[0]), 5) + "00"
        output += to_register(line[1])
        output += to_register(line[2])
        output += to_register(line[3])

    elif line[0] == "mov":
        if len(line) != 3:
            error(counter, "Wrong number of arguments")
        elif "$" in line[2]:
            output += "00010" + "0"
            output += to_register(line[1])
            output += format(int(line[2][1:]), 7)
        
        else:
            if not check_2_reg(line):
                error(counter, "wrong number of arguments")
            output += format(commands.index(line[0]), 5) + "00000"
            output += to_register(line[1])
            if line[2] == "FLAGS":
                output += "111"
            else:
                output += to_register(line[2])

    elif line[0] in ("div", "not", "cmp", "mod"):
        if not check_2_reg(line):
            error(counter, "wrong number of arguments")
        output += format(commands.index(line[0]), 5) + "00000"
        output += to_register(line[1])
        output += to_register(line[2])

    elif line[0] in ("ld", "st"):
        if not check_2_reg(line):
            error(counter, "wrong number of arguments")
        output += format(commands.index(line[0]), 5) + "0"
        output += to_register(line[1])
        output += to_address(line[2])

    elif line[0] in ("rs", "ls"):
        if not check_2_reg(line):
            error(counter, "wrong number of arguments")
        output += format(commands.index(line[0]), 5) + "0"
        output += to_register(line[1])
        if "$" not in line[2]:
            error(counter, "General Syntax Error")
        output += format(int(line[2][1:]), 7)

    elif line[0] == "movf":
        if len(line) != 3:
            error(counter, "invalid number of arguments")
        output += format(commands.index(line[0]), 5)
        output += to_register(line[1])
        if not "$"in line[2]:
            error(counter, "invalid format")
        output += convert_float_8bit(line[2][1:])

    elif line[0] in ("jmp", "jlt", "jgt", "je"):
        if not check_1_reg(line):
            error(counter, "wrong number of arguments")

        if line[0] == "jmp":
            output += "01111"
        elif line[0] == "jlt":
            output += "11100"
        elif line[0] == "jgt":
            output += "11101"
        elif line[0] == "je":
            output += "11111"

        output += "0000"
        if line[1] in vars:
            error(counter, f"{line[1]} is a variable not a label")
        if line[1] not in labels:
            error(counter, "undefined label")
        output += labels[line[1]]

    elif line[0] == "nop":
        if (len(line) != 1):
            error(counter, "invalid number of arguments")
        output += format(commands.index(line[0]), 5) + "00000000000"

    elif line[0] in ("asl", "asr"):
        if not check_2_reg(line):
            error(counter, "Wrong number of arguments")
        output += format(commands.index(line[0]), 5) + "0"
        output += to_register(line[1])
        if line[2][0] != "$":
            error(counter, "expected a decimal value")
        if int(line[2][1:]) not in (0, 1):
            error(counter, "immediate value out of range")
        output += format(int(line[2][1:]), 7)

    else:
        error(counter, "not a valid instruction")

    output += "\n"

if not hlt:
    error(counter, "No hlt in code.")

print(output)