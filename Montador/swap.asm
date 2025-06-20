xor r1, r1  ; R1 = 0 (endereço do teclado)
out addr, r1  ; Liga o teclado
data r0, 0xf9 ; 0xf9 -> 7 elementos
; R0 = inicio , R1 = fim (0x00)
data r2, 1  ; R2 = incrementador de R0 (inicio++)

cmp r0, r1  ; inicio == fim ?
je 14 ; Pula para fazer o swap do vetor

in data, r3 ; R3 = valor lido do teclado
st r0, r3 ; Armazena R3 no endereço 'inicio'
add r2, r0  ; inicio += 1
jmp 6 ; Repete o loop

data r0, 0xf9 ; R0 = inicio

data r1, 0xff ; R1 = fim

cmp r0, r1  ; inicio >= fim ?
jae 36  ; Pula para mostrar o vetor no terminal

ld r0, r2 ; R2 = valor no endereço 'inicio'
ld r1, r3 ; R3 = valor no endereço 'fim'
xor r2, r3
xor r3, r2  ; Troca os valores de R2 e R3
xor r2, r3
st r0, r2 ; Armazena R2 no endereço 'inicio'
st r1, r3 ; Armazena R3 no endereço 'fim'
data r2, 1  ; R2 = incrementador de R0 (inicio++)

data r3, -1 ; R3 = incrementador de R1 (fim--)

add r2, r0  ; inicio += 1
add r3, r1  ; fim -= 1
jmp 18  ; Repete o loop

data r0, 0xf9 ; R0 = inicio

data r1, 0  ; R1 = fim

out addr, r2  ; Liga o monitor (R2 == 1)
cmp r0, r1  ; inicio == fim ?
je 47 ; Encerra o programa

ld r0, r3 ; R3 = valor no endereço 'inicio'
out data, r3  ; Mostra o char R3 no terminal
add r2, r0  ; inicio += 1
jmp 41  ; Repete o loop

jmp 47  ; Programa encerrado