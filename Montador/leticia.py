# Autora: Leticia Souza de Souza
# Matricula: 22450212

import sys  # Importa o módulo 'sys' (necessário para acessar argumentos da linha de comando e encerrar o programa)
import os   # Importa o módulo 'os' (necessário para remover arquivo de saída em caso de erro)

# Tabela de instruções que usam os dois registradores (RA e RB), com seus códigos em hexadecimal
# Essas instruções geram sempre um único byte, pois não possuem argumento imediato
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

# Tabela de instruções que usam apenas o registrador RB
# Algumas (como DATA) também têm segundo byte de argumento
only_rb = {
    'DATA': 0x20,
    'JMPR': 0x30,
    'IN': 0x70,
    'OUT': 0x78
}

# Tabela de instruções que ocupam dois bytes no código de máquina:
# primeiro byte: opcode, segundo byte: dado imediato ou endereço
two_bytes = {
    'DATA': 0x20,
    'JMP': 0x40,
    'JCAEZ': 0x50
}

# Tabela de registradores, associando nomes (R0, R1, etc.) a valores numéricos usados na codificação
registers = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3
}

# Tabela de flags da instrução JCAEZ, cada flag ativa um bit específico no opcode:
# C=8 (1000), A=4 (0100), E=2 (0010), Z=1 (0001)
jcaez = {
    'C': 8,
    'A': 4,
    'E': 2,
    'Z': 1
}

# Verifica se o programa recebeu exatamente 3 argumentos: python3 montador.py <entrada.asm> <saida.txt>
if len(sys.argv) != 3:
    print("Uso correto: python3 montador.py <entrada.asm> <saida.txt>")  # Mensagem de instrução
    sys.exit(1)  # Encerra o programa com erro

# Guarda os caminhos dos arquivos de entrada e saída informados pelo usuário
path_in, path_out = sys.argv[1], sys.argv[2]

# ---------- 1ª PASSAGEM ----------
# Objetivo: identificar labels, calcular endereços e expandir pseudo-instruções

labels = {}            # Dicionário para mapear nome do label → endereço no código final
address = 0            # Contador de posição na memória (em bytes)
program_lines = []     # Lista para armazenar as linhas pré-processadas (já sem labels e com pseudo-instruções expandidas)

with open(path_in, "r") as inputFile:
    for line in inputFile:
        # Remove comentário (tudo após ';') e espaços extras
        line = line.split(";")[0].strip()
        if not line:
            continue  # Ignora linhas vazias

        # Separa a linha em partes, usando espaço como separador
        parts = [x.strip().upper() for x in line.replace(",", " ").split()]

        # Se for um label (ex: LOOP:)
        if parts[0].endswith(':'):
            label = parts[0][:-1]            # Remove os dois pontos
            labels[label] = address          # Salva na tabela de labels o endereço atual
            parts = parts[1:]                # Remove o label da lista para processar instrução
            if not parts:
                program_lines.append([])     # Linha que tinha só label, sem instrução
                continue

        instr = parts[0]

        # Detecta e expande pseudo-instruções
        if instr == 'CLR':
            # CLR RB → vira XOR RB, RB
            reg = parts[1]
            program_lines.append(['XOR', reg, reg])
            address += 1  # XOR ocupa 1 byte

        elif instr == 'MOVE':
            # MOVE RA, RB → vira XOR RB, RB seguido de XOR RA, RB
            reg_a = parts[1]
            reg_b = parts[2]
            program_lines.append(['XOR', reg_b, reg_b])
            program_lines.append(['XOR', reg_a, reg_b])
            address += 2  # são duas instruções, cada uma ocupa 1 byte

        elif instr == 'HALT':
            # HALT → vira JMP para o próprio endereço (loop infinito)
            program_lines.append(['JMP', f"0X{address:02X}"])  # Gera string com endereço em hexadecimal
            address += 2  # JMP ocupa 2 bytes

        else:
            # Linha normal (não é pseudo-instrução)
            program_lines.append(parts)
            # Soma tamanho que ela vai ocupar:
            if instr[0] == 'J' and instr != "JMP":
                # Instruções do tipo JC, JAE, etc → viram JCAEZ + flags, sempre ocupam 2 bytes
                address += 2
            elif instr in two_bytes:
                address += 2  # Instruções como JMP e DATA também ocupam 2 bytes
            else:
                address += 1  # Demais instruções ocupam 1 byte

