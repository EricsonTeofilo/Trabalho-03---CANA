import math
import pygame
import random

class GerenciadorDistancia:
    def __init__(self):
        pass

    def encontrar_par_mais_proximo(self, objetos):
        """Encontra o par mais próximo em um conjunto de objetos."""
        if len(objetos) < 2:
            return [], 0

        # Ordena objetos por coordenada x
        objetos.sort(key=lambda obj: obj.a)
        return self.closest_pair_recursivo(objetos)

    def closest_pair_recursivo(self, objetos):
        n = len(objetos)
        
        if n < 2:
            return [], float('inf'), 0

        if n == 2:
            dist = self.calcular_distancia(objetos[0], objetos[1])
            return [objetos[0], objetos[1]], dist, 1

        meio = n // 2
        linha_divisoria = objetos[meio].a

        lado_esquerdo = objetos[:meio]
        lado_direito = objetos[meio:]

        par_esquerdo, d_esquerda, cont_esq = self.closest_pair_recursivo(lado_esquerdo)
        par_direito, d_direita, cont_dir = self.closest_pair_recursivo(lado_direito)

        if d_esquerda < d_direita:
            d_min = d_esquerda
            par_mais_proximo = par_esquerdo
        else:
            d_min = d_direita
            par_mais_proximo = par_direito

        faixa = [obj for obj in objetos if abs(obj.a - linha_divisoria) < d_min]
        par_faixa, d_faixa, cont_faixa = self._faixa_menor_distancia(faixa, d_min)

        total_cont = cont_esq + cont_dir + cont_faixa

        if d_faixa < d_min:
            return par_faixa, d_faixa, total_cont
        return par_mais_proximo, d_min, total_cont


    def _faixa_menor_distancia(self, faixa, d_min):
        """Encontra o menor par na faixa próxima à linha divisória."""
        # Ordena por coordenada y
        faixa.sort(key=lambda obj: obj.b)  
        min_dist = d_min
        par_mais_proximo = []
        cont_verificacoes = 0

        for i in range(len(faixa)):
            for j in range(i + 1, len(faixa)):
                cont_verificacoes += 1
                if (faixa[j].b - faixa[i].b) >= min_dist:
                    break
                dist = self.calcular_distancia(faixa[i], faixa[j])
                if dist < min_dist:
                    min_dist = dist
                    par_mais_proximo = [faixa[i], faixa[j]]

        return par_mais_proximo, min_dist, cont_verificacoes

    def calcular_distancia(self, obj1, obj2):
        """Calcula a distância entre dois objetos."""
        dx = obj1.a - obj2.a
        dy = obj1.b - obj2.b
        return math.sqrt(dx * dx + dy * dy)

class Sprite:
    def __init__(self, largura_tela, altura_tela):
        self.a = random.randint(0, largura_tela)
        self.b = random.randint(0, altura_tela)
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

    def desenha(self, tela, cor=(255, 255, 255)):
        pygame.draw.circle(tela, cor, (self.a, self.b), 5)