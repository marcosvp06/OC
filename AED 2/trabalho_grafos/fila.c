#include <stdlib.h>
#include "fila.h"

void inicializa_fila(Fila* fila){
  fila->inicio = NULL;
  fila->final == NULL;
  fila->tamanho = 0;
}

void enfila(Fila* fila, int valor){
  TipoNo *novo = (TipoNo *)malloc(sizeof(TipoNo));
  novo->dado = valor;
  if (fila->tamanho){
    fila->final->prox = novo;
  }
  else{
    fila->inicio = novo;
  }
  fila->final = novo;
  fila->tamanho++;
}

void desenfila(Fila *fila){
  if (fila->tamanho){
    TipoNo* aux = fila->inicio;
    if (fila->tamanho == 1)
    {
      fila->final = NULL;
    }
    fila->inicio = aux->prox;
    free(aux);
    fila->tamanho--;
  }
}

void libera_fila(Fila* fila){
  while(fila->inicio){
    desenfila(fila);
  }
}