#include "lista.h"

void inicializa_lista(Lista* lista){
    lista->prim = NULL;
    lista->ult = NULL;
    lista->tamanho = 0;
}

NoLista* cria_no(int valor){
    NoLista* aux = malloc(sizeof(NoLista));
    aux->dado = valor;
    aux->prox = NULL;
    return aux;
}

void insere_final(Lista* lista, int valor){
    NoLista* novo = cria_no(valor);
    if (lista->tamanho){
        lista->ult->prox = novo;
    }
     else{
        lista->prim = novo;
    }
    lista->ult = novo;
    lista->tamanho++;
}

void enfila(Lista* lista, int valor){
  NoLista *novo = cria_no(valor);
  if (lista->tamanho){
    lista->ult->prox = novo;
  }
  else{
    lista->prim = novo;
  }
  lista->ult = novo;
  lista->tamanho++;
}

void desenfila(Lista *lista){
  if (lista->tamanho){
    NoLista* aux = lista->prim;
    if (lista->tamanho == 1)
    {
      lista->ult = NULL;
    }
    lista->prim = aux->prox;
    free(aux);
    lista->tamanho--;
  }
}

void empilha(Lista* lista, int valor){
    NoLista* novo = cria_no(valor);
    if (!lista->tamanho){
        lista->ult = novo;
    }
    novo->prox = lista->prim;
    lista->prim = novo;
}

void desempilha(Lista* lista){
    if (lista->tamanho){
        NoLista* aux = lista->prim;
        if (lista->tamanho == 1){
            lista->ult = NULL;
        }
        lista->prim = aux->prox;
        free(aux);
        lista->tamanho--;
  }
}

void libera_lista(Lista* lista){
  while(lista->prim){
    desempilha(lista);
  }
}