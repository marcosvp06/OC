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

typedef struct DadoVertice{
  Cor cor;
  int distancia;
  int predecessor;
} DadoVertice;

typedef struct Grafo{
  bool** matrizAdj;
  int numVertices;
  int numArestas;
} Grafo;

void inicializa_grafo_matriz(Grafo* grafo, int numVertices);

void adiciona_aresta_grafo(Grafo* grafo, int origem, int destino);

void gera_arestas_aleatorias(Grafo* grafo, float grau_conexidade);

void bfs(Grafo* grafo, int inicial);

void mostra_grafo_matriz(Grafo grafo);

void mostra_vertices(Grafo grafo, DadoVertice* dadosVertices);

void libera_grafo(Grafo* grafo);

#endif