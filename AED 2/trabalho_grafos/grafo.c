#include <stdio.h>
#include <stdlib.h>
#include "grafo.h"
#include "fila.h"

void inicializa_grafo_matriz(Grafo* grafo, int numVertices){
  grafo->dadosVertices = (DadoVertice*) malloc(sizeof(DadoVertice) * numVertices);
  grafo->matrizAdj = (Bool**) malloc(sizeof(Bool*) * numVertices);
  for (int i = 0; i < numVertices; i++){
    grafo->matrizAdj[i] = (Bool*) malloc(sizeof(Bool) * numVertices);
    for (int j = 0; j < numVertices; j++){
      grafo->matrizAdj[i][j] = False;
    }
    DadoVertice dado;
    dado.cor = Branco;
    dado.distancia = -1;
    dado.predecessor = -1;
    grafo->dadosVertices[i] = dado;
  }
  grafo->numVertices = numVertices;
  grafo->numArestas = 0;
}

void adiciona_aresta_grafo(Grafo* grafo, int origem, int destino){
  grafo->matrizAdj[origem][destino] = True;
  grafo->matrizAdj[destino][origem] = True;
  grafo->numArestas++;
}

void gera_arestas_aleatorias(Grafo* grafo, float grau_conexidade){
  int numVertices = grafo->numVertices;
  int arestas = (int) (grau_conexidade * numVertices * (numVertices - 1)) / 2;
  printf("Arestas esperadas: %d\n", arestas);

  if (arestas < numVertices - 1) return;

  int *vertices = (int *)malloc(sizeof(int) * numVertices);

  for (int i = 0; i < numVertices; i++){
    vertices[i] = i;
  }

  int temp;
  for (int i = numVertices - 1; i > 0; i--){
    int j = rand() % (i + 1);
    temp = vertices[i];
    vertices[i] = vertices[j];
    vertices[j] = temp;
  }

  for (int i = 0; i < numVertices - 1; i++){
    adiciona_aresta_grafo(grafo, vertices[i], vertices[i + 1]);
    arestas--;
  }
  printf("Arestas depois de tornar conexo: %d\n", grafo->numArestas);
  printf("Arestas esperadas restantes: %d\n", arestas);

  int origem, destino;
  while (arestas > 0){
    origem = rand() % numVertices;
    destino = rand() % numVertices;
    if (origem != destino && grafo->matrizAdj[origem][destino] == False){
      adiciona_aresta_grafo(grafo, origem, destino);
      printf("Vértices %d e %d conectados.\n", origem, destino);
      arestas--;
    }
  }
}

void bfs(Grafo* grafo, int inicial){

  grafo->dadosVertices[inicial].cor = Cinza;
  grafo->dadosVertices[inicial].distancia = 0;
  grafo->dadosVertices[inicial].predecessor = -1;

  Fila fila;
  inicializa_fila(&fila);
  enfila(&fila, inicial);

  while (fila.inicio){
    int atual = fila.inicio->dado;
    for (int j = 0; j < grafo->numVertices; j++){

      if (grafo->matrizAdj[atual][j] == True &&
         grafo->dadosVertices[j].cor == Branco){

        grafo->dadosVertices[j].cor = Cinza;
        grafo->dadosVertices[j].distancia = grafo->dadosVertices[atual].distancia + 1;
        grafo->dadosVertices[j].predecessor = atual;
        enfila(&fila, j);
      }
    }
    desenfila(&fila);
    grafo->dadosVertices[atual].cor = Preto;
  }
}

void mostra_grafo_matriz(Grafo grafo){
  for (int i = 0; i < grafo.numVertices; i++){
    for (int j = 0; j < grafo.numVertices; j++){
      printf("%d ", grafo.matrizAdj[i][j]);
    }
    printf("\n");
  }
  printf("Número de arestas: %d\n\n", grafo.numArestas);
}

void mostra_vertices(Grafo grafo){
  char* cores[3] = {"branco", "cinza", "preto"};
  int maior = grafo.dadosVertices[0].distancia;
  for (int i = 0; i < grafo.numVertices; i++){
    DadoVertice dado = grafo.dadosVertices[i];
    printf("--- Vértice: %d ---\n", i);
    printf("Cor: %s\n", cores[dado.cor]);
    printf("Distância: %d\n", dado.distancia);
    printf("Predecessor: %d\n", dado.predecessor);
    printf("\n");
    if (dado.distancia > maior){
      maior = dado.distancia;
    }
  }
  printf("Maior distância: %d\n", maior);
  printf("\n");
}

void libera_grafo(Grafo* grafo){
  for (int i = 0; i < grafo->numVertices; i++){
    free(grafo->matrizAdj[i]);
  }
  free(grafo->matrizAdj);
  free(grafo->dadosVertices);

  grafo->dadosVertices = NULL;
  grafo->matrizAdj = NULL;
  grafo->numArestas = 0;
  grafo->numVertices = 0;
}