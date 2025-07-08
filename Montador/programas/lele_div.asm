; Aluna: Leticia Souza de Souza
; Matricula: 22450212

; limpa os registradores
clr r0
clr r1
clr r2
clr r3
; entra na sub-rotina de leitura
jmp leitura_teclado

errado:
  data r0, 1
  out addr, r0  ; liga o monitor
  data r0, 63   ; valor de '?'
  out data, r0
  jmp encerra  ; pula para o halt

leitura_teclado:
  out addr, r0  ; liga o teclado
  in data, r0
  in data, r1
  data r2, 47 ; valor de '/'
  data r3, -48  ; valor de -'0'
  cmp r1, r2
  je sem_dezenas  ; se tem apenas um digito no dividendo, entao sem dezenas
  add r3, r0    ; transforma dezenas em inteiro
  add r3, r1  ; transforma unidades em inteiro
  jmp vezes10 ; multiplica as dezenas por 10
  vezes10:
    shl r0, r2
    shl r0, r0
    shl r0, r0
    shl r0, r0
    add r2, r0  ; resultado vezes 10 fica no r0
  add r1, r0  ; dividendo = 10*dezenas + unidades
  in data, r1
  data r2, 47 ; valor de '/'
  cmp r1, r2
  je continua ; continua se foi digitado '/'
  jmp errado
  sem_dezenas: add r3, r0 ; transforma resultado para inteiro
  continua:
    in data, r1
    add r3, r1  ; transforma o divisor em inteiro
    jmp divide  ; pula para a sub-rotina de divisao

divide:
  cmp r1, r1
  jz errado ; divisao por 0 -> erro
  clr r2  ; quociente
  data r3, 1
  subtracao:
    cmp r0, r1
    jae subtrai   ; se dividendo maior ou igual que divisor -> subtrai
    jmp fim_divisao
    subtrai:
      not r1, r1
      add r3, r1
      add r1, r0  ; dividendo -= divisor
      add r3, r2  ; quociente += 1
      not r1, r1
      add r3, r1  ; dividendo = dividendo
      jmp subtracao ; loop
  fim_divisao:
    move r2, r1 ; quociente fica em r1
    jmp exibe ; entra na sub-rotina de exibicao da resposta

exibe:
    data r0, 1
    out addr, r0  ; liga o monitor
    clr r2  ; dezenas = 0
    data r3, 10
    cmp r1, r3
    jae dezenas  ; se resultado >= 10, calcula digito das dezenas
    jmp unidades ; senao, exibe so a unidade
    dezenas:
      add r0, r2  ; dezenas += 1
      data r3, -10
      add r3, r1  ; resultado -= 10
      data r3, 10
      cmp r1, r3  ; resultado ainda >= 10 ?
      jae dezenas  ; loop

      data r3, 48 ; valor de '0'
      add r3, r2  ; transforma as dezenas para ascii
      out data, r2  ; exibe as dezenas no monitor
      jmp unidades

    unidades:
      data r3, 48 ; valor de '0'
      add r3, r1  ; transforma as unidades para ascii
      out data, r1  ; exibe as unidades no monitor
      jmp encerra

encerra: halt ; encerra o programa