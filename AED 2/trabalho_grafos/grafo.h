#ifndef GRAFO_H_INCLUDED
#define GRAFO_H_INCLUDED

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "lista.h"

// Definição das cores utilizadas nos algoritmos de busca
typedef int Cor;

#define Branco 0  ///< Vértice não visitado
#define Cinza  1  ///< Vértice descoberto (em processamento)
#define Preto  2  ///< Vértice totalmente processado

/**
 * @struct Grafo
 * @brief Representa um grafo não direcionado usando matriz de adjacência.
 */
typedef struct Grafo {
    bool** matrizAdj;  ///< Matriz de adjacência (numVertices x numVertices)
    int numVertices;   ///< Quantidade de vértices no grafo
    int numArestas;    ///< Quantidade de arestas no grafo
} Grafo;

/**
 * @struct ArvoreBFS
 * @brief Representa uma árvore de níveis gerada pela BFS.
 */
typedef struct {
    Lista* niveis;    ///< Vetor de listas, cada uma representando um nível
    int max_nivel;    ///< Maior nível visitado a partir da raiz
} ArvoreBFS;

/**
 * @struct ItemPilha
 * @brief Estrutura auxiliar para controle de pilha com relação pai-filho (ciclo).
 */
typedef struct {
    int vertice;  ///< Vértice atual
    int pai;      ///< Pai do vértice no caminho
} ItemPilha;

// ==== Inicialização do grafo ====

/**
 * @brief Inicializa a matriz de adjacência de um grafo vazio.
 * @param grafo Ponteiro para o grafo a ser inicializado.
 * @param numVertices Número de vértices.
 */
void inicializa_grafo_matriz(Grafo* grafo, int numVertices);

// ==== Manipulação de arestas ====

/**
 * @brief Adiciona uma aresta não-direcionada entre dois vértices.
 * @param grafo Ponteiro para o grafo.
 * @param origem Índice do vértice de origem.
 * @param destino Índice do vértice de destino.
 */
void adiciona_aresta_grafo(Grafo* grafo, int origem, int destino);

/**
 * @brief Gera aleatoriamente arestas para o grafo baseado em um grau de conexidade.
 * @param grafo Ponteiro para o grafo.
 * @param grau_conexidade Valor entre 0.0 e 1.0 indicando densidade de conexões.
 */
void gera_arestas_aleatorias(Grafo* grafo, float grau_conexidade);

/**
 * @brief Gera uma árvore aleatória (grafo conexo e sem ciclos).
 * @param grafo Ponteiro para o grafo.
 */
void gera_arvore_aleatoria(Grafo* grafo);

// ==== BFS ====

/**
 * @brief Executa a busca em largura (BFS) e gera uma árvore de níveis.
 * @param grafo Ponteiro para o grafo.
 * @param inicial Vértice de partida.
 * @return Estrutura contendo listas de níveis visitados.
 */
ArvoreBFS bfs(Grafo* grafo, int inicial);

/**
 * @brief Mostra na tela os níveis da árvore gerada pela BFS.
 * @param arvore Estrutura contendo os níveis visitados.
 */
void mostra_arvore_bfs(ArvoreBFS arvore);

/**
 * @brief Libera memória associada à árvore de BFS.
 * @param arvore Ponteiro para a árvore.
 * @param numVertices Quantidade de vértices (tamanho do vetor de níveis).
 */
void libera_arvore_bfs(ArvoreBFS* arvore, int numVertices);

// ==== DFS (Iterativa e Recursiva) ====

/**
 * @brief Executa a busca em profundidade (DFS) de forma iterativa.
 * @param grafo Ponteiro para o grafo.
 * @param inicial Vértice de partida.
 * @return Lista com a sequência de visita dos vértices.
 */
Lista dfs_iterativa(Grafo* grafo, int inicial);

/**
 * @brief Executa a busca em profundidade (DFS) recursiva.
 * @param grafo Ponteiro para o grafo.
 * @param inicial Vértice de partida.
 * @return Lista com a sequência de visita dos vértices.
 */
Lista dfs(Grafo* grafo, int inicial);

/**
 * @brief Função auxiliar recursiva da DFS.
 * @param grafo Ponteiro para o grafo.
 * @param atual Vértice atual sendo visitado.
 * @param cores Vetor de marcação de cores dos vértices.
 * @param sequencia Ponteiro para a lista de visita.
 */
void dfs_visita(Grafo* grafo, int atual, Cor* cores, Lista* sequencia);

/**
 * @brief Imprime a sequência de vértices visitados pela DFS.
 * @param seq Lista com a ordem de visita.
 */
void mostra_sequencia_dfs(Lista seq);

// ==== Caminhos e Ciclos ====

/**
 * @brief Mostra todos os caminhos possíveis a partir de um vértice.
 * @param grafo Ponteiro para o grafo.
 * @param inicial Vértice de origem.
 */
void mostra_todos_caminhos(Grafo* grafo, int inicial);

/**
 * @brief Função recursiva para busca de todos os caminhos (auxiliar).
 * @param grafo Ponteiro para o grafo.
 * @param caminho Ponteiro para o caminho atual.
 * @param visitado Vetor de marcação de vértices visitados.
 */
void busca_caminhos(Grafo* grafo, Lista* caminho, bool* visitado);

/**
 * @brief Verifica se o grafo possui ciclos utilizando DFS.
 * @param grafo Ponteiro para o grafo.
 * @param inicial Vértice inicial da busca.
 * @return true se há ciclo, false caso contrário.
 */
bool possui_ciclo(Grafo* grafo, int inicial);

// ==== Utilidades ====

/**
 * @brief Imprime a matriz de adjacência do grafo.
 * @param grafo Estrutura do grafo.
 */
void mostra_grafo_matriz(Grafo grafo);

/**
 * @brief Libera toda a memória alocada pelo grafo.
 * @param grafo Ponteiro para o grafo.
 */
void libera_grafo(Grafo* grafo);

#endif