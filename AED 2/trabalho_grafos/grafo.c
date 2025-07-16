#include "grafo.h"

/**
 * @brief Inicializa um grafo vazio com matriz de adjacência.
 * Todos os valores são definidos como `false` (sem arestas).
 */
void inicializa_grafo_matriz(Grafo* grafo, int numVertices) {
    grafo->matrizAdj = (bool**) malloc(sizeof(bool*) * numVertices);
    for (int i = 0; i < numVertices; i++) {
        grafo->matrizAdj[i] = (bool*) malloc(sizeof(bool) * numVertices);
        for (int j = 0; j < numVertices; j++) {
            grafo->matrizAdj[i][j] = false;
        }
    }
    grafo->numVertices = numVertices;
    grafo->numArestas = 0;
}

/**
 * @brief Define todas as cores como Branco (não visitado).
 */
void inicializa_cores(Cor* cores, int tamanho) {
    for (int i = 0; i < tamanho; i++) {
        cores[i] = Branco;
    }
}

/**
 * @brief Inicializa um vetor de listas vazias para armazenar caminhos.
 */
void inicializa_caminhos(Lista* caminhos, int tamanho) {
    for (int i = 0; i < tamanho; i++) {
        inicializa_lista(&caminhos[i]);
    }
}

/**
 * @brief Adiciona uma aresta não-direcionada entre dois vértices.
 */
void adiciona_aresta_grafo(Grafo* grafo, int origem, int destino) {
    grafo->matrizAdj[origem][destino] = true;
    grafo->matrizAdj[destino][origem] = true;
    grafo->numArestas++;
}

/**
 * @brief Gera aleatoriamente arestas para o grafo com um grau de conexidade.
 * Garante que o grafo seja conexo.
 */
void gera_arestas_aleatorias(Grafo* grafo, float grau_conexidade) {
    int numVertices = grafo->numVertices;
    int arestas = (int)(grau_conexidade * numVertices * (numVertices - 1)) / 2;

    if (arestas < numVertices - 1) {
        printf("Impossivel gerar um grafo conexo, faltam arestas.\n");
    }

    int* vertices = (int*) malloc(sizeof(int) * numVertices);
    for (int i = 0; i < numVertices; i++) {
        vertices[i] = i;
    }

    // Embaralha os vértices (Fisher-Yates)
    int temp;
    for (int i = numVertices - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        temp = vertices[i];
        vertices[i] = vertices[j];
        vertices[j] = temp;
    }

    // Cria árvore base para garantir conexidade
    for (int i = 1; i < numVertices; i++) {
        int k = rand() % i;
        adiciona_aresta_grafo(grafo, vertices[i], vertices[k]);
        arestas--;
    }

    // Adiciona arestas aleatórias restantes
    int origem, destino;
    while (arestas > 0) {
        origem = rand() % numVertices;
        destino = rand() % numVertices;
        if (origem != destino && grafo->matrizAdj[origem][destino] == false) {
            adiciona_aresta_grafo(grafo, origem, destino);
            arestas--;
        }
    }

    free(vertices);
}

/**
 * @brief Gera uma árvore aleatória (sem ciclos), conectando todos os vértices.
 */
void gera_arvore_aleatoria(Grafo* grafo) {
    int numVertices = grafo->numVertices;
    int* vertices = (int*) malloc(sizeof(int) * numVertices);

    for (int i = 0; i < numVertices; i++) {
        vertices[i] = i;
    }

    // Embaralha os vértices
    for (int i = numVertices - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = vertices[i];
        vertices[i] = vertices[j];
        vertices[j] = temp;
    }

    // Conecta em árvore
    for (int i = 1; i < numVertices; i++) {
        int k = rand() % i;
        adiciona_aresta_grafo(grafo, vertices[i], vertices[k]);
    }

    free(vertices);
}

