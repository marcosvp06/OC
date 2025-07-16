#ifndef FILA_H_INCLUDED
#define FILA_H_INCLUDED

#include <stdlib.h>

typedef struct NoFila{
  int dado;
  struct NoFila* prox;
} NoFila;

typedef struct Fila{
  NoFila* inicio;
  NoFila* final;
  int tamanho;
} Fila;

void inicializa_fila(Fila* fila);

void enfila(Fila* fila, int valor);

void desenfila(Fila* fila);

void libera_fila(Fila* fila);

#endif