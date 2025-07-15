import pygame
import math

class Projetil:
    def __init__(self, x, y, angulo, velocidade=5):
        self.x = x
        self.y = y
        self.angulo = angulo
        self.velocidade = velocidade

    def movimenta(self):
        self.x += math.cos(self.angulo) * self.velocidade
        self.y += math.sin(self.angulo) * self.velocidade

    def desenha(self, tela):
        comprimento = 15
        x_fim = self.x + math.cos(self.angulo) * comprimento
        y_fim = self.y + math.sin(self.angulo) * comprimento

        pygame.draw.line(tela, (0, 255, 200), (int(self.x), int(self.y)), (int(x_fim), int(y_fim)), 5)
