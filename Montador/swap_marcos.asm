data r0, 0xf9 ; endereço do primeiro elemento do vetor

data r1, 0xff ; endereço do último elemento do vetor
              ; tamanho vetor = 0xff - 0xf9 + 1 = 7 elementos
data r2, 8  ; valor do primeiro elemento do vetor

data r3, 1  ; R3 é o incrementador de R0 e R2

cmp r0, r1  ; endereço atual > endereço final ?
ja 0x10  ; se sim, acabou de criar o vetor

st r0, r2 ; guarda o valor de R2 no endereço atual contido em R0
add r3, r0  ; incrementa 1 em R0 (endereço atual)
add r3, r2  ; incrementa 1 em R2 (valor atual)
jmp 0x08  ; repete o loop

data r0, 0xf9 ; endereço do primeiro elemento do vetor (inicio)
              ; R1 ainda possui endereço do último elemento (fim)
cmp r0, r1  ; inicio >= fim ?
jae 0x24  ; se sim, encerra o programa

ld r0, r2 ; carrega da memória (para R2) o valor no endereço 'inicio'
ld r1, r3 ; carrega da memória (para R3) o valor no endereço 'fim'
xor r2, r3
xor r3, r2  ; Troca os valores de R2 e R3
xor r2, r3
st r0, r2 ; armazena na memória o valor de R2 no endereço 'inicio'
st r1, r3 ; armazena na memória o valor de R3 no endereço 'fim'
data r2, -1 ; R2 vira o incrementador de 'fim'

data r3, 1 ; R3 vira o incrementador de 'inicio'

add r3, r0  ; incrementa 1 em 'inicio'
add r2, r1  ; incrementa -1 em 'fim'
jmp 0x12  ; repete o loop

jmp 0x24  ; encerra o programa