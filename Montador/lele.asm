data r0 0         # Endereco do teclado
out addr r0       # Ativa o teclado

in data r0        # R0 recebe o primeiro dígito (em ASCII)
in data r2        # R2 recebe o caractere da operação (em ASCII)
in data r1        # R1 recebe o segundo dígito (em ASCII)

data r3 48        # R3 recebe o valor ASCII de '0'

xor r3 r0         # Converte R0 de ASCII para inteiro
xor r3 r1         # Converte R1 de ASCII para inteiro

data r3 45        # R3 recebe o valor ASCII de '-'
cmp r2 r3         # Verifica se a operação é subtração
je subtrai        # Se sim, pula para o bloco de subtração

data r3 43        # R3 recebe o valor ASCII de '+'
cmp r2 r3         # Verifica se a operação é adição
je soma           # Se sim, pula para o bloco de soma

data r3 42       # R3 recebe o valor ASCII de '*'
cmp r2 r3         # Verifica se a operação é multiplicação
je multiplica     # Se sim, pula para o bloco de multiplicação

data r2 1         # Endereco do monitor
data r3 63        # R3 recebe o valor ASCII de '?'
out addr r2       # Ativa o monitor
out data r3       # Exibe '?' no monitor
jump encerra      # Se a operação não for reconhecida, encerra o programa

soma:
    add r0 r1     # Soma os dois dígitos (resultado vai para R1)
    jump final     # Vai para a parte final que imprime o resultado

subtrai:
    data r3 1      # R3 = 1, para usar no complemento de dois

    cmp r0 r1      # Compara os dois dígitos
    jae positivo   # Se R0 >= R1, executa R0 - R1
    jump negativo  # Caso contrário, executa R1 - R0 e exibe sinal de negativo

    positivo:
        not r1 r1      # Inverte todos os bits de R1
        add r3 r1      # Converte R1 para complemento de dois (negativo)
        jump soma      # Soma R0 + (-R1)

    negativo:
        not r0 r0      # Inverte todos os bits de R0
        add r3 r0      # Converte R0 para complemento de dois (negativo)
        out addr r3    # Ativa o monitor
        out data r2    # Exibe o sinal '-' no monitor
        jump soma      # Soma R1 + (-R0)

multiplica:
    data r2 0xff    # R2 = endereço temporário 0xFF
    st r2 r1        # Armazena R1 (segundo dígito) no endereço 0xFF

    data r3 1       # Inicializa contador R3 com 1

    cmp r0 r1       # Compara os dois operandos
    jz zero         # Se 'a' for 0, resultado é zero
    
    cmp r1 r0       # Compara os dois operandos
    jz zero         # Se 'b' for 0, resultado é zero
    jae a_vezes_b   # Se R1 >= R0, executa R1 somado R0 vezes

    st r2 r0        # Caso contrário, armazena R0 no endereço 0xFF
    data r2 0       # Zera R2
    add r0 r2       # Copia R0 para R2
    data r0 0       # Zera R0
    add r1 r0       # Copia R1 para R0
    data r1 0       # Zera R1
    add r2 r1       # Copia o valor de R0 antigo (agora em R2) para R1

    a_vezes_b:
        cmp r0 r3        # Verifica se já somou R1 R0 vezes
        je final          # Se sim, vai para impressão do resultado

        data r2 1
        add r2 r3         # Incrementa contador
        data r2 0xff
        ld r2 r2          # Carrega valor original de R1 de 0xFF
        add r2 r1         # Soma ao acumulador em R1
        jump a_vezes_b    # Repete até alcançar o número de repetições

    zero:
        data r1 0
        jump final

final:
    data r0 1         # R0 = 1 (para uso no contador)
    out addr r0       # Ativa o monitor
    data r2 0         # Zera R2 (vai armazenar as dezenas)
    data r3 10        # R3 = 10
    cmp r1 r3         # Verifica se resultado >= 10
    jae dezena        # Se sim, calcula dígito das dezenas
    jump unidade      # Caso contrário, imprime só unidade

dezena:
    add r0 r2         # Incrementa contador de dezenas
    data r3 246       # R3 = -10 (em complemento de dois)
    add r3 r1         # Subtrai 10 do valor total
    data r3 10        # R3 = 10 novamente
    cmp r1 r3         # Verifica se ainda >= 10
    jae dezena        # Repete se ainda houver dezenas a subtrair

    data r3 48        # R3 = '0' em ASCII
    add r3 r2         # Converte número de dezenas para ASCII
    out data r2       # Imprime o dígito das dezenas

unidade:
    data r3 48        # R3 = '0' em ASCII
    add r3 r1         # Converte valor de R1 para ASCII
    out data r1       # Imprime o dígito das unidades

encerra:
    jump encerra      # Loop infinito para encerrar o programa