import pygame
import random

class Sprite:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        # Tamanho do sprite
        self.raio = 5 

        # Margem de saída
        self.margem_saida = 100 

        self.a = random.randint(-self.margem_saida, self.largura_tela + self.margem_saida)
        self.b = random.randint(-self.margem_saida, self.altura_tela + self.margem_saida)

        # Velocidades
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

        # Controle de velocidade
        self.velocidade = random.randint(5, 10)
        self.contador_frames = 0

    def get_rect(self):
        return pygame.Rect(self.a - self.raio, self.b - self.raio, 2 * self.raio, 2 * self.raio)

    def movimentacao(self):
        self.contador_frames += 1
        if self.contador_frames < self.velocidade:
            return
        self.contador_frames = 0

        # Atualiza posição
        self.a += self.dx
        self.b += self.dy

        # Checa as bordas
        if self.a <= -self.margem_saida:
            self.a = -self.margem_saida
            self.dx *= -1

        elif self.a >= self.largura_tela + self.margem_saida:
            self.a = self.largura_tela + self.margem_saida
            self.dx *= -1

        if self.b <= -self.margem_saida:
            self.b = -self.margem_saida
            self.dy *= -1

        elif self.b >= self.altura_tela + self.margem_saida:
            self.b = self.altura_tela + self.margem_saida
            self.dy *= -1

    def desenha(self, tela, cor=(255, 255, 255)):
        if -self.margem_saida <= self.a <= self.largura_tela + self.margem_saida and \
           -self.margem_saida <= self.b <= self.altura_tela + self.margem_saida:
            pygame.draw.circle(tela, cor, (self.a, self.b), self.raio)