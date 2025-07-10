#ifndef FILA_H_INCLUDED
#define FILA_H_INCLUDED

typedef struct TipoNo{
  int dado;
  struct TipoNo* prox;
} TipoNo;

typedef struct Fila{
  TipoNo* inicio;
  TipoNo* final;
  int tamanho;
} Fila;

void inicializa_fila(Fila* fila);

void enfila(Fila* fila, int valor);

void desenfila(Fila* fila);

void libera_fila(Fila* fila);

#endif