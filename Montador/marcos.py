# Autor: Marcos Paulo Vieira Pedrosa
# Matricula: 22401906

import sys
import os
from dataclasses import dataclass, field

@dataclass
class Instruction:
    opcode: int
    has_ra: bool
    has_rb: bool
    has_2bytes: bool

@dataclass
class PseudoInstruction:
    has_first_register: bool
    has_second_register: bool
    bytes_size: int
    replacements: list[str] = field(default_factory=list)

instructions = {
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

pseudoInstructions = {
    "MOV":  PseudoInstruction(True, True, 2, ["XOR RB RB", "XOR RA RB"]),
    "CLR":  PseudoInstruction(True, False, 1, ["XOR RA RA"]),
    "HALT": PseudoInstruction(False, False, 2, ["JMP HALT_LABEL"])
}

registers = {"R0": 0b00, "R1": 0b01, "R2": 0b10, "R3": 0b11}
jcaez = {'C': 0b1000, 'A': 0b0100, 'E': 0b0010, 'Z': 0b0001}

def pre_process(input_lines, labels, original_line_numbers):
    output_line = 0
    halt_count = 0
    new_lines = []

    for lineno, original_line in enumerate(input_lines, start=1):

        clean_line = original_line.split(";", 1)[0].strip()
        parts_with_label = clean_line.split(":", 1)
        if len(parts_with_label) == 2:
            label = parts_with_label[0].strip().upper()
            if label:
                labels[label] = output_line
            clean_line = parts_with_label[1].strip()

        clean_line = clean_line.replace(",", " ")
        if not clean_line:
            continue

        parts = clean_line.upper().split()
        instr_name = parts[0]
        args = parts[1:]

        if instr_name in pseudoInstructions:
            pseudo = pseudoInstructions[instr_name]
            expanded = list(pseudo.replacements)

            if pseudo.has_first_register:
                expanded = [instr.replace("RA", args[0]) for instr in expanded]
            if pseudo.has_second_register:
                expanded = [instr.replace("RB", args[1]) for instr in expanded]

            if instr_name == "HALT":
                halt_label = f"__HALT_{halt_count}"
                halt_count += 1
                expanded = [instr.replace("HALT_LABEL", halt_label) for instr in expanded]
                labels[halt_label] = output_line

            new_lines.extend(expanded)
            original_line_numbers.extend([lineno] * len(expanded))
            output_line += pseudo.bytes_size

        else:
            new_lines.append(clean_line)
            original_line_numbers.append(lineno)
            output_line += 1
            if instr_name.startswith("J") or (
                instr_name in instructions and instructions[instr_name].has_2bytes
            ):
                output_line += 1

    input_lines[:] = new_lines
    return

def assemble(input_lines, labels, fout, original_line_numbers):
    for i, line in enumerate(input_lines):
        lineno = original_line_numbers[i]
        try:
            parts = line.upper().split()
            if not parts:
                continue

            instr_name = parts[0]
            args = parts[1:]
            result = ra = rb = 0
            hex_addr = ""
            pos = 0

            if instr_name[0] == "J" and instr_name not in ["JMP", "JMPR"]:
                for ch in instr_name[1:]:
                    result += jcaez[ch]
                instr_name = "JCAEZ"

            if instr_name in ["IN", "OUT"]:
                if args[0] == "ADDR":
                    result += 4
                pos += 1

            instr = instructions[instr_name]

            if instr.has_ra:
                ra = registers[args[pos]]
                pos += 1
            if instr.has_rb:
                rb = registers[args[pos]]
                pos += 1

            result += instr.opcode + 4 * ra + rb
            hex_result = f"{result:02X}"

            if instr.has_2bytes:
                addr_str = args[-1]
                if addr_str in labels:
                    addr_str = f"0X{labels[addr_str]:02X}"

                if addr_str.startswith(("0X", "0B")):
                    addr = int(addr_str, 0)
                    if not 0 <= addr <= 255:
                        raise ValueError("Valor fora do intervalo [0, 255]")
                else:
                    addr = int(addr_str)
                    if instr_name == "DATA" and not -128 <= addr <= 127:
                        raise ValueError("Valor fora do intervalo [-128, 127]")
                    if instr_name != "DATA" and not 0 <= addr <= 255:
                        raise ValueError("Valor fora do intervalo [0, 255]")
                addr_byte = (addr + 256) % 256
                hex_addr = "\n" + f"{addr_byte:02X}"

            fout.write(hex_result + hex_addr + "\n")

        except Exception as e:
            raise Exception(f"Erro ao montar na linha {lineno}: {line.strip()} | Erro: {e}") from e

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 montador.py <entrada.asm> <saida.txt>")
        sys.exit(1)

    path_in, path_out = sys.argv[1], sys.argv[2]

    try:
        with open(path_in, 'r') as fin, open(path_out, 'w') as fout:
            fout.write("v3.0 hex words plain\n")
            labels = {}
            original_line_numbers = []
            input_lines = fin.read().splitlines()

            pre_process(input_lines, labels, original_line_numbers)
            assemble(input_lines, labels, fout, original_line_numbers)

    except Exception as e:
        print(e)
        if os.path.exists(path_out):
            os.remove(path_out)
        sys.exit(1)

if __name__ == "__main__":
    main()