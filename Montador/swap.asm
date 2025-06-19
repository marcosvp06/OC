xor r0 r0
out addr r0
data r1 1

data r2 7

in data r3
st r0 r3
add r1 r0
cmp r0 r2
je 0x0e

jmp 0x06

codigo
data r1 -1
