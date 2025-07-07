clr r3, r3 ;  Inicializa a stack
jmp main

soma:
  data r2, 0xa0
  data r1, 0xa1
  ld r2, r0
  ld r1, r1
  add r1, r0
  st r2, r0

  ld r3, r2 ; puxa o endereco do topo
  data r1, 1
  add r1, r3  ; desce na stack
  jmpr r2 ; pula para onde foi chamado

main:
  data r0, 0xa0
  data r1, 3
  st r0, r1
  data  r0, 0xa1
  data r1, 2
  st r0, r1


  data r1, -1
  add r1, r3  ; subiu na stack
  data r2, chamada1
  data r1, 3
  add  r1, r2 ; endereco a ser adicionado na stack
  st r3, r2 ; adiciona na stack

  chamada1:
  jmp soma

  chamada2:
  data r1, -1
  add r1, r3  ; subiu na stack
  data r2, chamada2
  data r1, 11
  add  r1, r2 ; endereco a ser adicionado na stack
  st r3, r2 ; adiciona na stack
  jmp soma

  chamada3:
  data r1, -1
  add r1, r3  ; subiu na stack
  data r2, chamada3
  data r1, 11
  add  r1, r2 ; endereco a ser adicionado na stack
  st r3, r2 ; adiciona na stack
  jmp soma

  data r1, 0xa0
  ld r1, r0
  halt