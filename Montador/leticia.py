# Autora: Leticia Souza de Souza
# Matricula: 22450212

import sys # Importa o modulo 'sys'
import os # Importa o modulo 'os'

# Tabela de instrucoes que usam os dois registradores (RA e RB) com seus codigos em hexa
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

# Tabela de instrucoes que usam apenas o registrador RB com seus codigos em hexa
only_rb = {
    'DATA': 0x20,
    'JMPR': 0x30,
    'IN': 0x70,
    'OUT': 0x78
}

# Tabela de instrucoes que geram dois bytes de saida com seus códigos em hexa
two_bytes = {
    'DATA': 0x20,
    'JMP': 0x40,
    'JCAEZ': 0x50
}

# Tabela de registradores com seus codigos em inteiro
registers = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3
}

# Tabela de flags da instrucao JCAEZ com seus codigos em inteiro
# Cada flag acrescenta no codigo da instrucao o bit '1' da sua posicao no JCAEZ. Dessa forma: 'C' = 0b1000; 'A' = 0b0100; 'E' = 0b0010; 'Z' = 0b0001
jcaez = {
    'C': 8,
    'A': 4,
    'E': 2,
    'Z': 1
}

# Checa se existem 3 argumentos após o comando "python3": montador.py <entrada.asm> <saida.txt>)
if len(sys.argv) != 3:
    print("Uso correto: python3 montador.py <entrada.asm> <saida.txt>")  # Mensagem explicando o uso correto dos argumentos
    sys.exit(1)  # Encerra o programa se os argumentos estiverem errados

# Pega os nomes dos caminhos dos arquivos de entrada e saida
path_in, path_out = sys.argv[1], sys.argv[2]

# Abre o arquivo de entrada (.asm) para leitura
with open(path_in , "r") as inputFile:
  # Abre o arquivo de saida (.txt) para escrita
  with open(path_out, "w") as outputFile:

    # Escreve no arquivo de saida o cabeçalho do formato v3.0 hex words plain
    outputFile.write("v3.0 hex words plain\n")

    # Percorre cada linha do arquivo de entrada
    for line in inputFile:
        # Remove comentários (tudo após ';') e espaços extras
        line = line.split(";")[0].strip()
        if not line:
            continue  # Ignora linhas vazias

        # Troca vírgulas por espaços (para facilitar o split)
        line = line.replace(",", " ")

        # Converte tudo para maiusculas, retira espacos extras e guarda as partes numa lista
        parts = [x.strip().upper() for x in line.split()]
        instruction = parts[0]  # A primeira palavra representa a instrução
        result = 0  # Valor inicial do codigo de maquina da linha
        hex_addr = ""   # String que contem o segundo byte (addr)

        # Consulta a tabela para tratar instrucoes que utilizam os dois registradores (RA e RB)
        if instruction in has_ra_rb:
            ra = parts[1]  # RA é a segunda palavra
            rb = parts[-1]  # RB é a última palavra
            result += has_ra_rb[instruction] + 4*registers[ra] + registers[rb] # Monta o primeiro byte: instrucao + RA deslocado 2 vezes para a esquerda + RB

        # Consulta a tabela para tratar instrucoes que utilizam apenas o segundo registrador (RB)
        elif instruction in only_rb:
            if instruction == "DATA":
                rb = parts[1]  # se for a instrucao DATA, o registrador RB esta na palavra central (DATA RB, Addr)
            else:
                rb = parts[-1]  # As demais instrucoes usam a ultima palavra como registrador RB
                result += only_rb[instruction]  # Acumula no resultado o valor do codigo da instrucao

                # Para as instrucoes IN e OUT, verifica se a segunda palavra representa o modo de endereco (ADDR)
                if instruction in ["IN", "OUT"] and parts[1] == "ADDR":
                    result += 4  # Se for endereco, soma 4 no resultado (pois se trata da soma com 0b100)
            result += registers[rb]  # Soma o valor do codigo do registrador RB no resultado

        # Caso seja a instrucao CLF (nao utiliza registradores)
        elif instruction == "CLF":
            result += 0x60  # Soma o valor do codigo do CLF

        # Trata instrucoes do tipo JCAEZ (ex: JC, JAE, etc.)
        elif instruction[0] == 'J' and instruction != "JMP":
            for ch in instruction[1:]:  # Percorre os caracteres de flag (ex: JCE -> ['C','E'])
                result += jcaez[ch]  # Soma o valor do codigo da flag correspondente (consultado na tabela)
            instruction = "JCAEZ"  # Muda o nome da instrucao para ser encontrada na tabela seguir o tratamento de two_bytes

        # Consulta a tabela para tratar instrucoes que utilizam dois bytes
        if instruction in two_bytes:
            result += two_bytes[instruction]  # Acumula no resultado o valor do codigo da instrucao (consultado na tabela)

            # Pergunta se o argumento que contem o valor do segundo byte esta em binario ou em hexadecimal
            if parts[-1].startswith(("0X", "0B")):
                addr = int(parts[-1], 0)  # Interpreta o argumento do segundo byte (como binario ou hexa) e converte para inteiro

                # Se for binario ou hexa e nao estiver no intervalo [0, 255], entao esta incorreto
                if not 0 <= addr <= 255:
                    os.remove(path_out)  # Remove o arquivo de saida
                    raise ValueError("Valor fora do intervalo [0, 255]") # Mostra mensagem de erro
            # Se nao for binario ou hexa, entao sera tratado como decimal
            else:
                addr = int(parts[-1])  # Interpreta o argumento do segundo byte como decimal e converte para inteiro

                # Se for decimal e guardar um dado (instrucao DATA) deve estar no intervalo [-128, 127], senao apresenta erro
                if instruction == "DATA" and not -128 <= addr <= 127:
                    os.remove(path_out)  # Remove o arquivo de saida
                    raise ValueError("Valor fora do intervalo [-128, 127]") # Mostra mensagem de erro
                # Se for decimal e guardar um endereco (nao for DATA) deve estar no intervalo [0, 255]
                if instruction != "DATA" and not 0 <= addr <= 255:
                    os.remove(path_out)  # Remove o arquivo de saida
                    raise ValueError("Endereco fora do intervalo [0, 255]") # Mostra mensagem de erro

            # Calcula o complemento de 2 (em 8 bits) para o valor do segundo byte
            complement = (addr + 256) % 256
            hex_addr = "\n" + hex(complement)[2:].upper()  # Gera a segunda linha com o valor do segundo byte em hexa
            if len(hex_addr) == 2:
                hex_addr = hex_addr[:1] + '0' + hex_addr[1:] # Se houver apenas 1 digito, acrescentar '0' entre o \n e o digito (ex: \n02)

        # Converte o resultado final do codigo da instrucao para hexa
        # Se for a instrucao LD, acrescentar '0' antes
        hex_code = hex(result)[2:].upper() if instruction != "LD" else '0' + hex(result)[2:].upper()
        # Escreve o código de máquina final no arquivo de saida (com o segundo byte, caso houver)
        outputFile.write(hex_code + hex_addr + "\n")