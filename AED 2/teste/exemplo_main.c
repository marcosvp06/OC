#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "grafo.h"
#include "lista.h"

#define NUM_VERTICES 10

int main(){
  srand(time(NULL));

  Grafo g1;
  inicializa_grafo_matriz(&g1, NUM_VERTICES);
  gera_arestas_aleatorias(&g1, 0.25f);
  mostra_grafo_matriz(g1);
  
  int v_exemplo = 3;
  ArvoreBFS arvore = bfs(&g1, v_exemplo);
  mostra_arvore_bfs(arvore);

  Lista sequencia_vertices_dfs = dfs(&g1, v_exemplo);
  mostra_sequencia_dfs(sequencia_vertices_dfs);
  mostra_todos_caminhos(&g1, v_exemplo);

  if(possui_ciclo(&g1, 0)){
    printf("O grafo possui ciclo.\n\n");
  }
  else {
    printf("O grafo NAO possui ciclo.\n\n");
  }

  libera_arvore_bfs(&arvore, g1.numVertices);
  libera_lista(&sequencia_vertices_dfs);
  libera_grafo(&g1);
}