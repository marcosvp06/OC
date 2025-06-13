import sys, os
has_ra_rb = {'ADD': 0x80, 'SHR': 0x90, 'SHL': 0xa0, 'NOT': 0xb0, 'AND': 0xc0, 'OR': 0xd0, 'XOR': 0xe0, 'CMP': 0xf0, 'LD': 0x00, 'ST': 0x10}
only_rb = {'DATA': 0x20, 'JMPR': 0x30, 'IN': 0x70, 'OUT': 0x78}
two_bytes = {'DATA': 0x20, 'JMP': 0x40, 'JCAEZ': 0x50}
registers = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3}
jcaez = {'C': 8, 'A': 4, 'E': 2, 'Z': 1}

if len(sys.argv) != 3:
    print("Uso: python montador.py <entrada.asm> <saida.txt>")
    sys.exit(1)
path_in, path_out = sys.argv[1], sys.argv[2]
with open(path_in , "r") as inputFile:
  with open(path_out, "w") as outputFile:

    outputFile.write("v3.0 hex words plain\n")
    for line in inputFile:
        line = line.split(";")[0].strip()
        if not line:
            continue
        line = line.replace(",", " ")

        parts = [x.strip().upper() for x in line.split()]
        instruction = parts[0]
        result = 0
        hex_addr = ""

        if instruction in has_ra_rb:
            ra = parts[-2]
            rb = parts[-1]
            result += has_ra_rb[instruction] + 4*registers[ra] + registers[rb]

        elif instruction in only_rb:
            if instruction == "DATA":
                rb = parts[-2]
            else:
                rb = parts[-1]
                result += only_rb[instruction]
                if instruction in ["IN", "OUT"] and parts[-2] == "ADDR":
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
            if parts[-1][:2] in ["0X", "0B"]:
                addr = int(parts[-1], 0)
            else:
                addr = int(parts[-1])
            if addr > 127 or addr < -128:
                os.remove(path_out)
                raise ValueError("Foi encontrado um valor invalido! Intervalo: [-128, 127]")
            else:
                complement = (addr + 256) % 256 
                hex_addr = "\n" + hex(complement)[2:].upper()
        hex_code = hex(result)[2:].upper()
        outputFile.write(hex_code + hex_addr + "\n")