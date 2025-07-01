# Autora: Leticia Souza de Souza
# Matricula: 22450212

import sys
import os

has_ra_rb = {
    'ADD': 0x80,
    'SHR': 0x90,
    'SHL': 0xa0,
    'NOT': 0xb0,
    'AND': 0xc0,
    'OR': 0xd0,
    'XOR': 0xe0,
    'CMP': 0xf0,
    'LD': 0x00,
    'ST': 0x10
}
only_rb = {
    'DATA': 0x20,
    'JMPR': 0x30,
    'IN': 0x70,
    'OUT': 0x78
}
two_bytes = {
    'DATA': 0x20,
    'JMP': 0x40,
    'JCAEZ': 0x50
}
registers = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3
}
jcaez = {
    'C': 8,
    'A': 4,
    'E': 2,
    'Z': 1
}

if len(sys.argv) != 3:
    print("Uso correto: python3 montador.py <entrada.asm> <saida.txt>")
    sys.exit(1)

path_in, path_out = sys.argv[1], sys.argv[2]

# 1ª PASSAGEM: identificar labels e calcular endereços
labels = {}
address = 0
program_lines = []  # para guardar as linhas pré-processadas (expandindo pseudo-instruções)

with open(path_in, "r") as f:
    for line in f:
        original_line = line
        line = line.split(";")[0].strip()
        if not line:
            continue

        parts = [x.strip().upper() for x in line.replace(",", " ").split()]

        # Se for label (termina com ':')
        if parts[0].endswith(':'):
            label = parts[0][:-1]
            labels[label] = address
            parts = parts[1:]
            if not parts:
                program_lines.append([])  # linha só com label
                continue

        instr = parts[0]

        # Checar e expandir pseudo-instruções na primeira passagem
        if instr == 'CLR':
            reg = parts[1]
            program_lines.append(['XOR', reg, reg])
            address += 1
        elif instr == 'MOV':
            reg_a = parts[1]
            reg_b = parts[2]
            program_lines.append(['XOR', reg_b, reg_b])
            program_lines.append(['XOR', reg_a, reg_b])
            address += 2
        elif instr == 'HALT':
            # HALT vira JMP para o próprio endereço
            program_lines.append(['JMP', str(address)])
            address += 2  # JMP tem dois bytes
        else:
            program_lines.append(parts)
            # Calcular tamanho normalmente
            if instr[0] == 'J' and instr != 'JMP':
                address += 2
            elif instr in two_bytes:
                address += 2
            else:
                address += 1

# 2ª PASSAGEM: gerar código de máquina
with open(path_out, "w") as outputFile:
    outputFile.write("v3.0 hex words plain\n")

    current_address = 0  # para HALT saber onde está

    for parts in program_lines:
        if not parts:
            continue

        instruction = parts[0]
        result = 0
        hex_addr = ""

        if instruction in has_ra_rb:
            ra = parts[1]
            rb = parts[-1]
            result += has_ra_rb[instruction] + 4*registers[ra] + registers[rb]

        elif instruction in only_rb:
            if instruction == "DATA":
                rb = parts[1]
            else:
                rb = parts[-1]
                result += only_rb[instruction]
                if instruction in ["IN", "OUT"] and parts[1] == "ADDR":
                    result += 4
            result += registers[rb]

        elif instruction == "CLF":
            result += 0x60

        elif instruction[0] == 'J' and instruction != "JMP":
            for ch in instruction[1:]:
                result += jcaez[ch]
            instruction = "JCAEZ"

        if instruction in two_bytes:
            result += two_bytes[instruction]
            dest = parts[-1]
            if dest in labels:
                addr = labels[dest]
            else:
                try:
                    addr = int(dest, 0)
                except:
                    os.remove(path_out)
                    raise ValueError(f"Label ou valor inválido: {dest}")

                if instruction == "DATA" and not -128 <= addr <= 127:
                    os.remove(path_out)
                    raise ValueError("Valor fora do intervalo [-128, 127]")
                if instruction != "DATA" and not 0 <= addr <= 255:
                    os.remove(path_out)
                    raise ValueError("Endereco fora do intervalo [0, 255]")

            complement = (addr + 256) % 256
            hex_addr = "\n" + f"{complement:02X}"

        hex_code = hex(result)[2:].upper() if instruction != "LD" else '0' + hex(result)[2:].upper()
        outputFile.write(hex_code + hex_addr + "\n")

        # Atualiza endereço atual
        if instruction in two_bytes:
            current_address += 2
        else:
            current_address += 1