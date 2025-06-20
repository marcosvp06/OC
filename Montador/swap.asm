xor r2, r2  ; R0 = 0
out addr, r2  ; Liga o teclado
data r0, 0xf9 ; 0xf9 = 7 elementos

data r1, 1  ; R1 = 1

cmp r0, r2
je 14

in data, r3
st r0, r3
add r1, r0
jmp 6

data r0, 0xf9

data r1, 0xff

cmp r0, r1
jae 36

ld r0, r2
ld r1, r3
xor r2, r3
xor r3, r2
xor r2, r3
st r0, r2
st r1, r3
data r2, 1

data r3, -1

add r2, r0
add r3, r1
jmp 18

data r0, 0xf9 ; 0xf9 = 7 elementos

data r1, 1  ; R1 = 1

data r2, 0

out addr, r1  ; liga o monitor
cmp r0, r2
je 51

ld r0, r3
out data, r3
add r1, r0
jmp 43

jmp 51