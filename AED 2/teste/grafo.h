#ifndef GRAFO_H_INCLUDED
#define GRAFO_H_INCLUDED

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "lista.h"

typedef int Cor;
#define Branco 0
#define Cinza 1
#define Preto 2

typedef struct Grafo{
  bool** matrizAdj;
  int numVertices;
  int numArestas;
} Grafo;

typedef struct {
    Lista* niveis;   // vetor de listas de vértices por nível
    int max_nivel;   // maior nível alcançado
} ArvoreBFS;

typedef struct {
    int vertice;
    int pai;
} ItemPilha;

void inicializa_grafo_matriz(Grafo* grafo, int numVertices);

void adiciona_aresta_grafo(Grafo* grafo, int origem, int destino);

void gera_arestas_aleatorias(Grafo* grafo, float grau_conexidade);

ArvoreBFS bfs(Grafo* grafo, int inicial);

void mostra_arvore_bfs(ArvoreBFS arvore);

void libera_arvore_bfs(ArvoreBFS* arvore, int numVertices);

// DFS: retorna uma lista com a sequência de vértices visitados
Lista dfs(Grafo* grafo, int inicial);

// Mostra a sequência de vértices visitados
void mostra_sequencia_dfs(Lista seq);

void mostra_todos_caminhos(Grafo* grafo, int inicial);

void busca_caminhos(Grafo* grafo, Lista* caminho, bool* visitado);

bool possui_ciclo(Grafo* grafo, int inicial);

void mostra_grafo_matriz(Grafo grafo);

void libera_grafo(Grafo* grafo);

#endif