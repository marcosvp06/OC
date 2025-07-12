#include "grafo.h"

void inicializa_grafo_matriz(Grafo* grafo, int numVertices){
  grafo->matrizAdj = (bool**) malloc(sizeof(bool*) * numVertices);
  for (int i = 0; i < numVertices; i++){
    grafo->matrizAdj[i] = (bool*) malloc(sizeof(bool) * numVertices);
    for (int j = 0; j < numVertices; j++){
      grafo->matrizAdj[i][j] = false;
    }
  }
  grafo->numVertices = numVertices;
  grafo->numArestas = 0;
}

void inicializa_cores(Cor* cores, int tamanho){
  for (int i = 0; i < tamanho; i++){
    cores[i] = Branco;
  }
}

void inicializa_caminhos(Lista* caminhos, int tamanho){
  for (int i = 0; i < tamanho; i++){
    inicializa_lista(&caminhos[i]);
  }
}

void adiciona_aresta_grafo(Grafo* grafo, int origem, int destino){
  grafo->matrizAdj[origem][destino] = true;
  grafo->matrizAdj[destino][origem] = true;
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
    if (origem != destino && grafo->matrizAdj[origem][destino] == false){
      adiciona_aresta_grafo(grafo, origem, destino);
      printf("Vertices %d e %d conectados.\n", origem, destino);
      arestas--;
    }
  }
}

void bfs(Grafo* grafo, int inicial){
  Cor* cores = malloc(sizeof(Cor) * grafo->numVertices);
  inicializa_cores(cores, grafo->numVertices);
  Lista* caminhos = malloc(sizeof(Lista) * grafo->numVertices);
  inicializa_caminhos(caminhos, grafo->numVertices);
  int* distancias = malloc(sizeof(int) * grafo->numVertices);

  cores[inicial] = Cinza;
  distancias[inicial] = 0;
  insere_final(&caminhos[inicial], inicial);

  Lista fila;
  inicializa_lista(&fila);
  enfila(&fila, inicial);

  while (fila.prim){
    int atual = fila.prim->dado;
    for (int j = 0; j < grafo->numVertices; j++){

      if (grafo->matrizAdj[atual][j] == true &&
        cores[j] == Branco){

        cores[j] = Cinza;
        distancias[j] = distancias[atual] + 1;
        insere_final(&caminhos[j], atual);
        enfila(&fila, j);
      }
    }
    desenfila(&fila);
    cores[atual] = Preto;
  }
}

void mostra_grafo_matriz(Grafo grafo){
  for (int i = 0; i < grafo.numVertices; i++){
    for (int j = 0; j < grafo.numVertices; j++){
      printf("%d ", grafo.matrizAdj[i][j]);
    }
    printf("\n");
  }
  printf("Numero de arestas: %d\n\n", grafo.numArestas);
}

void mostra_vertices(Grafo grafo, DadoVertice* dadosVertices){
  char* cores[3] = {"branco", "cinza", "preto"};
  int maior = dadosVertices[0].distancia;
  for (int i = 0; i < grafo.numVertices; i++){
    DadoVertice dado = dadosVertices[i];
    printf("--- Vertice: %d ---\n", i);
    printf("Cor: %s\n", cores[dado.cor]);
    printf("Distancia: %d\n", dado.distancia);
    printf("Predecessor: %d\n", dado.predecessor);
    printf("\n");
    if (dado.distancia > maior){
      maior = dado.distancia;
    }
  }
  printf("Maior distancia: %d\n", maior);
  printf("\n");
}

void libera_grafo(Grafo* grafo){
  for (int i = 0; i < grafo->numVertices; i++){
    free(grafo->matrizAdj[i]);
  }
  free(grafo->matrizAdj);

  grafo->matrizAdj = NULL;
  grafo->numArestas = 0;
  grafo->numVertices = 0;
}