import sys
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

two_bytes = {
  'DATA': 0x20,
  'JMP': 0x40,
  'JCAEZ': 0x50
}

only_rb = {
  'DATA': 0x20,
  'JMPR': 0x30,
  'IN': 0x70,
  'OUT': 0x78
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
    print("Uso: python montador.py <entrada.asm> <saida>")
    sys.exit(1)
path_entrada, path_saida = sys.argv[1], sys.argv[2]

with open(path_entrada , "r") as entrada:
  with open(path_saida, "w") as saida:

    saida.write("v3.0 hex words plain\n")
    for linha in entrada:
        linha = linha.split(";")[0].strip()
        if not linha:
            continue
        linha = linha.replace(",", " ")

        separados = [x.strip().upper() for x in linha.split()]
        instruction = separados[0]
        resultado = 0
        ra = "None"
        rb = "None"
        addr = -1000
        hex_addr = ""

        if instruction in has_ra_rb:
            ra = separados[-2]
            rb = separados[-1]
            resultado += has_ra_rb[instruction] + registers[ra] + registers[rb]

        elif instruction in only_rb:
            if instruction == "DATA":
                rb = separados[-2]
            else:
                rb = separados[-1]
                resultado += only_rb[instruction]
            resultado += registers[rb]

        if instruction in ["IN", "OUT"]:
            if separados[-2] == "Addr":
                resultado += 4

        elif instruction == "CLF":
            resultado += 0x60

        elif instruction[0] == 'J' and instruction != "JMP":
            for ch in instruction[1:]:
                resultado += jcaez[ch]
            instruction = "JCAEZ"

        if instruction in two_bytes:
            resultado += two_bytes[instruction]
            addr = int(separados[-1], 0)
            if addr <= 127 and addr >= -128:
                complement = (addr + 256) % 256 
                hex_addr = "\n" + hex(complement)[2:].upper()

        hex_code = hex(resultado)[2:].upper()
        saida.write(hex_code + hex_addr + "\n")

        print(instruction)
        print(f"Ra = {ra}")
        print(f"Rb = {rb}")
        print(f"code = {hex_code}")
        if addr == -1000:
            print(f"addr = None")
        else:
            print(f"addr = {hex_addr}")
        print("")