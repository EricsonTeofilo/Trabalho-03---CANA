import numpy as np
import noise
import time
from scipy.signal import convolve2d

class GeradorTerreno:
    def __init__(self, largura, altura, escala, semente, octavas=6, persistencia=0.5, lacunaridade=2.0):
        self.largura = largura
        self.altura = altura
        self.escala = escala
        self.octavas = octavas
        self.persistencia = persistencia
        self.lacunaridade = lacunaridade
        self.semente = semente if semente is not None else np.random.randint(0, 100)

    def gerar_pontos(self):
        x = np.arange(self.largura) / self.escala
        y = np.arange(self.altura) / self.escala
        x, y = np.meshgrid(x, y)

        mapa = np.vectorize(lambda x, y: noise.pnoise2(
            x, y, octaves=self.octavas,
            persistence=self.persistencia,
            lacunarity=self.lacunaridade,
            base=self.semente))(x, y)
        min_val, max_val = np.min(mapa), np.max(mapa)

        if max_val > min_val:
            mapa = (mapa - min_val) / (max_val - min_val) * 255

        # suavização do terreno
#

        return mapa


class GeradorTerrenoSelecaoLinear:
    def __init__(self, tamanho, profundidade_max, escala_perlin, semente, octavas=6, persistencia=0.5, lacunaridade=2.0):
        self.tamanho = tamanho
        self.profundidade_max = profundidade_max
        self.escala_perlin = escala_perlin
        self.octavas = octavas
        self.persistencia = persistencia
        self.lacunaridade = lacunaridade
        self.rng = np.random.default_rng(semente)
        self.semente = semente
        self.tempos_por_nivel = {}

    def _mediana_das_medianas_otimizada(self, regiao, indice_alvo):
        arr = regiao.ravel()
        return mediana_das_medianas(arr, indice_alvo)

    def gerar_pontos(self):
        gerador_base = GeradorTerreno(
            largura=self.tamanho,
            altura=self.tamanho,
            escala=self.escala_perlin,
            octavas=self.octavas,
            persistencia=self.persistencia,
            lacunaridade=self.lacunaridade,
            semente=self.semente
        )
        mapa = gerador_base.gerar_pontos()

        self.tempos_por_nivel = {}
        self.refinar_divisao_conquista(mapa, 0, 0, self.tamanho, self.tamanho, 1)
        self.tempos_por_nivel = sorted(self.tempos_por_nivel.items())
        return mapa

    def refinar_divisao_conquista(self, mapa, x0, y0, largura, altura, nivel):
        if nivel > self.profundidade_max or largura < 4 or altura < 4:
            return

        inicio = time.perf_counter()
        regiao = mapa[y0:y0 + altura, x0:x0 + largura]

        if regiao.size > 0:
            fracao_para_selecionar = 1 / 5
            percentil_index = int(regiao.size * (1.0 - fracao_para_selecionar))
            pivo = self._mediana_das_medianas_otimizada(regiao, percentil_index)
            rugosidade = 20 / nivel
            mascara_refinamento = regiao >= pivo
            deslocamentos = self.rng.uniform(-rugosidade, rugosidade, size=regiao.shape)
            regiao[mascara_refinamento] += deslocamentos[mascara_refinamento]

        fim = time.perf_counter()
        duracao = fim - inicio
        self.tempos_por_nivel[nivel] = self.tempos_por_nivel.get(nivel, 0) + duracao

        metade_largura = largura // 2
        metade_altura = altura // 2

        self.refinar_divisao_conquista(mapa, x0, y0, metade_largura, metade_altura, nivel + 1)
        self.refinar_divisao_conquista(mapa, x0 + metade_largura, y0, largura - metade_largura, metade_altura, nivel + 1)
        self.refinar_divisao_conquista(mapa, x0, y0 + metade_altura, metade_largura, altura - metade_altura, nivel + 1)
        self.refinar_divisao_conquista(mapa, x0 + metade_largura, y0 + metade_altura, largura - metade_largura, altura - metade_altura, nivel + 1)


def mediana_das_medianas(arr, k):
    n = len(arr)
    if n <= 5:
        return np.partition(arr, k)[k]
    
    medians = []
    for i in range(0, n, 5):
        grupo = arr[i:i + 5]
        mediana_grupo = np.partition(grupo, len(grupo) // 2)[len(grupo) // 2]
        medians.append(mediana_grupo)

    medians = np.array(medians)
    mediana_pivo = mediana_das_medianas(medians, len(medians) // 2)

    menores = arr[arr < mediana_pivo]
    iguais = arr[arr == mediana_pivo]
    maiores = arr[arr > mediana_pivo]

    if k < len(menores):
        return mediana_das_medianas(menores, k)
    elif k < len(menores) + len(iguais):
        return mediana_pivo
    else:
        return mediana_das_medianas(maiores, k - len(menores) - len(iguais))
