#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "grafo.h"
#include "lista.h"

int main(){
  srand(time(NULL));

  Grafo g1;
  inicializa_grafo_matriz(&g1, 30);
  gera_arestas_aleatorias(&g1, 0.25f);
  mostra_grafo_matriz(g1);
  bfs(&g1, 4);
  libera_grafo(&g1);
}
