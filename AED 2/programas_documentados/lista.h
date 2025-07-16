#ifndef LISTA_H_INCLUDED
#define LISTA_H_INCLUDED

#include <stdlib.h>
#include <stdio.h>

/**
 * @struct NoLista
 * @brief Estrutura de um nó da lista encadeada.
 */
typedef struct NoLista {
    int dado;               ///< Valor armazenado no nó
    struct NoLista* prox;   ///< Ponteiro para o próximo nó
} NoLista;

/**
 * @struct Lista
 * @brief Lista encadeada com ponteiros para o primeiro e último elementos.
 * @param prim Ponteiro para o primeiro nó da lista
 * @param ult Ponteiro para o último nó da lista
 * @param tamanho Quantidade de elementos na lista
 * @
 */
typedef struct Lista {
    NoLista* prim;
    NoLista* ult;
    int tamanho;
} Lista;

/**
 * @brief Inicializa uma lista vazia.
 * @param lista Ponteiro para a lista a ser inicializada.
 */
void inicializa_lista(Lista* lista);

/**
 * @brief Cria um novo nó com o valor fornecido.
 * @param valor Valor a ser armazenado.
 * @return Ponteiro para o novo nó criado.
 */
NoLista* cria_no(int valor);

/**
 * @brief Insere um valor no final da lista.
 * @param lista Ponteiro para a lista.
 * @param valor Valor a ser inserido.
 */
void insere_final(Lista* lista, int valor);

/**
 * @brief Remove o último elemento da lista.
 * @param lista Ponteiro para a lista.
 */
void remove_final(Lista* lista);

/**
 * @brief Enfileira um valor no final da lista (fila).
 * @param lista Ponteiro para a lista.
 * @param valor Valor a ser enfileirado.
 */
void enfila(Lista* lista, int valor);

/**
 * @brief Desenfileira (remove) o primeiro elemento da lista (fila).
 * @param lista Ponteiro para a lista.
 */
void desenfila(Lista* lista);

/**
 * @brief Empilha um valor no início da lista (pilha).
 * @param lista Ponteiro para a lista.
 * @param valor Valor a ser empilhado.
 */
void empilha(Lista* lista, int valor);

/**
 * @brief Desempilha (remove) o elemento do topo da pilha (início da lista).
 * @param lista Ponteiro para a lista.
 */
void desempilha(Lista* lista);

/**
 * @brief Libera toda a memória alocada pela lista.
 * @param lista Ponteiro para a lista.
 */
void libera_lista(Lista* lista);

#endif