clr r0        ; Endereco do teclado
out addr, r0       ; Ativa o teclado

in data, r0        ; R0 recebe o primeiro dígito (em ASCII)
in data, r2        ; R2 recebe o caractere da operação (em ASCII)
in data, r1        ; R1 recebe o segundo dígito (em ASCII)

data r3, 1         ; Endereco do monitor
out addr, r3       ; Ativa o monitor

data r3, 48        ; R3 recebe o valor ASCII de '0'

xor r3, r0         ; Converte R0 de ASCII para inteiro
xor r3, r1         ; Converte R1 de ASCII para inteiro

data r3, 43        ; R3 recebe o valor ASCII de '+'
cmp r2, r3         ; Verifica se a operação é adição
je soma           ; Se sim, pula para o bloco de soma

data r3, 45        ; R3 recebe o valor ASCII de '-'
cmp r2, r3         ; Verifica se a operação é subtração
je subtrai        ; Se sim, pula para o bloco de subtração

data r3, 42       ; R3 recebe o valor ASCII de '*'
cmp r2, r3         ; Verifica se a operação é multiplicação
je multiplica     ; Se sim, pula para o bloco de multiplicação

data r3, 63        ; R3 recebe o valor ASCII de '?'
out data, r3       ; Exibe '?' no monitor
halt      ; Se a operação não for reconhecida, encerra o programa

soma:
    add r0, r1     ; Soma os dois dígitos (resultado vai para R1)
    jmp final     ; Vai para a parte final que imprime o resultado

subtrai:
    data r3, 1      ; R3 = 1, para usar no complemento de dois

    cmp r0, r1      ; Compara os dois dígitos
    jae positivo   ; Se R0 >= R1, executa R0 - R1
    jmp negativo  ; Caso contrário, executa R1 - R0 e exibe sinal de negativo

    positivo:
        not r1, r1      ; Inverte todos os bits de R1
        add r3, r1      ; Converte R1 para complemento de dois (negativo)
        jmp soma      ; Soma R0 + (-R1)

    negativo:
        not r0, r0      ; Inverte todos os bits de R0
        add r3, r0      ; Converte R0 para complemento de dois (negativo)
        out data, r2    ; Exibe o sinal '-' no monitor
        jmp soma      ; Soma R1 + (-R0)

multiplica:
    clr r2
    add r1, r2

    data r3, 1       ; Inicializa contador R3 com 1

    cmp r0, r1       ; Compara os dois operandos
    jz zero         ; Se 'a' for 0, resultado é zero

    cmp r1, r0       ; Compara os dois operandos
    jz zero         ; Se 'b' for 0, resultado é zero
    jae a_vezes_b   ; Se R1 >= R0, executa R1 somado R0 vezes

    xor r2, r2
    add r0, r2

    xor r0, r1
    xor r1, r0       ; Troca R0 com R1
    xor r0, r1

    a_vezes_b:
        cmp r0, r3        ; Verifica se já somou R1 R0 vezes
        je final          ; Se sim, vai para impressão do resultado

        data r3, -1
        add r3, r0
        add r2, r1
        data r3, 1

        jmp a_vezes_b    ; Repete até alcançar o número de repetições

    zero:
        clr r1
        jmp final

final:
    data r0, 1         ; R0 = 1 (para uso no contador)
    xor r2, r2         ; Zera R2 (vai armazenar as dezenas)
    data r3, 10        ; R3 = 10
    cmp r1, r3         ; Verifica se resultado >= 10
    jae dezena        ; Se sim, calcula dígito das dezenas
    jmp unidade      ; Caso contrário, imprime só unidade

dezena:
    add r0, r2         ; Incrementa contador de dezenas
    data r3, -10       ; R3 = -10
    add r3, r1         ; Subtrai 10 do valor total
    data r3, 10        ; R3 = 10 novamente
    cmp r1, r3         ; Verifica se ainda >= 10
    jae dezena        ; Repete se ainda houver dezenas a subtrair

    data r3, 48        ; R3 = '0' em ASCII
    add r3, r2         ; Converte número de dezenas para ASCII
    out data, r2       ; Imprime o dígito das dezenas

unidade:
    data r3, 48        ; R3 = '0' em ASCII
    add r3, r1         ; Converte valor de R1 para ASCII
    out data, r1       ; Imprime o dígito das unidades

encerra: halt      ; Loop infinito para encerrar o programa