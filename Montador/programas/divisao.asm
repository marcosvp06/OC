jmp main ; Programa inicia na main

; Trata casos de erro mostrando '?' no monitor e encerrando o programa
caso_de_erro:
  data r0, 1    ; Seta R0 para 0x01
  out addr, r0  ; Seleciona o monitor (Endereco 0x01)
  data r0, 63   ; Guarda em R0 o valor de '?' em ascii
  out data, r0  ; Mostra '?' no monitor
  jmp _halt_    ; Encerra o programa

; Realiza a leitura do teclado no formato "dividendo/divisor"
; O dividendo deve possuir 2 digitos, o divisor 1 digito
; Guarda (como valores inteiros) o dividendo em R0, e o divisor em R1
leitura:
  clr r0  ; Limpa R0 para 0x00
  out addr, r0  ; Seleciona o teclado (Endereco 0x00)

  in data, r0 ; Le do teclado o digito das dezenas do dividendo
  in data, r1 ; Le do teclado o digito das unidades do dividendo

  data r3, -48  ; Oposto do valor do ascii '0' (Em complemento de dois)
  add r3, r0    ; Converte o digito das dezenas para inteiro subtraido '0'
  add r3, r1  ; Converte o digito das unidades para inteiro subtraido '0'

  jmp multiplica_10 ; Multiplica o digito das dezenas por 10 (guardado em R0)
  return_multi:

  add r1, r0  ; Soma as unidades com as dezenas do dividendo

  in data, r1 ; Le do teclado o simbolo '/' da divisao inteira
  data r2, 47 ; Guarda em R2 o valor de '/' em ascii
  cmp r1, r2  ; Compara o simbolo digitado com '/'
  je operacao_valida  ; Se forem iguais, a operacao e valida
  jmp caso_de_erro  ; Caso contrario, trata como erro

  operacao_valida:
    in data, r1 ; Le do teclado o digito das unidades do divisor
    add r3, r1  ; Converte o divisor para inteiro subtraido '0'
    jmp return_leitura  ; Finaliza a leitura

; Multiplica o valor contido em R0 por 10, e guarda em R0
multiplica_10:
  move r0, r2 ; Copia o valor de R0 em R2
  shl r2, r2  ; Multiplica o valor de R2 por 2 (R3 = 2*valor)
  shl r0, r0
  shl r0, r0  ; Multiplica o valor de R0 por 8 (R0 = 8*valor)
  shl r0, r0
  add r2, r0  ; Soma R2 em R0 (R0 = 8*valor + 2*valor == 10*valor)
  jmp return_multi

; Realiza a divisao inteira entre um dividendo (R0) e um divisor (R1)
; Guarda (como inteiros) o quociete em R0 e o resto em R1
divisao_inteira:
  cmp r1, r1  ; Compara o divisor com ele proprio
  jz caso_de_erro ; Se divisor for zero, trata como erro

  clr r2      ; Inicializando o contador em R2 (quociente = 0)
  data r3, 1  ; Incrementador do contador

  loop_:
    cmp r0, r1    ; Compara o dividendo com o divisor
    jae faz_div   ; Enquanto dividendo >= divisor, faz a divisao
    jmp fim_loop  ; Caso contrario, encerra o loop
    faz_div:
      not r1, r1
      add r3, r1  ; Obtendo o complemento de 2 do divisor (-1 * divisor)
      add r1, r0  ; Subtrai divisor do dividendo (R0 = R0 - R1)
      add r3, r2  ; Incrementa 1 no contador (quociente++)
      not r1, r1
      add r3, r1  ; Divisor volta a ser positivo ( (-1)*(-1)*divisor )
      jmp loop_   ; Repete o loop

  fim_loop: move r0, r1 ; Copia o resto para R1
  move r2, r0 ; Copia o quociente para R0

  data r3, 0xff ; Seta em R3 o endereco 0xff
  ld r3, r3 ; Carrega da memoria (em 0xff) o valor correspondente ao endereco da ultima chamada da divisao_inteira
  jmpr r3  ; Finaliza a divisao retornando para depois de onde foi chamada

; Exibe no monitor um valor inteiro (em R0) entre 0 e 99 (com dois digitos)
mostra_resultado:
  data r1, 10 ; Dividendo = R0 / Divisor = 10

  data r2, 0xff ; Seta em R2 o endereco 0xff
  data r3, 0x4e ; Seta em R3 o endereco 0x4e
  st r2, r3 ; Armazena na memoria (em 0xff) o endereco de retorno dessa chamada da divisao_inteira (0x4e)
  jmp divisao_inteira ; Quociente (R0) = dezenas / Resto (R1) = unidades
  ; endereco de retorno == 0x62

  data r2, 48 ; Guarda em R2 o valor de '0' em ascii
  add r2, r0  ; Converte o digito das dezenas para ascii somando '0'
  add r2, r1  ; Converte o digito das unidades para ascii somando '0'

  data r3, 1    ; Seta R3 para 0x01
  out addr, r3  ; Seleciona o monitor (Endereco 0x01)
  out data, r0  ; Exibe o digito das dezenas no monitor
  out data, r1  ; Exibe o digito das unidades no monitor
  jmp return_mostra

main:
  jmp leitura
  return_leitura:

  data r2, 0xff ; Seta em R2 o endereco 0xff
  data r3, 0x62 ; Seta em R3 o endereco 0x62
  st r2, r3 ; Armazena na memoria (em 0xff) o endereco de retorno dessa chamada da divisao_inteira (0x62)
  jmp divisao_inteira
  ; endereco de retorno == 0x62

  jmp mostra_resultado
  return_mostra:

  _halt_: halt