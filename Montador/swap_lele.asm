data r0, 0xf9

data r1, 0x00

data r2, 8

data r3, 1

cmp r0, r1
je 0x0f

st r0, r0
add r3, r0
jmp 0x08

data r0, 0xf9

data r1, 0xff

cmp r0, r1
jae 37

ld r0, r2
ld r1, r3
xor r2, r3
xor r3, r2
xor r2, r3
st r0, r2
st r1, r3
data r3, 1

add r3, r0
data r2, -1

add r2, r1
jmp 19

jmp 37