# ---------- 2ª PASSAGEM ----------
# Objetivo: gerar código de máquina final

with open(path_out, "w") as outputFile:
    outputFile.write("v3.0 hex words plain\n")  # Cabeçalho para formato usado no Logisim

    for parts in program_lines:
        if not parts:
            continue  # Linha vazia (só label)

        instruction = parts[0]  # Nome da instrução (ex: ADD, JMP etc.)
        result = 0              # Vai acumular o valor do primeiro byte
        hex_addr = ""           # Segundo byte (se houver)

        # Monta instruções que têm dois registradores
        if instruction in has_ra_rb:
            ra = parts[1]  # Primeiro registrador
            rb = parts[-1] # Segundo registrador
            # Cálculo: opcode + RA deslocado 2 bits (4×ra) + RB
            result += has_ra_rb[instruction] + 4*registers[ra] + registers[rb]

        # Monta instruções que têm só RB
        elif instruction in only_rb:
            if instruction == "DATA":
                rb = parts[1]
            else:
                rb = parts[-1]
                result += only_rb[instruction]
                # IN/OUT podem ter modo ADDR:
                if instruction in ["IN", "OUT"] and parts[1] == "ADDR":
                    result += 4  # Seta bit que indica modo endereço
            result += registers[rb]

        # Monta instrução CLF (não usa registradores)
        elif instruction == "CLF":
            result += 0x60

        # Monta instruções JCAEZ (ex: JC, JAE, JE, etc)
        elif instruction[0] == 'J' and instruction != "JMP":
            for ch in instruction[1:]:
                result += jcaez[ch]  # Soma valor da flag correspondente
            instruction = "JCAEZ"   # Ajusta nome para pegar o opcode correto abaixo

        # Se a instrução tem segundo byte (DATA, JMP ou JCAEZ)
        if instruction in two_bytes:
            result += two_bytes[instruction]  # Soma o opcode base
            dest = parts[-1]                  # Argumento que representa endereço ou valor

            # Se for label, substitui pelo endereço
            if dest in labels:
                dest = f"0X{labels[dest]:02X}"

            # Converte argumento para inteiro, lidando com diferentes bases numéricas
            if dest.startswith(("0X", "0B")):
                addr = int(dest, 0)  # Converte direto (detecta base pelo prefixo)
                if not 0 <= addr <= 255:
                    os.remove(path_out)
                    raise ValueError("Valor fora do intervalo [0, 255]")  # Endereço fora do intervalo permitido
            else:
                addr = int(dest)  # Interpreta como decimal
                if instruction == "DATA" and not -128 <= addr <= 127:
                    os.remove(path_out)
                    raise ValueError("Valor fora do intervalo [-128, 127]")  # Valor imediato fora do intervalo permitido
                if instruction != "DATA" and not 0 <= addr <= 255:
                    os.remove(path_out)
                    raise ValueError("Endereco fora do intervalo [0, 255]")  # Endereço inválido

            # Calcula complemento de 2 para representar números negativos corretamente
            complement = (addr + 256) % 256
            hex_addr = "\n" + f"{complement:02X}"  # Gera string do segundo byte em hexa, ex: \n3F

        # Converte primeiro byte para string hexadecimal
        hex_code = hex(result)[2:].upper() if instruction != "LD" else '0' + hex(result)[2:].upper()
        # Escreve no arquivo de saída o primeiro byte + (se existir) segundo byte
        outputFile.write(hex_code + hex_addr + "\n")