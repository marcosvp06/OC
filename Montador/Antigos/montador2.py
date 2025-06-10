import sys

# "INSTR" : [binary_instr0000, second byte, RegA, RegB]
instructions = {
    "ADD": [0b10000000, 0, 1, 1],
    "SHR": [0b10010000, 0, 1, 1],
    "SHL": [0b10100000, 0, 1, 1],
    "NOT": [0b10110000, 0, 1, 1],
    "AND": [0b11000000, 0, 1, 1],
    "OR" : [0b11010000, 0, 1, 1],
    "XOR": [0b11100000, 0, 1, 1],
    "CMP": [0b11110000, 0, 1, 1],

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

def is_jcaez(i):
    caez = 0b0000
    auxCaez = ['C', 'A', 'E', 'Z']

    if i[0] != 'J' or i in instructions:
        return 0b0000
    
    for x in range(1, len(i)):
        if i[x] in jcaez:
            if i[x] in auxCaez:
                auxCaez.remove(i[x])
                caez += jcaez[i[x]]
            else:
                raise ValueError(f"Flag repetida em '{i}'!")
        else:
            raise ValueError(f"Flag invalida '{i[x]}' em '{i}'!")
    return caez

if len(sys.argv) != 3:
    print("Uso: python3 script.py <entrada> <saida>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(output_file, "r") as input, open(output_file, "wb") as output:
    for lineno, line in enumerate(input, start=1):
        try:
            parts = line.strip().split()
            if not parts:
                continue

            instr = parts[0]

            caezBin = is_jcaez(instr)
            if caezBin:
                instr = "JCAEZ"

            if instr not in instructions:
                raise ValueError(f"Instrucao invalida '{instr}' na linha {lineno}")

            binary = instructions[instr][0] + caezBin
            is_2bytes = instructions[instr][1]
            is_ra = instructions[instr][2]
            is_rb = instructions[instr][3]
            raStr, rbStr = "", ""

            i = 1

            if is_ra:
                if i >= len(parts):
                    raise ValueError(f"Esperado registrador RA apos '{instr}' na linha {lineno}")
                raStr = parts[i]
                if raStr not in registers:
                    raise ValueError(f"Registrador invalido '{raStr}' na linha {lineno}")
                raBin = registers[raStr]
                binary += raBin << 2
                i += 1

            if is_rb:
                if i >= len(parts):
                    raise ValueError(f"Esperado registrador RB após '{raStr}' na linha {lineno}")
                rbStr = parts[i]
                if rbStr not in registers:
                    raise ValueError(f"Registrador inválido '{rbStr}' na linha {lineno}")
                rbBin = registers[rbStr]
                binary += rbBin
                i += 1

            output.write(binary.to_bytes(1, byteorder='big'))

            if is_2bytes:
                if i >= len(parts):
                    raise ValueError(f"Esperado argumento adicional (endereço/dado) após '{instr}' na linha {lineno}")
                addr = parts[i]
                try:
                    binary = int(addr)
                except ValueError:
                    raise ValueError(f"Endereco/Dado invalido '{addr}' na linha {lineno}")
                if not (0 <= binary <= 255):
                    raise ValueError(f"Valor fora do intervalo (0–255): '{addr}' na linha {lineno}")
                output.write(binary.to_bytes(1, byteorder='big'))
                i += 1

            if i != len(parts):
                raise ValueError(f"Argumentos extras apos instrucao '{instr}' na linha {lineno}")

        except ValueError as e:
            print(f"[ERRO] {e}")