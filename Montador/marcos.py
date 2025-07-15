# Autor: Marcos Paulo Vieira Pedrosa
# Matricula: 22401906

# Importa módulos da biblioteca padrão:
import sys  # Para acessar argumentos da linha de comando e encerrar o programa com sys.exit
import os   # Para operações de sistema, como deletar arquivo de saída em caso de erro
from dataclasses import dataclass, field  # Para criar classes simples (estruturas de dados)

# Classe Instruction representa uma instrução real da linguagem de máquina
# Cada campo indica informações que o montador precisa saber para gerar o código binário
@dataclass
class Instruction:
    opcode: int         # Código hexadecimal da instrução
    has_ra: bool        # Indica se a instrução utiliza registrador RA
    has_rb: bool        # Indica se a instrução utiliza registrador RB
    has_2bytes: bool    # Indica se a instrução ocupa dois bytes na memória (precisa de um segundo byte de argumento)

# Classe PseudoInstruction representa uma pseudo-instrução (não existe no processador, mas será substituída)
# Campos indicam quais registradores ela usa, quantos bytes vai gerar e quais instruções reais substituem
@dataclass
class PseudoInstruction:
    has_first_register: bool    # Indica se a instrução utiliza um regsitrador na primeira posição
    has_second_register: bool   # Indica se a instrução utiliza um regsitrador na segunda posição
    bytes_size: int             # Quantos bytes no total essa pseudo-instrução vai gerar no código final
    replacements: list[str] = field(default_factory=list)  # Lista de strings com as instruções reais que a substituem

# Tabela (Dicionário) com todas as instruções, seus opcodes e suas configuracoes de uso de registradores (RA, RB) e segundo byte
instructions = {
    "ADD":   Instruction(0x8000, True, True, False),
    "SHR":   Instruction(0x9000, True, True, False),
    "SHL":   Instruction(0xA000, True, True, False),
    "NOT":   Instruction(0xB000, True, True, False),
    "AND":   Instruction(0xC000, True, True, False),
    "OR" :   Instruction(0xD000, True, True, False),
    "XOR":   Instruction(0xE000, True, True, False),
    "CMP":   Instruction(0xF000, True, True, False),
    "LD":    Instruction(0x0000, True, True, False),
    "ST":    Instruction(0x1000, True, True, False),
    "DATA":  Instruction(0x2000, False, True, True),
    "JMPR":  Instruction(0x3000, False, True, False),
    "JMP":   Instruction(0x4000, False, False, True),
    "JCAEZ": Instruction(0x5000, False, False, True),
    "CLF":   Instruction(0x6000, False, False, False),
    "IN":    Instruction(0x7000, False, True, False),
    "OUT":   Instruction(0x7008, False, True, False)
}

# Tabela (Dicionário) com todas as pseudo-instruções e seus opcodes
# Funciona associando a chave 'nome' (string) a um objeto Instruction
# # Cada pseudo-instrução será expandida para instruções reais descritas em 'replacements'
pseudoInstructions = {
    "MOVE": PseudoInstruction(True, True, 2, ["XOR RB RB", "XOR RA RB"]), # MOVE RA RB → limpa RB e copia RA
    "CLR":  PseudoInstruction(True, False, 1, ["XOR RA RA"]), # CLR RA → zera RA
    "HALT": PseudoInstruction(False, False, 2, ["JMP HALT_LABEL"]) # HALT → loop infinito via JMP para label gerado
}

# Tabela de registradores com seus códigos binários (usados ao montar as instruções)
registers = {"R0": 0b00, "R1": 0b01, "R2": 0b10, "R3": 0b11}

# Tabela de flags para a instrução JCAEZ, indicando o bit correspondente de cada flag
jcaez = {'C': 0b1000, 'A': 0b0100, 'E': 0b0010, 'Z': 0b0001}

# Função para pré-processar as linhas de entrada antes da montagem:
# Expande pseudo-instruções, processa labels e calcula endereços
def pre_process(input_lines, labels, original_line_numbers):
    output_line = 0        # Conta qual linha do arquivo final (importante para calcular endereços)
    halt_count = 0         # Contador para gerar labels únicos para cada HALT
    new_lines = []         # Guarda as novas linhas após expansão

    # Percorre todas as linhas originais, guardando o número da linha original (para mensagens de erro)
    for lineno, original_line in enumerate(input_lines, start=1):
        # Remove comentários (tudo após ';') e espaços no início/fim
        clean_line = original_line.split(";", 1)[0].strip()

        # Verifica se existe label na linha (identificado por ':')
        parts_with_label = clean_line.split(":", 1)
        if len(parts_with_label) == 2:
            label = parts_with_label[0].strip().upper()  # Nome do label em maiúsculo
            if label:
                labels[label] = output_line  # Salva no dicionário de labels, associando ao número da linha de saída
            clean_line = parts_with_label[1].strip()     # Remove o label da linha, ficando só a instrução

        clean_line = clean_line.replace(",", " ")  # Troca vírgulas por espaço para padronizar

        if not clean_line:
            continue  # Ignora linhas vazias

        parts = clean_line.upper().split()  # Divide a linha em partes (instrução + argumentos)
        instr_name = parts[0]
        args = parts[1:]

        # Se for pseudo-instrução:
        if instr_name in pseudoInstructions:
            pseudo = pseudoInstructions[instr_name]
            expanded = list(pseudo.replacements)  # Copia as instruções reais para expandir

            # Se precisa substituir RA e RB pelos registradores dados
            if pseudo.has_first_register:
                expanded = [instr.replace("RA", args[0]) for instr in expanded]
            if pseudo.has_second_register:
                expanded = [instr.replace("RB", args[1]) for instr in expanded]

            # Se for HALT, gera label único e substitui o placeholder
            if instr_name == "HALT":
                halt_label = f"__HALT_{halt_count}"
                halt_count += 1
                expanded = [instr.replace("HALT_LABEL", halt_label) for instr in expanded]
                labels[halt_label] = output_line  # Marca onde será o label

            # Adiciona as instruções expandidas ao código final
            new_lines.extend(expanded)
            # Marca que todas essas instruções vieram da mesma linha original (para mensagens de erro)
            original_line_numbers.extend([lineno] * len(expanded))
            # Soma bytes que essas instruções ocuparão
            output_line += pseudo.bytes_size

        else:
            # Linha normal (não pseudo-instrução)
            new_lines.append(clean_line)
            original_line_numbers.append(lineno)
            output_line += 1
            # Se a instrução ocupa dois bytes (ex: JMP, JCAEZ, DATA etc), soma mais 1
            if (instr_name.startswith("J") and instr_name != "JMPR") or(instr_name in instructions and instructions[instr_name].has_2bytes):
                output_line += 1

    # Substitui as linhas originais pelas novas linhas processadas
    input_lines[:] = new_lines

