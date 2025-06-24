data r0, 0xf9 ; R0 = inicial (0xf9)
xor r1, r1  ; R1 = final (0x00)
data r2, 1  ; R2 = incrementador de "inicial"
data r3, 10 ; Elemento inicial a ser inserido no vetor
cmp r0, r1  ; Compara "inicial" com "final"
je 0x0f ; Se forem iguais, termina o loop
st r0, r3 ; Armazena o elemento (R3) no endereço "inicial"
add r2, r0  ; inicial += 1
add r2, r3 ; Valor do elemento += 1
jmp 0x07 ; Repete o loop
data r0, 0xf9 ; R0 = inicial (0xf9)
data r1, 0xff ; R1 = final (0xff)
cmp r0, r1  ; Compara "inicial" com "final"
jae 0x25  ; Se "inicial" for maior ou igual que "final", terminou o swap
ld r0, r2 ; R2 = valor no endereço 'inicial'
ld r1, r3 ; R3 = valor no endereço 'final'
xor r2, r3
xor r3, r2  ; Faz a troca dos valores de R2 e R3
xor r2, r3
st r0, r2 ; Insere R2 no endereço 'inicial'
st r1, r3 ; Insere R3 no endereço 'final'
data r2, 1  ; R2 = incrementador de "inicial"
data r3, -1 ; R3 = incrementador de "final"
add r2, r0  ; inicial += 1
add r3, r1  ; final -= 1
jmp 0x13  ; Repete o loop
jmp 0x25  ; Finaliza o programa num loop