import pygame


class GerenciadorProjetil:
    def __init__(self):
        self.projeteis = []

    def adiciona(self, projetil):
        self.projeteis.append(projetil)

    def atualiza(self, tela, objetos, largura_tela, altura_tela):
        for projetil in self.projeteis[:]:
            projetil.movimenta()
            projetil.desenha(tela)

            if projetil.x < 0 or projetil.x > largura_tela or projetil.y < 0 or projetil.y > altura_tela:
                self.projeteis.remove(projetil)
                continue

            # Checa colisão com objetos
            projetil_rect = pygame.Rect(projetil.x - 2, projetil.y - 2, 4, 4)
            for obj in objetos[:]:
                objeto_rect = pygame.Rect(obj.a - 2, obj.b - 2, 10, 10) 
                if projetil_rect.colliderect(objeto_rect):
                    objetos.remove(obj)
                    self.projeteis.remove(projetil)
                    break
