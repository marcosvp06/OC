#ifndef LISTA_H_INCLUDED
#define LISTA_H_INCLUDED

#include <stdlib.h>
#include <stdio.h>

typedef struct NoLista{
    int dado;
    struct NoLista* prox;
} NoLista;

typedef struct Lista{
    NoLista* prim;
    NoLista* ult;
    int tamanho;
} Lista;

void inicializa_lista(Lista* lista);

NoLista* cria_no(int valor);

void insere_final(Lista* lista, int valor);

void remove_final(Lista* lista);

void enfila(Lista* lista, int valor);

void desenfila(Lista* lista);

void empilha(Lista* lista, int valor);

void desempilha(Lista* lista);

void libera_lista(Lista* lista);

#endif