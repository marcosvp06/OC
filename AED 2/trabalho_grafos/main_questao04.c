#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "grafo.h"
#include "lista.h"

void limpa_tela() {
    #ifdef _WIN32 // Verifica se o sistema é Windows
        system("cls"); // Comando para Windows
    #else // Para Linux, macOS e outros sistemas tipo Unix
        system("clear"); // Comando para Linux/Unix
    #endif
}

int main() {
    srand(time(NULL));

    int tamanhos_vertices[] = {5, 6, 7}; // tamanhos pequenos para evitar explosão
    float graus_conexidade[] = {0.4f, 0.6f, 0.8f, 1.0f};
    int n_vertices = sizeof(tamanhos_vertices) / sizeof(tamanhos_vertices[0]);
    int n_graus = sizeof(graus_conexidade) / sizeof(graus_conexidade[0]);

    for (int i = 0; i < n_vertices; i++) {
        int numVertices = tamanhos_vertices[i];

        for (int j = 0; j < n_graus; j++) {
            float grau = graus_conexidade[j];

            printf("\n===== Testando com %d vertices =====\n", numVertices);

            printf("\n-> Criando grafo com %.0f%% de conexidade:\n\n", grau * 100);

            Grafo g;
            inicializa_grafo_matriz(&g, numVertices);
            gera_arestas_aleatorias(&g, grau);
            
            int v_aleatorio = rand() % numVertices;
            mostra_todos_caminhos(&g, v_aleatorio);

            libera_grafo(&g);

            printf("Pressione ENTER para continuar...");
            getchar();
            limpa_tela();
        }
    }

    printf("\n===== Fim da questao 4 =====\n");

    return 0;
}