# Função para montar (gerar o código de máquina) a partir das linhas processadas
def assemble(input_lines, labels, fout, original_line_numbers):
    for i, line in enumerate(input_lines):
        lineno = original_line_numbers[i]  # Número da linha original (para mensagem de erro)
        try:
            parts = line.upper().split()
            if not parts:
                continue  # Ignora linhas vazias

            instr_name = parts[0]
            args = parts[1:]
            result = ra = rb = 0   # Inicializa valores intermediários
            hex_addr = ""          # Segundo byte (quando existir)
            pos = 0                # Posição do próximo argumento a ser lido

            # Trata instrução JCAEZ: soma valores das flags ao opcode
            if instr_name[0] == "J" and instr_name not in ["JMP", "JMPR"]:
                for ch in instr_name[1:]:
                    result += jcaez[ch]
                instr_name = "JCAEZ"  # Para consultar na tabela de instruções

            # Trata instruções IN/OUT com modo ADDR (endereço)
            if instr_name in ["IN", "OUT"]:
                if args[0] == "ADDR":
                    result += 4  # Marca bit que indica que é modo endereço
                pos += 1

            instr = instructions[instr_name]  # Busca dados sobre a instrução

            # Se usa RA e/ou RB, pega códigos dos registradores
            if instr.has_ra:
                ra = registers[args[pos]]
                pos += 1
            if instr.has_rb:
                rb = registers[args[pos]]
                pos += 1

            # Monta primeiro byte: opcode + 4*RA + RB
            result += instr.opcode + 4 * ra + rb
            hex_result = f"{result:04X}"  # Converte para hexa com dois dígitos

            # Se a instrução precisa de segundo byte (ex: endereço ou imediato)
            if instr.has_2bytes:
                addr_str = args[-1]
                # Se argumento for um label, substitui pelo valor
                if addr_str in labels:
                    addr_str = f"0X{labels[addr_str]:02X}"

                # Converte string para inteiro, considerando se é hexa, binário ou decimal
                if addr_str.startswith(("0X", "0B")):
                    addr = int(addr_str, 0)
                    if not 0 <= addr <= 65535:
                        raise ValueError("Valor fora do intervalo [0, 65535]")
                else:
                    addr = int(addr_str)
                    if instr_name == "DATA" and not -32768 <= addr <= 32767:
                        raise ValueError("Valor fora do intervalo [-32768, 32767]")
                    if instr_name != "DATA" and not 0 <= addr <= 65535:
                        raise ValueError("Valor fora do intervalo [0, 65535]")

                # Calcula complemento de 2 para representar valores negativos ou positivos corretamente
                addr_byte = (addr + 65536) % 65536
                hex_addr = "\n" + f"{addr_byte:04X}"  # Segundo byte

            # Escreve no arquivo de saída o byte da instrução (+ segundo byte se existir)
            fout.write(hex_result + hex_addr + "\n")

        except Exception as e:
            # Em caso de erro, mostra mensagem detalhada com número da linha e conteúdo
            raise Exception(f"Erro ao montar na linha {lineno}: {line.strip()} | Erro: {e}") from e

# Função principal: orquestra o processo de ler o arquivo, pré-processar e montar
def main():
    # Verifica se foram passados os dois argumentos: entrada e saída
    if len(sys.argv) != 3:
        print("Uso: python3 montador.py <entrada.asm> <saida.txt>")
        sys.exit(1)

    path_in, path_out = sys.argv[1], sys.argv[2]

    try:
        # Abre o arquivo de entrada para leitura e o de saída para escrita
        with open(path_in, 'r') as fin, open(path_out, 'w') as fout:
            fout.write("v3.0 hex words plain\n")  # Cabeçalho exigido pelo Logisim
            labels = {}  # Guarda os labels e seus endereços
            original_line_numbers = []  # Guarda número das linhas originais (para erros)
            input_lines = fin.read().splitlines()  # Lê todas as linhas do arquivo
            pre_process(input_lines, labels, original_line_numbers)  # Expande pseudo-instruções e resolve labels
            assemble(input_lines, labels, fout, original_line_numbers)  # Monta e escreve no arquivo final

    except Exception as e:
        print(e)
        if os.path.exists(path_out):
            os.remove(path_out)  # Remove arquivo de saída em caso de erro, para evitar arquivo corrompido
        sys.exit(1)

# Ponto de entrada do script: só executa main() se o script for chamado diretamente
if __name__ == "__main__":
    main()