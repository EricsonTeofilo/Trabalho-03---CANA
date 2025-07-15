import pygame
import math
import time
from projetil import Projetil

class Jogador:
    def __init__(self, largura_tela, altura_tela):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        self.largura = 20
        self.altura = 20

        # Posição inicial no centro da tela
        self.x = largura_tela // 2
        self.y = altura_tela // 2

        self.velocidade = 1

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def verifica_colisao(self, objetos):
        jogador_rect = self.get_rect()
        for obj in objetos[:]:
            if jogador_rect.colliderect(obj.get_rect()):
                return True 
        return False

    def movimentacao(self, teclas):
        if teclas[pygame.K_w]:
            self.y -= self.velocidade
        if teclas[pygame.K_s]:
            self.y += self.velocidade
        if teclas[pygame.K_a]:
            self.x -= self.velocidade
        if teclas[pygame.K_d]:
            self.x += self.velocidade

        self.x = max(0, min(self.x, self.largura_tela - self.largura))
        self.y = max(0, min(self.y, self.altura_tela - self.altura))

    def atirar(self, gerenciador_projetil):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        angulo = math.atan2(dy, dx)
        projetil = Projetil(self.x, self.y, angulo)
        gerenciador_projetil.adiciona(projetil)

    def desenha(self, tela):
        # Calcula o angulo para o cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        angulo = math.atan2(dy, dx)

        tamanho = 20
        pontos = [
            (self.x + math.cos(angulo) * tamanho, self.y + math.sin(angulo) * tamanho),
            (self.x + math.cos(angulo + 2.5) * tamanho, self.y + math.sin(angulo + 2.5) * tamanho),
            (self.x + math.cos(angulo - 2.5) * tamanho, self.y + math.sin(angulo - 2.5) * tamanho),
        ]

        pygame.draw.polygon(tela, (100, 100, 100), pontos)