/**
 * @brief Executa BFS a partir de um vértice inicial e constrói árvore de níveis.
 * @return Estrutura contendo as listas de vértices por nível.
 */
ArvoreBFS bfs(Grafo* grafo, int inicial) {
    Cor* cores = malloc(sizeof(Cor) * grafo->numVertices);
    inicializa_cores(cores, grafo->numVertices);

    int* distancias = malloc(sizeof(int) * grafo->numVertices);
    for (int i = 0; i < grafo->numVertices; i++)
        distancias[i] = -1;

    ArvoreBFS arvore;
    arvore.niveis = malloc(sizeof(Lista) * grafo->numVertices);
    arvore.max_nivel = 0;

    for (int i = 0; i < grafo->numVertices; i++)
        inicializa_lista(&arvore.niveis[i]);

    cores[inicial] = Cinza;
    distancias[inicial] = 0;
    insere_final(&arvore.niveis[0], inicial);

    Lista fila;
    inicializa_lista(&fila);
    enfila(&fila, inicial);

    while (fila.prim) {
        int atual = fila.prim->dado;

        for (int j = 0; j < grafo->numVertices; j++) {
            if (grafo->matrizAdj[atual][j] && cores[j] == Branco) {
                cores[j] = Cinza;
                distancias[j] = distancias[atual] + 1;
                insere_final(&arvore.niveis[distancias[j]], j);
                if (distancias[j] > arvore.max_nivel)
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

/**
 * @brief Imprime a árvore gerada pela BFS em níveis.
 */
void mostra_arvore_bfs(ArvoreBFS arvore) {
    printf("Arvore resultante da BFS:\n");
    for (int nivel = 0; nivel <= arvore.max_nivel; nivel++) {
        printf("Nivel %d: ", nivel);
        NoLista* no = arvore.niveis[nivel].prim;
        while (no) {
            printf("%d ", no->dado);
            no = no->prox;
        }
        printf("\n");
    }
    printf("\n");
}

/**
 * @brief Libera a memória associada à árvore BFS.
 */
void libera_arvore_bfs(ArvoreBFS* arvore, int numVertices) {
    for (int i = 0; i < numVertices; i++) {
        libera_lista(&arvore->niveis[i]);
    }
    free(arvore->niveis);
    arvore->niveis = NULL;
    arvore->max_nivel = 0;
}

/**
 * @brief Executa DFS iterativa a partir de um vértice inicial.
 * @return Lista com a sequência de visita dos vértices.
 */
Lista dfs_iterativa(Grafo* grafo, int inicial) {
    Cor* cores = malloc(sizeof(Cor) * grafo->numVertices);
    inicializa_cores(cores, grafo->numVertices);

    Lista sequencia;
    inicializa_lista(&sequencia);

    Lista pilha;
    inicializa_lista(&pilha);
    empilha(&pilha, inicial);

    while (pilha.prim) {
        int atual = pilha.prim->dado;
        desempilha(&pilha);

        if (cores[atual] == Branco) {
            cores[atual] = Preto;
            insere_final(&sequencia, atual);

            for (int j = grafo->numVertices - 1; j >= 0; j--) {
                if (grafo->matrizAdj[atual][j] && cores[j] == Branco) {
                    empilha(&pilha, j);
                }
            }
        }
    }

    free(cores);
    libera_lista(&pilha);
    return sequencia;
}

/**
 * @brief Executa DFS recursiva a partir de um vértice inicial.
 */
Lista dfs(Grafo* grafo, int inicial) {
    Cor* cores = malloc(sizeof(Cor) * grafo->numVertices);
    inicializa_cores(cores, grafo->numVertices);

    Lista sequencia;
    inicializa_lista(&sequencia);

    dfs_visita(grafo, inicial, cores, &sequencia);

    free(cores);
    return sequencia;
}

/**
 * @brief Função recursiva auxiliar da DFS.
 */
void dfs_visita(Grafo* grafo, int atual, Cor* cores, Lista* sequencia) {
    cores[atual] = Preto;
    insere_final(sequencia, atual);

    for (int j = 0; j < grafo->numVertices; j++) {
        if (grafo->matrizAdj[atual][j] && cores[j] == Branco) {
            dfs_visita(grafo, j, cores, sequencia);
        }
    }
}

/**
 * @brief Mostra a sequência de vértices visitados pela DFS.
 */
void mostra_sequencia_dfs(Lista sequencia) {
    printf("Sequencia de vertices visitados na DFS:\n");
    NoLista* no = sequencia.prim;
    while (no) {
        printf("%d ", no->dado);
        no = no->prox;
    }
    printf("\n\n");
}

/**
 * @brief Mostra todos os caminhos possíveis a partir de um vértice.
 */
void mostra_todos_caminhos(Grafo* grafo, int inicial) {
    printf("Todos os caminhos a partir do vertice %d:\n", inicial);
    bool* visitado = malloc(sizeof(bool) * grafo->numVertices);
    for (int i = 0; i < grafo->numVertices; i++)
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

/**
 * @brief Função auxiliar recursiva para listar todos os caminhos possíveis.
 */
void busca_caminhos(Grafo* grafo, Lista* caminho, bool* visitado) {
    if (caminho->tamanho == grafo->numVertices) {
        NoLista* no = caminho->prim;
        while (no) {
            printf("%d ", no->dado);
            no = no->prox;
        }
        printf("\n");
        return;
    }

    int ultimo = caminho->ult->dado;

    for (int j = 0; j < grafo->numVertices; j++) {
        if (grafo->matrizAdj[ultimo][j] && !visitado[j]) {
            visitado[j] = true;
            insere_final(caminho, j);
            busca_caminhos(grafo, caminho, visitado);
            visitado[j] = false;
            remove_final(caminho);
        }
    }
}

/**
 * @brief Verifica se o grafo possui ciclos usando DFS com controle de pai.
 * @return true se o grafo possui ciclo, false caso contrário.
 */
bool possui_ciclo(Grafo* grafo, int inicial) {
    Cor* cores = malloc(sizeof(Cor) * grafo->numVertices);
    inicializa_cores(cores, grafo->numVertices);

    Lista pilha, pais;
    inicializa_lista(&pilha);
    inicializa_lista(&pais);

    empilha(&pilha, inicial);
    empilha(&pais, -1);

    while (pilha.prim) {
        int atual = pilha.prim->dado;
        desempilha(&pilha);

        int pai = pais.prim->dado;
        desempilha(&pais);

        if (cores[atual] == Branco) {
            cores[atual] = Cinza;

            for (int j = grafo->numVertices - 1; j >= 0; j--) {
                if (grafo->matrizAdj[atual][j]) {
                    if (cores[j] == Branco) {
                        empilha(&pilha, j);
                        empilha(&pais, atual);
                    } else if (j != pai) {
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

/**
 * @brief Imprime a matriz de adjacência do grafo.
 */
void mostra_grafo_matriz(Grafo grafo) {
    printf("Matriz de adjacencia com %d vertices:\n", grafo.numVertices);
    for (int i = 0; i < grafo.numVertices; i++) {
        for (int j = 0; j < grafo.numVertices; j++) {
            printf("%d ", grafo.matrizAdj[i][j]);
        }
        printf("\n");
    }
    printf("Numero de arestas do grafo: %d\n\n", grafo.numArestas);
}

/**
 * @brief Libera toda a memória alocada pela matriz de adjacência do grafo.
 */
void libera_grafo(Grafo* grafo) {
    for (int i = 0; i < grafo->numVertices; i++) {
        free(grafo->matrizAdj[i]);
    }
    free(grafo->matrizAdj);

    grafo->matrizAdj = NULL;
    grafo->numArestas = 0;
    grafo->numVertices = 0;
}