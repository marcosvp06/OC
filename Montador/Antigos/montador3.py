import sys, os
from dataclasses import dataclass

@dataclass
class Instrucao:
    opcode: int
    is_2bytes: bool
    is_ra: bool
    is_rb: bool

instructions = {
    "ADD":   Instrucao(0b10000000, False, True, True),
    "SHR":   Instrucao(0b10010000, False, True, True),
    "SHL":   Instrucao(0b10100000, False, True, True),
    "NOT":   Instrucao(0b10110000, False, True, True),
    "AND":   Instrucao(0b11000000, False, True, True),
    "OR" :   Instrucao(0b11010000, False, True, True),
    "XOR":   Instrucao(0b11100000, False, True, True),
    "CMP":   Instrucao(0b11110000, False, True, True),
    "LD":    Instrucao(0b00000000, True, True, True),
    "ST":    Instrucao(0b00010000, True, True, True),
    "DATA":  Instrucao(0b00100000, True, False, True),
    "JUMPR": Instrucao(0b00110000, False, False, True),
    "JUMP":  Instrucao(0b01000000, True, False, False),
    "JCAEZ": Instrucao(0b01010000, True, False, False),
    "CLF":   Instrucao(0b01100000, False, False, False),
    "IN":    Instrucao(0b01110000, False, False, True),
    "OUT":   Instrucao(0b01111000, False, False, True)
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

def is_jcaez(aux):
    aux = aux.upper()
    if aux in instructions:
        return 0b0000
    if not aux.startswith("J"):
        return 0b0000

    flags = 0b0000
    usados = set()
    for ch in aux[1:]:
        ch = ch.upper()
        if ch not in jcaez:
            raise ValueError(f"Flag desconhecida '{ch}' em '{aux}'")
        if ch in usados:
            raise ValueError(f"Flag repetida '{ch}' em '{aux}'")
        usados.add(ch)
        flags |= jcaez[ch]
    return flags

def montar_instrucao(parts, lineno):
    if not parts:
        return b''

    parts = [p.upper() for p in parts]
    if len(parts) == 1 and parts[0][-1] == ":":
        labels[parts[0]] = linecode
    instr = parts[0]
    caez_bin = is_jcaez(instr)
    if caez_bin:
        instr = "JCAEZ"

    if instr not in instructions:
        raise ValueError(f"Instrucao invalida '{instr}' na linha {lineno}: {' '.join(parts)}")

    info = instructions[instr]
    binary = info.opcode + caez_bin
    i = 1

    if instr in ["IN", "OUT"]:
        if i >= len(parts):
            raise ValueError(f"Esperado modo (DATA ou ADDR) apos '{instr}' na linha {lineno}")
        modo = parts[i].upper()
        if modo == "ADDR":
            binary += 0b100
        elif modo != "DATA":
            raise ValueError(f"Modo invalido '{modo}' em '{instr}' na linha {lineno}")
        i += 1

    if info.is_ra:
        if i >= len(parts):
            raise ValueError(f"Esperado registrador RA apos '{instr}' na linha {lineno}")
        ra = parts[i].upper()
        if ra not in registers:
            raise ValueError(f"Registrador invalido '{ra}' na linha {lineno}")
        binary += registers[ra] << 2
        i += 1

    if info.is_rb:
        if i >= len(parts):
            raise ValueError(f"Esperado registrador RB apos '{instr}' na linha {lineno}")
        rb = parts[i].upper()
        if rb not in registers:
            raise ValueError(f"Registrador invalido '{rb}' na linha {lineno}")
        binary += registers[rb]
        i += 1

    result = [binary.to_bytes(1, 'big')]

    if info.is_2bytes:
        if i >= len(parts):
            raise ValueError(f"Esperado valor adicional apos '{instr}' na linha {lineno}")
        if parts[i] in labels:
            value = labels[parts[i]]
        else:
            try:
                value = int(parts[i], 0)
            except ValueError:
                raise ValueError(f"Valor invalido '{parts[i]}' na linha {lineno}")
            if not (0 <= value <= 255):
                raise ValueError(f"Valor fora do intervalo (0-255): '{value}' na linha {lineno}")
        result.append(value.to_bytes(1, 'big'))
        i += 1

    if i != len(parts):
        raise ValueError(f"Argumentos extras apos instrucao na linha {lineno}: {' '.join(parts[i:])}")

    return b''.join(result)

# === Main ===
labels = {}
linecode = 0

def main():
    import sys
    if len(sys.argv) != 3:
        print("Uso: python montador.py <entrada.ldc> <saida.bin>")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    if not entrada.lower().endswith(".ldc"):
        print(f"Erro: o arquivo de entrada deve ter extensao .ldc (recebido: '{entrada}')")
        sys.exit(1)

    with open(entrada, 'r') as fin, open(saida, 'wb') as fout:
        sucesso = True
        for lineno, line in enumerate(fin, start=1):
            line = line.split(":3")[0].strip()
            if not line:
                continue
            linecode += 1
            parts = line.split()
            try:
                bytes_instrucao = montar_instrucao(parts, lineno)
                fout.write(bytes_instrucao)
            except ValueError as e:
                print(f"[ERRO] {e}")
                sucesso = False

    if sucesso:
        print("Compilacao concluida com sucesso!")
    else:
        print("Compilacao finalizada com erros.")
        os.remove(saida)

if __name__ == "__main__":
    main()