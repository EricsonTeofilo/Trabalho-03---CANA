import numpy as np
import matplotlib.pyplot as plt
import time

from geradorSeletivoMedianas import GeradorTerrenoSelecaoLinear
from geradorExaustivo import GeradorTerreno


def visualizar_wireframe_3d(mapa_de_altura, titulo):
    """Renderiza o resultado final em 3D (wireframe simples)."""
    altura, largura = mapa_de_altura.shape
    X, Y = np.meshgrid(np.arange(largura), np.arange(altura))

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_wireframe(X, Y, mapa_de_altura, rstride=2, cstride=2, linewidth=0.5)

    ax.set_title(titulo)
    ax.set_xlabel("Eixo X")
    ax.set_ylabel("Eixo Y")
    ax.set_zlabel("Elevação")
    plt.show()


if __name__ == "__main__":
    # PARÂMETROS
    TAMANHO_TERRENO = 100 
    ESCALA_RUIDO = 60.0
    SEMENTE_FIXA = 2077
    PROFUNDIDADE_MAX = 3

    print("Selecione o método de geração do terreno:")
    print("1 - Gerador Terreno (Exaustivo com Ruído Perlin)")
    print("2 - Gerador Seletivo (Refinamento Recursivo com Mediana)")
    metodo = int(input("Escolha (1 ou 2): ").strip())

    if metodo == 1:
        print("Método selecionado: Gerador exaustivo")
        gerador = GeradorTerreno(
            largura=TAMANHO_TERRENO,
            altura=TAMANHO_TERRENO,
            escala=ESCALA_RUIDO,
            semente=SEMENTE_FIXA
        )

    elif metodo == 2:
        print("Método selecionado: Gerador seletivo (Mediana das Medianas)")
        gerador = GeradorTerrenoSelecaoLinear(
            tamanho=TAMANHO_TERRENO,
            profundidade_max=PROFUNDIDADE_MAX,
            escala_perlin=ESCALA_RUIDO,
            semente=SEMENTE_FIXA,
            octavas=6,
            persistencia=0.5,
            lacunaridade=2.0
        )

    else:
        print("Opção inválida. Encerrando o programa.")
        exit(1)

    print("Iniciando a geração do terreno...")
    tempo_inicio = time.time()
    mapa_gerado = gerador.gerar_pontos()
    tempo_fim = time.time()

    duracao = tempo_fim - tempo_inicio
    print(f"Terreno gerado em {duracao:.4f} segundos.")

    if metodo == 2:
        print("Tempo gasto por nível (seleção linear):")
        for nivel, tempo in gerador.tempos_por_nivel:
            print(f"  Nível {nivel}: {tempo:.4f} segundos")

    titulo_grafico = f"Wireframe 3D ({TAMANHO_TERRENO}x{TAMANHO_TERRENO} pontos) - Método {'Exaustivo' if metodo == 1 else 'Seletivo'}"
    visualizar_wireframe_3d(mapa_gerado, titulo_grafico)
