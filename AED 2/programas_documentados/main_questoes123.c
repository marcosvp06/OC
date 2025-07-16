#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "grafo.h"
#include "lista.h"

/**
 * @brief Limpa o terminal, dependendo do sistema operacional.
 */
void limpa_tela() {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

/**
 * @brief Calcula a média de um vetor de tempos.
 * @param tempos Vetor contendo os tempos.
 * @param tamanho Tamanho do vetor.
 * @return Média dos tempos.
 */
double calcula_media_tempo(double tempos[], int tamanho) {
    if (tamanho == 0) return 0.0;
    double soma = 0.0;
    for (int i = 0; i < tamanho; i++)
        soma += tempos[i];
    return soma / tamanho;
}

/**
 * @brief Calcula o tempo decorrido entre dois instantes.
 * @param inicio Instante inicial (clock_t).
 * @param fim Instante final (clock_t).
 * @return Tempo em segundos (double).
 */
double calcula_tempo(clock_t inicio, clock_t fim) {
    return (double)(fim - inicio) / CLOCKS_PER_SEC;
}

int main() {
    srand(time(NULL));

    // Conjuntos de teste: tamanhos e graus de conexidade
    int tamanhos_vertices[] = {10, 50, 100, 300, 500, 750, 1000, 1500, 2500};
    float graus_conexidade[] = {0.25f, 0.40f, 0.65f, 0.85f, 1.0f};
    int n_vertices = sizeof(tamanhos_vertices) / sizeof(tamanhos_vertices[0]);
    int n_graus = sizeof(graus_conexidade) / sizeof(graus_conexidade[0]);

    double medias_bfs[n_vertices];
    double medias_dfs[n_vertices];

    // Abertura dos arquivos CSV
    FILE *csv_bfs = fopen("tempos_bfs.csv", "w");
    FILE *csv_dfs = fopen("tempos_dfs.csv", "w");
    if (!csv_bfs || !csv_dfs) {
        perror("Erro ao abrir arquivo CSV");
        return 1;
    }

    // Cabeçalhos dos arquivos CSV
    fprintf(csv_bfs, "Vertices");
    fprintf(csv_dfs, "Vertices");
    for (int j = 0; j < n_graus; j++) {
        fprintf(csv_bfs, ",%.0f%%", graus_conexidade[j]*100);
        fprintf(csv_dfs, ",%.0f%%", graus_conexidade[j]*100);
    }
    fprintf(csv_bfs, ",Media\n");
    fprintf(csv_dfs, ",Media\n");

    printf("==== INICIO DAS MEDICOES ====\n");

    // Loop principal de teste
    for (int i = 0; i < n_vertices; i++) {
        int numVertices = tamanhos_vertices[i];
        double tempos_bfs[n_graus];
        double tempos_dfs[n_graus];

        printf("\n===== Testando com %d vertices =====\n", numVertices);

        for (int j = 0; j < n_graus; j++) {
            float grau = graus_conexidade[j];
            printf("\n-> Grafo com %.0f%% de conexidade:\n\n", grau * 100);

            Grafo g;
            inicializa_grafo_matriz(&g, numVertices);
            gera_arestas_aleatorias(&g, grau);

            // --- Execução e medição de tempo da BFS ---
            clock_t inicio_bfs = clock();
            ArvoreBFS arvore = bfs(&g, 0);
            clock_t fim_bfs = clock();
            double tempo_bfs = calcula_tempo(inicio_bfs, fim_bfs);
            tempos_bfs[j] = tempo_bfs;

            if (numVertices <= 300) {
                mostra_arvore_bfs(arvore);
            }
            libera_arvore_bfs(&arvore, g.numVertices);

            // --- Execução e medição de tempo da DFS ---
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

            printf("Tempos (s): BFS = %.9f | DFS = %.9f\n", tempo_bfs, tempo_dfs);
            printf("-----------------------------------------------------\n");
        }

        // Cálculo das médias para cada tamanho de grafo
        double media_bfs = calcula_media_tempo(tempos_bfs, n_graus);
        double media_dfs = calcula_media_tempo(tempos_dfs, n_graus);
        medias_bfs[i] = media_bfs;
        medias_dfs[i] = media_dfs;

        printf("\n>> Medias para %d vertices:\n", numVertices);
        printf("BFS: %.9f s | DFS: %.9f s\n", media_bfs, media_dfs);

        // Escrita dos resultados no CSV
        fprintf(csv_bfs, "%d", numVertices);
        for (int j = 0; j < n_graus; j++)
            fprintf(csv_bfs, ",%.9f", tempos_bfs[j]);
        fprintf(csv_bfs, ",%.9f\n", media_bfs);

        fprintf(csv_dfs, "%d", numVertices);
        for (int j = 0; j < n_graus; j++)
            fprintf(csv_dfs, ",%.9f", tempos_dfs[j]);
        fprintf(csv_dfs, ",%.9f\n", media_dfs);

        printf("\nPressione ENTER para continuar...\n");
        getchar();
        limpa_tela();
    }

    fclose(csv_bfs);
    fclose(csv_dfs);

    // Exibe resumo final das médias
    printf("\n         ====== RESUMO FINAL DAS MEDIAS ======\n\n");
    printf("%-15s %-20s %-20s\n", "Vertices", "Media BFS (s)", "Media DFS (s)");
    printf("--------------------------------------------------------------\n");
    for (int i = 0; i < n_vertices; i++) {
        printf("%-15d %-20.9f %-20.9f\n",
            tamanhos_vertices[i], medias_bfs[i], medias_dfs[i]);
    }

    return 0;
}