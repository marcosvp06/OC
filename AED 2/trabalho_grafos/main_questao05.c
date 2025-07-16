#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "grafo.h"
#include "lista.h"

/**
 * @brief Limpa o terminal de acordo com o sistema operacional.
 */
void limpa_tela() {
    #ifdef _WIN32 // Verifica se o sistema é Windows
        system("cls"); // Comando para Windows
    #else // Para Linux, macOS e outros sistemas tipo Unix
        system("clear"); // Comando para Linux/Unix
    #endif
}

int main() {
    srand(time(NULL)); // Inicializa semente aleatória

    // Conjuntos de tamanhos de grafos e graus de conexidade
    int tamanhos_vertices[] = {10, 20, 50, 100};
    float graus_conexidade[] = {0.25f, 0.40f, 0.65f, 0.85f, 1.0f};

    int n_vertices = sizeof(tamanhos_vertices) / sizeof(tamanhos_vertices[0]);
    int n_graus = sizeof(graus_conexidade) / sizeof(graus_conexidade[0]);

    for (int i = 0; i < n_vertices; i++) {
        int numVertices = tamanhos_vertices[i];

        printf("\n=== Testando com %d vertices ===\n", numVertices);

        for (int j = 0; j < n_graus; j++) {
            float grau = graus_conexidade[j];
            printf("\nGrau de conexidade: %.0f%%\n", grau * 100);

            Grafo g;
            inicializa_grafo_matriz(&g, numVertices);

            // 50% de chance de gerar uma árvore (sem ciclos) ou grafo com possibilidade de ciclo
            if (rand() % 2 == 0) {
                printf("Gerando grafo SEM ciclo (arvore aleatoria)...\n");
                gera_arvore_aleatoria(&g);
            } else {
                printf("Gerando grafo potencialmente COM ciclos...\n");
                gera_arestas_aleatorias(&g, grau);
            }

            // Verifica presença de ciclo a partir do vértice 0
            if (possui_ciclo(&g, 0)) {
                printf("Resultado: O grafo possui ciclo.\n");
            } else {
                printf("Resultado: O grafo NAO possui ciclo.\n");
            }

            libera_grafo(&g);
        }

        printf("\nPressione ENTER para continuar...");
        getchar();
        limpa_tela();
    }

    printf("\n=== Fim da questao 5 ===\n");

    return 0;
}