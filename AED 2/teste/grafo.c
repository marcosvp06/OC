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

  if (arestas < numVertices - 1){
    printf("Impossivel gerar um grafo conexo, faltam arestas.\n");
  }

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

  int origem, destino;
  while (arestas > 0){
    origem = rand() % numVertices;
    destino = rand() % numVertices;
    if (origem != destino && grafo->matrizAdj[origem][destino] == false){
      adiciona_aresta_grafo(grafo, origem, destino);
      arestas--;
    }
  }
}

ArvoreBFS bfs(Grafo* grafo, int inicial){
    Cor* cores = malloc(sizeof(Cor) * grafo->numVertices);
    inicializa_cores(cores, grafo->numVertices);

    int* distancias = malloc(sizeof(int) * grafo->numVertices);
    for(int i = 0; i < grafo->numVertices; i++)
        distancias[i] = -1; // -1 indica que não foi visitado

    ArvoreBFS arvore;
    arvore.niveis = malloc(sizeof(Lista) * grafo->numVertices);
    arvore.max_nivel = 0;

    for(int i = 0; i < grafo->numVertices; i++)
        inicializa_lista(&arvore.niveis[i]);

    cores[inicial] = Cinza;
    distancias[inicial] = 0;
    insere_final(&arvore.niveis[0], inicial);

    Lista fila;
    inicializa_lista(&fila);
    enfila(&fila, inicial);

    while(fila.prim){
        int atual = fila.prim->dado;

        for(int j = 0; j < grafo->numVertices; j++){
            if(grafo->matrizAdj[atual][j] && cores[j] == Branco){
                cores[j] = Cinza;
                distancias[j] = distancias[atual] + 1;

                // inserir no nível correspondente
                insere_final(&arvore.niveis[ distancias[j] ], j);

                // atualizar max_nivel
                if(distancias[j] > arvore.max_nivel)
                    arvore.max_nivel = distancias[j];

                enfila(&fila, j);
            }
        }

        desenfila(&fila);
        cores[atual] = Preto;
    }

    free(cores);
    free(distancias);
    libera_lista(&fila);

    return arvore;
}

void mostra_arvore_bfs(ArvoreBFS arvore){
  printf("Arvore resultante da BFS:\n");
    for(int nivel = 0; nivel <= arvore.max_nivel; nivel++){
        printf("Nivel %d: ", nivel);
        NoLista* no = arvore.niveis[nivel].prim;
        while(no){
            printf("%d ", no->dado);
            no = no->prox;
        }
        printf("\n");
    }
  printf("\n");
}

void libera_arvore_bfs(ArvoreBFS* arvore, int numVertices){
    for(int i = 0; i < numVertices; i++){
        libera_lista(&arvore->niveis[i]);
    }
    free(arvore->niveis);
    arvore->niveis = NULL;
    arvore->max_nivel = 0;
}

Lista dfs(Grafo* grafo, int inicial){
    Cor* cores = malloc(sizeof(Cor) * grafo->numVertices);
    inicializa_cores(cores, grafo->numVertices);

    Lista sequencia; // vai guardar a ordem dos vértices visitados
    inicializa_lista(&sequencia);

    Lista pilha;
    inicializa_lista(&pilha);
    empilha(&pilha, inicial);

    while(pilha.prim){
        int atual = pilha.prim->dado;
        desempilha(&pilha);

        if(cores[atual] == Branco){
            cores[atual] = Preto; // marca como visitado (já que não vai voltar nele)
            insere_final(&sequencia, atual);

            // empilhar os vizinhos (em ordem decrescente para visitar em ordem crescente)
            for(int j = grafo->numVertices - 1; j >= 0; j--){
                if(grafo->matrizAdj[atual][j] && cores[j] == Branco){
                    empilha(&pilha, j);
                }
            }
        }
    }

    free(cores);
    libera_lista(&pilha);

    return sequencia;
}

void mostra_sequencia_dfs(Lista sequencia){
    printf("Sequencia de vertices visitados na DFS:\n");
    NoLista* no = sequencia.prim;
    while(no){
        printf("%d ", no->dado);
        no = no->prox;
    }
    printf("\n\n");
}

void mostra_todos_caminhos(Grafo* grafo, int inicial){
    bool* visitado = malloc(sizeof(bool) * grafo->numVertices);
    for(int i = 0; i < grafo->numVertices; i++)
        visitado[i] = false;

    Lista caminho;
    inicializa_lista(&caminho);

    visitado[inicial] = true;
    insere_final(&caminho, inicial);

    busca_caminhos(grafo, &caminho, visitado);

    libera_lista(&caminho);
    free(visitado);
    printf("\n");
}

void busca_caminhos(Grafo* grafo, Lista* caminho, bool* visitado){
    // Se o caminho já tem todos os vértices, mostramos
    if(caminho->tamanho == grafo->numVertices){
        NoLista* no = caminho->prim;
        while(no){
            printf("%d ", no->dado);
            no = no->prox;
        }
        printf("\n");
        return;
    }

    // Último vértice no caminho
    int ultimo = caminho->ult->dado;

    for(int j = 0; j < grafo->numVertices; j++){
        if(grafo->matrizAdj[ultimo][j] && !visitado[j]){
            visitado[j] = true;
            insere_final(caminho, j);

            busca_caminhos(grafo, caminho, visitado);

            // backtrack
            visitado[j] = false;
            // remover último elemento
            remove_final(caminho);
        }
    }
}

bool possui_ciclo(Grafo* grafo, int inicial){
    Cor* cores = malloc(sizeof(Cor) * grafo->numVertices);
    inicializa_cores(cores, grafo->numVertices);

    Lista pilha;
    inicializa_lista(&pilha);

    // Empilha o vértice inicial, pai = -1
    empilha(&pilha, inicial);
    Lista pais; // lista paralela para guardar os pais
    inicializa_lista(&pais);
    empilha(&pais, -1);

    while(pilha.prim){
        int atual = pilha.prim->dado;
        desempilha(&pilha);

        int pai = pais.prim->dado;
        desempilha(&pais);

        if(cores[atual] == Branco){
            cores[atual] = Cinza;

            // percorrer vizinhos
            for(int j = grafo->numVertices - 1; j >= 0; j--){
                if(grafo->matrizAdj[atual][j]){
                    if(cores[j] == Branco){
                        empilha(&pilha, j);
                        empilha(&pais, atual);
                    }
                    else if(j != pai){
                        // achamos um vizinho já visitado que não é o pai
                        free(cores);
                        libera_lista(&pilha);
                        libera_lista(&pais);
                        return true;
                    }
                }
            }
        }
    }

    free(cores);
    libera_lista(&pilha);
    libera_lista(&pais);
    return false;
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

void libera_grafo(Grafo* grafo){
  for (int i = 0; i < grafo->numVertices; i++){
    free(grafo->matrizAdj[i]);
  }
  free(grafo->matrizAdj);

  grafo->matrizAdj = NULL;
  grafo->numArestas = 0;
  grafo->numVertices = 0;
}