#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "grafo.h"
#include "lista.h"

#define NUM_VERTICES 30

int main(){
  srand(time(NULL));

  Grafo g1;
  inicializa_grafo_matriz(&g1, NUM_VERTICES);
  gera_arestas_aleatorias(&g1, 0.5f);
  mostra_grafo_matriz(g1);

  ArvoreBFS arvore = bfs(&g1, 2);
  mostra_arvore_bfs(arvore);

  Lista seq = dfs(&g1, 4);
  mostra_sequencia_dfs(seq);

  printf("Todos os caminhos a partir do vertice 0:\n");
  //mostra_todos_caminhos(&g1, 0);

  if(possui_ciclo(&g1, 0)){
    printf("O grafo possui ciclo.\n");
  }
  else {
    printf("O grafo NAO possui ciclo.\n");
  }

  libera_arvore_bfs(&arvore, g1.numVertices);
  libera_lista(&seq);
  libera_grafo(&g1);
}
