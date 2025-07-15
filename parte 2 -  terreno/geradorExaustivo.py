import numpy as np
import noise

class GeradorTerreno:
    def __init__(self, largura, altura, escala, octavas=6, persistencia=0.5, lacunaridade=2.0, semente=None):
        self.largura = largura
        self.altura = altura
        self.escala = escala
        self.octavas = octavas
        self.persistencia = persistencia
        self.lacunaridade = lacunaridade
        self.semente = semente if semente is not None else np.random.randint(0, 100)
        
    def gerar_pontos(self):
        # Geração inicial do mapa com ruído de Perlin
        mapa = np.zeros((self.altura, self.largura))
        for y in range(self.altura):
            for x in range(self.largura):
                valor_ruido = noise.pnoise2(
                    x / self.escala, y / self.escala,
                    octaves=self.octavas,
                    persistence=self.persistencia,
                    lacunarity=self.lacunaridade,
                    base=self.semente
                )
                # Normalizando os valores de [-1, 1] para [0, 255]
                mapa[y][x] = (valor_ruido + 1) * 127.5  # Intervalo [0, 255]

        # Processamento quadrático adicional (média local geral)
        mapa_refinado = np.zeros_like(mapa)
        for y1 in range(self.altura):
            for x1 in range(self.largura):
                soma = 0.0
                contagem = 0
                for y2 in range(self.altura):
                    for x2 in range(self.largura):
                        peso = 1 / (1 + abs(y1 - y2) + abs(x1 - x2))  # Peso decrescente com a distância
                        soma += peso * mapa[y2][x2]
                        contagem += peso
                mapa_refinado[y1][x1] = soma / contagem  # Média ponderada
                
        return mapa_refinado
