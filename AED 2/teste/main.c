#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "grafo.h"
#include "lista.h"

double calcula_media_tempo(double tempos[], int tamanho) {
    if (tamanho == 0) return 0.0;
    double soma = 0.0;
    for (int i = 0; i < tamanho; i++) soma += tempos[i];
    return soma / tamanho;
}

double calcula_tempo(clock_t inicio, clock_t fim) {
    return (double)(fim - inicio) / CLOCKS_PER_SEC;
}

int main() {
    srand(time(NULL));

    int tamanhos_vertices[] = {10, 50, 100, 200, 300, 400, 500, 1000, 2000, 5000};
    float graus_conexidade[] = {0.25f, 0.40f, 0.65f, 0.85f, 1.0f};

    int n_vertices = sizeof(tamanhos_vertices) / sizeof(tamanhos_vertices[0]);
    int n_graus = sizeof(graus_conexidade) / sizeof(graus_conexidade[0]);

    double medias_bfs[n_vertices];
    double medias_dfs[n_vertices];

    for (int i = 0; i < n_vertices; i++) {
        int numVertices = tamanhos_vertices[i];

        double tempos_bfs[n_graus];
        double tempos_dfs[n_graus];

        printf("\n===== Testando com %d vertices =====\n", numVertices);

        for (int j = 0; j < n_graus; j++) {
            float grau = graus_conexidade[j];

            printf("\n-> Criando grafo com %.0f%% de conexidade:\n\n", grau * 100);

            Grafo g;
            inicializa_grafo_matriz(&g, numVertices);
            gera_arestas_aleatorias(&g, grau);

            // BFS
            clock_t inicio_bfs = clock();
            ArvoreBFS arvore = bfs(&g, 0);
            clock_t fim_bfs = clock();
            double tempo_bfs = calcula_tempo(inicio_bfs, fim_bfs);
            tempos_bfs[j] = tempo_bfs;

            if (numVertices <= 300) {
                mostra_arvore_bfs(arvore);
            }

            libera_arvore_bfs(&arvore, g.numVertices);

            // DFS
            clock_t inicio_dfs = clock();
            Lista seq = dfs(&g, 0);
            clock_t fim_dfs = clock();
            double tempo_dfs = calcula_tempo(inicio_dfs, fim_dfs);
            tempos_dfs[j] = tempo_dfs;

            if (numVertices <= 300) {
                mostra_sequencia_dfs(seq);
            }

            libera_lista(&seq);
            libera_grafo(&g);

            printf("Tempo BFS: %.9f s | Tempo DFS: %.9f s\n\n", tempo_bfs, tempo_dfs);
            printf("-----------------------------------------------------\n");
        }

        double media_bfs = calcula_media_tempo(tempos_bfs, n_graus);
        double media_dfs = calcula_media_tempo(tempos_dfs, n_graus);

        medias_bfs[i] = media_bfs;
        medias_dfs[i] = media_dfs;

        printf("\n>> Media de tempos para %d vertices:\n", numVertices);
        printf("BFS: %.9f s | DFS: %.9f s\n", media_bfs, media_dfs);

        // Pausa
        printf("\nPressione ENTER para continuar...");
        getchar();

        // Limpa a tela
        system("cls");
    }

    printf("\n=== RESUMO FINAL DAS MEDIAS ===\n");
    for (int i = 0; i < n_vertices; i++) {
        printf("\nNumero de vertices: %d\n", tamanhos_vertices[i]);
        printf("Media BFS: %.9f s\n", medias_bfs[i]);
        printf("Media DFS: %.9f s\n", medias_dfs[i]);
    }

    return 0;
}