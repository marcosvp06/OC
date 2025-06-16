# Autor: Marcos Paulo Vieira Pedrosa
# Matricula: 22401906

import sys, os  # Importa os modulos 'sys' (para uso no terminal) e 'os' (para operacoes com arquivos)
from dataclasses import dataclass  # Importa o 'dataclass' para criar uma estrutura de dados mais simples

# Define uma classe "Instrucao" para representar cada instrucao da linguagem de maquina
@dataclass
class Instrucao:
    opcode: int        # Codigo da instrucao (em hexa)
    has_ra: bool       # Indica se a instrucao utiliza o registrador RA
    has_rb: bool       # Indica se a instrucao utiliza o registrador RB
    has_2bytes: bool   # Indica se a instrucao ocupa dois bytes na memoria (precisa de um segundo byte de argumento)

# Tabela com todas as instrucoes, seus opcodes e suas configuracoes de uso de registradores (RA, RB) e segundo byte
instructions = {
    "ADD":   Instrucao(0x80, True, True, False),
    "SHR":   Instrucao(0x90, True, True, False),
    "SHL":   Instrucao(0xA0, True, True, False),
    "NOT":   Instrucao(0xB0, True, True, False),
    "AND":   Instrucao(0xC0, True, True, False),
    "OR" :   Instrucao(0xD0, True, True, False),
    "XOR":   Instrucao(0xE0, True, True, False),
    "CMP":   Instrucao(0xF0, True, True, False),
    "LD":    Instrucao(0x00, True, True, False),
    "ST":    Instrucao(0x10, True, True, False ),
    "DATA":  Instrucao(0x20, False, True, True ),
    "JMPR":  Instrucao(0x30, False, True, False),
    "JMP":   Instrucao(0x40, False, False, True),
    "JCAEZ": Instrucao(0x50, False, False, True),
    "CLF":   Instrucao(0x60, False, False, False),
    "IN":    Instrucao(0x70, False, True, False),
    "OUT":   Instrucao(0x78, False, True, False)
}

# Tabela de registradores com seus codigos binarios
registers = {"R0": 0b00, "R1": 0b01, "R2": 0b10, "R3": 0b11}

# Tabela de flags da instrucao JCAEZ com seus codigos em binario
jcaez = {'C': 0b1000, 'A': 0b0100, 'E': 0b0010, 'Z': 0b0001}

# Checa se o numero de argumentos passados no terminal esta correto (esperado: montador.py <entrada.asm> <saida.txt>)
if len(sys.argv) != 3:
    print("Uso: python3 montador.py <entrada.asm> <saida.txt>")  # Mostra mensagem de uso correto
    sys.exit(1)  # Encerra o programa

# Guarda os caminhos dos arquivos de entrada e saida
path_in = sys.argv[1]
path_out = sys.argv[2]

try:
    # Abre o arquivo de entrada (.asm) para leitura e o de saida (.txt) para escrita
    with open(path_in, 'r') as fin, open(path_out, 'w') as fout:
        fout.write("v3.0 hex words plain\n")  # Escreve o cabecalho do arquivo de memoria do Logisim

        # Percorre cada linha do arquivo de entrada, guardando o numero da linha (lineno) para uso em mensagens de erro
        for lineno, line in enumerate(fin, start=1):
            # Remove comentarios (tudo apos ';') e espacos extras
            line = line.split(";")[0].strip()
            if not line: continue  # Ignora linhas vazias

            # Troca virgulas por espacos e separa as partes da linha
            line = line.replace(",", " ")
            parts = [x.strip().upper() for x in line.split()] # Divide a linha em partes, retira espaços extras e converte tudo para maiusculas (e guarda numa lista contendo as partes)

            # Inicializa variaveis de trabalho: resultado do codigo da instrucao (result); codigo do registrador RA; codigo do registrador RB
            result = ra = rb = 0
            hex_addr = "" # Inicializa a string do segundo byte da instrucao (addr) a ser escrito (se houver)
            pos = 1  # Posicao inicial para leitura dos argumentos (por padrao, segunda palavra da linha)

            # Caso a instrucao comece com 'J' e nao seja "JMP" nem "JMPR", entao se trata da instrucao JCAEZ
            if parts[0][0] == "J" and parts[0] not in ["JMP", "JMPR"]:
                for ch in parts[0][1:]:  # Para cada flag presente na instrucao
                    result += jcaez[ch]  # Soma o valor correspondente da flag
                parts[0] = "JCAEZ"  # Altera o nome da instrucao para JCAEZ (para buscar na tabela depois)

            # Caso a instrucao seja IN ou OUT
            if parts[0] in ["IN", "OUT"]:
                pos += 1  # Avanca a posicao dos argumentos
                if parts[1] == "ADDR": # Caso utilize o modo endereco (ADDR)
                    result += 4  # Soma o valor de endereco (0b100) no resultado

            # Consulta a tabela de instrucoes e guarda em instr
            instr = instructions[parts[0]]

            # Se a instrucao usa RA, pega o codigo do registrador (consultando na tabela)
            if instr.has_ra:
                ra = registers[parts[pos]]
                pos += 1 # Avanca a posicao dos argumentos

            # Se a instrucao usa RB, pega o codigo do registrador (consultando na tabela)
            if instr.has_rb:
                rb = registers[parts[pos]]
                pos += 1 # Avanca a posicao dos argumentos

            # Monta o primeiro byte (opcode + 4*RA + RB)
            # Acumula no valor do codigo de maquina a soma entre: codigo da instrucao + codigo do registrador RA deslocado 2 vezes a esquerda (4*RA) + codigo do registrador RB. Ambos os valores consultados nas tabelas
            result += instr.opcode + 4*ra + rb
            hex_result = f"{result:02X}"  # Converte o resultado para hexa com dois digitos

            # Se for uma instrucao que escreve um segundo byte no arquivo de saida, ou seja, possui um argumento que guarda um valor ou endereco (Addr)
            if instr.has_2bytes:
                # Identifica se o argumento esta em hexadecimal ou binario
                if parts[-1].startswith(("0X", "0B")):
                    addr = int(parts[-1], 0)  # Converte para inteiro automaticamente (estando em binario ou hexa)
                    # Verifica o intervalo permitido (0 a 255)
                    if not 0 <= addr <= 255:
                        raise ValueError("Valor fora do intervalo [0, 255]") # Mostra mensagem de erro
                else:
                    addr = int(parts[-1])  # Converte o argumento como decimal
                    # Se for DATA, o intervalo permitido e [-128, 127]
                    if parts[0] == "DATA" and not -128 <= addr <= 127:
                        raise ValueError("Valor fora do intervalo [-128, 127]") # Mostra mensagem de erro
                    # Se for outra instrucao, o intervalo e [0, 255]
                    if parts[0] != "DATA" and not 0 <= addr <= 255:
                        raise ValueError("Valor fora do intervalo [0, 255]") # Mostra mensagem de erro

                # Calcula o complemento de 2 (em 8 bits) para representar o segundo byte
                complement = (addr + 256) % 256
                hex_addr = "\n" + f"{complement:02X}"  # Gera a linha do segundo byte em hexa

            # Escreve o resultado final no arquivo de saida: codigo instrucao + segundo byte
            fout.write(hex_result + hex_addr + "\n")

# Caso ocorra algum erro durante o processo
except Exception as e:
    print(f"Erro na linha {lineno}: {e}")  # Mostra em qual linha ocorreu o erro
    os.remove(path_out)  # Remove o arquivo de saida (para evitar deixar um arquivo corrompido)
    raise e  # Mostra o erro no terminal