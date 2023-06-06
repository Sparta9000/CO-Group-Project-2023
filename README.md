# CO-Group-Project-2023

Kuvam (2022264)
Lakshay Kumar (2022266)
Manan Aggarwal (2022273)
Manan Kadecha (2022274)

## Assembler
The assembler takes input from stdin and output to stdout.
In case of an error the assembler tells the line at which the error occured and relevent message for the error.

The assembler takes care of all the commands provided, converts the register to the corresponding binary value, assigns binary to labels and variables and Then uses them to generate the binary 

## Simulator
The simulator takes input from stdin and output to stdout.
It runs all the lines in a given program and prints the PC and all registers
After the halt statement it dumps all the values stored in memory to stdout.

## Bonus commands
| Opcode | Instruction | Semantics | Syntax | Type |
| --- | --- | --- | --- | --- |
| 10011 | Modulus | Performs reg1 = reg1 % reg2 | mod reg1 reg2 | C |
| 10100 | Power | Performs reg1 = reg2 ^ reg3 | pow reg1 reg2 reg3 | A |
| 10101 | No Operation | Resets FLAGS register | NOP | F |
| 10110 | Arithmetic Shift Left | Shifts bits of reg1 towards left and adds $Imm bit. Imm only takes values of 0 or 1 | asl reg1 $Imm | B |
| 10111 | Arithmetic Shift Right | Shifts bits of reg1 towards Right and adds $Imm bit. Imm only takes values of 0 or 1 | asr reg1 $Imm | B |