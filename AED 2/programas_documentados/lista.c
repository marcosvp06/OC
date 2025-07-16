#include "lista.h"

void inicializa_lista(Lista* lista) {
    lista->prim = NULL;
    lista->ult = NULL;
    lista->tamanho = 0;
}

/**
 * @brief Cria um novo nó contendo um valor.
 * @param valor Valor a ser armazenado no nó.
 * @return Ponteiro para o nó recém-criado.
 */
NoLista* cria_no(int valor) {
    NoLista* aux = malloc(sizeof(NoLista));
    aux->dado = valor;
    aux->prox = NULL;
    return aux;
}

/**
 * @brief Insere um novo valor no final da lista.
 * @param lista Ponteiro para a lista.
 * @param valor Valor a ser inserido.
 */
void insere_final(Lista* lista, int valor) {
    NoLista* novo = cria_no(valor);
    if (lista->tamanho) {
        lista->ult->prox = novo;
    } else {
        lista->prim = novo;
    }
    lista->ult = novo;
    lista->tamanho++;
}

/**
 * @brief Remove o último elemento da lista.
 * Se houver apenas um elemento, esvazia a lista.
 * @param lista Ponteiro para a lista.
 */
void remove_final(Lista* lista) {
    if (lista->tamanho == 0) return;

    if (lista->tamanho == 1) {
        free(lista->prim);
        lista->prim = NULL;
        lista->ult = NULL;
    } else {
        NoLista* atual = lista->prim;
        while (atual->prox != lista->ult) {
            atual = atual->prox;
        }
        free(lista->ult);
        atual->prox = NULL;
        lista->ult = atual;
    }
    lista->tamanho--;
}

/**
 * @brief Insere um valor no final da lista (modo fila).
 * @param lista Ponteiro para a lista.
 * @param valor Valor a ser inserido.
 */
void enfila(Lista* lista, int valor) {
    NoLista* novo = cria_no(valor);
    if (lista->tamanho) {
        lista->ult->prox = novo;
    } else {
        lista->prim = novo;
    }
    lista->ult = novo;
    lista->tamanho++;
}

/**
 * @brief Remove o primeiro elemento da lista (modo fila).
 * @param lista Ponteiro para a lista.
 */
void desenfila(Lista* lista) {
    if (lista->tamanho) {
        NoLista* aux = lista->prim;
        if (lista->tamanho == 1) {
            lista->ult = NULL;
        }
        lista->prim = aux->prox;
        free(aux);
        lista->tamanho--;
    }
}

/**
 * @brief Insere um valor no início da lista (modo pilha).
 * @param lista Ponteiro para a lista.
 * @param valor Valor a ser empilhado.
 */
void empilha(Lista* lista, int valor) {
    NoLista* novo = cria_no(valor);
    if (!lista->tamanho) {
        lista->ult = novo;
    }
    novo->prox = lista->prim;
    lista->prim = novo;
    lista->tamanho++;
}

/**
 * @brief Remove o elemento do topo da pilha (início da lista).
 * @param lista Ponteiro para a lista.
 */
void desempilha(Lista* lista) {
    if (lista->tamanho) {
        NoLista* aux = lista->prim;
        if (lista->tamanho == 1) {
            lista->ult = NULL;
        }
        lista->prim = aux->prox;
        free(aux);
        lista->tamanho--;
    }
}

/**
 * @brief Libera todos os nós da lista, esvaziando-a.
 * @param lista Ponteiro para a lista.
 */
void libera_lista(Lista* lista) {
    while (lista->prim) {
        desempilha(lista);
    }
}