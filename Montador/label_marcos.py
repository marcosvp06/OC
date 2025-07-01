# Autor: Marcos Paulo Vieira Pedrosa
# Matricula: 22401906

import sys, os
from dataclasses import dataclass

@dataclass
class Instruction:
    opcode: int
    has_ra: bool
    has_rb: bool
    has_2bytes: bool

Instructions = {
    "ADD":   Instruction(0x80, True, True, False),
    "SHR":   Instruction(0x90, True, True, False),
    "SHL":   Instruction(0xA0, True, True, False),
    "NOT":   Instruction(0xB0, True, True, False),
    "AND":   Instruction(0xC0, True, True, False),
    "OR" :   Instruction(0xD0, True, True, False),
    "XOR":   Instruction(0xE0, True, True, False),
    "CMP":   Instruction(0xF0, True, True, False),
    "LD":    Instruction(0x00, True, True, False),
    "ST":    Instruction(0x10, True, True, False),
    "DATA":  Instruction(0x20, False, True, True),
    "JMPR":  Instruction(0x30, False, True, False),
    "JMP":   Instruction(0x40, False, False, True),
    "JCAEZ": Instruction(0x50, False, False, True),
    "CLF":   Instruction(0x60, False, False, False),
    "IN":    Instruction(0x70, False, True, False),
    "OUT":   Instruction(0x78, False, True, False)
}

registers = {"R0": 0b00, "R1": 0b01, "R2": 0b10, "R3": 0b11}
jcaez = {'C': 0b1000, 'A': 0b0100, 'E': 0b0010, 'Z': 0b0001}

def preProcess(input_lines, labels):
    output_line = 0
    lineno = 0
    for lineno, line in enumerate(input_lines, start=1):
        line = line.split(";")[0].strip()
        aux_line = line.split(":")
        if len(aux_line) == 2:
            label = aux_line[0].strip()
            if label and label not in labels:
                labels[label.upper()] = output_line
        line = aux_line[-1].replace(",", " ").strip()
        input_lines[lineno-1] = line
        parts = [x.strip().upper() for x in line.split()]
        if not parts:
            continue
        output_line += 1
        if parts[0].startswith("J") or parts[0] in Instructions and Instructions[parts[0]].has_2bytes:
            output_line += 1
    return lineno

def assemble(input_lines, labels, fout):
    for lineno, line in enumerate(input_lines, start=1):
        parts = [x.strip().upper() for x in line.split()]
        if not parts:
            continue
        result = ra = rb = 0
        hex_addr = ""
        pos = 1

        if parts[0][0] == "J" and parts[0] not in ["JMP", "JMPR"]:
            for ch in parts[0][1:]:
                result += jcaez[ch]
            parts[0] = "JCAEZ"

        if parts[0] in ["IN", "OUT"]:
            if parts[1] == "ADDR":
                result += 4
            pos += 1

        instr = Instructions[parts[0]]

        if instr.has_ra:
            ra = registers[parts[pos]]
            pos += 1
        if instr.has_rb:
            rb = registers[parts[pos]]
            pos += 1

        result += instr.opcode + 4*ra + rb
        hex_result = f"{result:02X}"

        if instr.has_2bytes:
            if parts[-1] in labels:
              parts[-1] = f"0X{labels[parts[-1]]:02X}"

            if parts[-1].startswith(("0X", "0B")):
                addr = int(parts[-1], 0)
                if not 0 <= addr <= 255:
                    raise ValueError("Valor fora do intervalo [0, 255]")
            else:
                addr = int(parts[-1])
                if parts[0] == "DATA" and not -128 <= addr <= 127:
                    raise ValueError("Valor fora do intervalo [-128, 127]")
                if parts[0] != "DATA" and not 0 <= addr <= 255:
                    raise ValueError("Valor fora do intervalo [0, 255]")
            addr_byte = (addr + 256) % 256
            hex_addr = "\n" + f"{addr_byte:02X}"

        fout.write(hex_result + hex_addr + "\n")
    return lineno

if len(sys.argv) != 3:
    print("Uso: python3 montador.py <entrada.asm> <saida.txt>")
    sys.exit(1)

path_in = sys.argv[1]
path_out = sys.argv[2]
lineno = 1

try:
    with open(path_in, 'r') as fin, open(path_out, 'w') as fout:
        fout.write("v3.0 hex words plain\n")
        labels = {}
        input_lines = fin.read().split("\n")
        lineno = preProcess(input_lines, labels)
        lineno = assemble(input_lines, labels, fout)
except Exception as e:
    print(f"Erro na linha {lineno}: {e}")
    os.remove(path_out)
    raise e