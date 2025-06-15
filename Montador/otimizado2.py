import sys, os
from dataclasses import dataclass

@dataclass
class Instrucao:
    opcode: int
    has_2bytes: bool
    has_ra: bool
    has_rb: bool

instructions = {
    "ADD":   Instrucao(0x80, False, True, True),
    "SHR":   Instrucao(0x90, False, True, True),
    "SHL":   Instrucao(0xA0, False, True, True),
    "NOT":   Instrucao(0xB0, False, True, True),
    "AND":   Instrucao(0xC0, False, True, True),
    "OR" :   Instrucao(0xD0, False, True, True),
    "XOR":   Instrucao(0xE0, False, True, True),
    "CMP":   Instrucao(0xF0, False, True, True),
    "LD":    Instrucao(0x00, False, True, True),
    "ST":    Instrucao(0x10, False, True, True),
    "DATA":  Instrucao(0x20, True, False, True),
    "JMPR":  Instrucao(0x30, False, False, True),
    "JMP":   Instrucao(0x40, True, False, False),
    "JCAEZ": Instrucao(0x50, True, False, False),
    "CLF":   Instrucao(0x60, False, False, False),
    "IN":    Instrucao(0x70, False, False, True),
    "OUT":   Instrucao(0x78, False, False, True)
}

registers = {
    "R0": 0b00,
    "R1": 0b01,
    "R2": 0b10,
    "R3": 0b11
}

jcaez = {
    'C': 0b1000,
    'A': 0b0100,
    'E': 0b0010,
    'Z': 0b0001
}

try:
    with open(path_in, 'r') as fin, open(path_out, 'w') as fout:
        fout.write("v3.0 hex words plain\n")
        for lineno, line in enumerate(fin, start=1):
            line = line.split(";")[0].strip()
            if not line continue
            line = line.replace(",", " ")
            parts = [x.strip().upper() for x in line.split()]
            result = ra = rb = 0
            hex_addr = ""
            
            if parts[0][0] == "J" and not in ["JMP", "JMPR"]:
            for ch in parts[0][1:]:
                result += jcaez[ch]
            parts[0] = "JCAEZ"
            
            instr, i = instructions[parts[0]], 1
            if instr in ["IN", "OUT"] and parts[i] == "ADDR":
                result += 4
            if instr.has_ra:
                ra = parts[i]; i+=1
            if instr.has_rb:
                rb = parts[i]; i+=1
            result += instr.opcode + 4*ra + rb
            if instr.has_2bytes:    
                if parts[-1].startswith("0X", "0B"):
                    addr = int(parts[-1], 0)
                    if not 0 <= addr <= 255:
                        raise ValueError("Valor fora do intervalo [0, 255]")
                else:
                    addr = int(parts[-1])
                    if instr == "DATA" and not -128 <= addr <= 127:
                        raise ValueError("Valor fora do intervalo [-128, 127]")
                    if instr != "DATA" ans not 0 <= addr <= 255:
                        raise ValueError("Valor fora do intervalo [0, 255]")
                complement = (addr + 256) % 256
                hex_addr = "\n" + f"{complement:02X}"
            fout.write(f"{result:02X}" + hex_addr + "\n")
except Exception as e:
    os.remove(path_out)
    raise e
