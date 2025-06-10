# "INSTR" : [binary_instr0000, second byte?, RegA?, RegB?]
instructions = {
    "ADD":   [0b10000000, 0, 1, 1],
    "SHR":   [0b10010000, 0, 1, 1],
    "SHL":   [0b10100000, 0, 1, 1],
    "NOT":   [0b10110000, 0, 1, 1],
    "AND":   [0b11000000, 0, 1, 1],
    "OR" :   [0b11010000, 0, 1, 1],
    "XOR":   [0b11100000, 0, 1, 1],
    "CMP":   [0b11110000, 0, 1, 1],
    "LD":    [0b00000000, 0, 1, 1],
    "ST":    [0b00010000, 0, 1, 1],
    "DATA":  [0b00100000, 1, 0, 1],
    "JUMPR": [0b00110000, 0, 0, 1],
    "JUMP":  [0b01000000, 1, 0, 0],
    "JCAEZ": [0b01010000, 1, 0, 0],
    "CLF":   [0b01100000, 0, 0, 0],
    "IN":    [0b01110000, 0, 1, 0],
    "OUT":   [0b01111000, 0, 1, 0]
}

# "REG" : Addr
registers = {
    "R0" : 0b00,
    "R1" : 0b01,
    "R2" : 0b10,
    "R3" : 0b11
}

jcaez = {
    'C' : 0b1000,
    'A' : 0b0100,
    'E' : 0b0010,
    'Z' : 0b0001
}

inOut = {
    "ADDR" : 0b100,
    "DATA" : 0b000
}

def is_jcaez(i):
    caez = 0b0000
    auxCaez = ['C', 'A', 'E', 'Z']

    if i[0] != 'J' or i in instr:
        return 0b0000
    
    for x in range(1, len(i)):
        if i[x] in jcaez:
            auxCaez.remove(i[x])
            caez += jcaez[i[x]]
        else:
            raise ValueError("Entrada invalida!")
    return caez


#main do montador

with open("input.ldc", "r") as input, open("output.bin", "wb") as output:
    for line in input:
        parts = line.strip().split()
        instr = parts[0]

        caezBin = is_jcaez(instr)
        if caezBin:
            instr = "JCAEZ"

        if instr in instructions:

            binary = instructions[instr][0] + caezBin
            is_2bytes = instructions[instr][1]
            is_ra = instructions[instr][2]
            is_rb = instructions[instr][3]
            i = 1
        #else: error

            if is_ra:
                raStr = parts[i]
                #if raStr not in registers: error
                raBin = registers[raStr]
                binary += raBin<<2
                i += 1

            #if is_in_out

            if is_rb:
                rbStr = parts[i]
                #if rbStr not in registers: error
                rbBin = registers[rbStr]
                binary += rbBin
                i += 1

            output.write(binary.to_bytes(1, byteorder='big'))

            if is_2bytes:
                addr = parts[i]
                binary = int(addr)
                #if binary > 255 or binary < 0: error
                i += 1
                output.write(binary.to_bytes(1, byteorder='big'))

        #if i != len(parts): error