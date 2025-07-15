import pygame
from pygame.locals import *
from sys import exit
from Sprites import Sprite
from player import Jogador
from gerenciarProjetil import GerenciadorProjetil
from closetPair import GerenciadorDistancia
from forcaBruta import GerenciadorDistancia2

pygame.init()

# Dimensões da tela
x = 1280
y = 720
sprites = 100

# Escolher o método de 
def escolher_metodo():
    while True:
        print("Escolha o método que deseja utilizar:")
        print("1 - Força Bruta")
        print("2 - Close Pair")
        
        escolha = input("Digite 1 ou 2: ").strip()
        
        if escolha in ('1', '2'):
            return int(escolha)
        else:
            print("Entrada inválida. Por favor, digite 1 ou 2.\n")

metodo = escolher_metodo()

tela = pygame.display.set_mode((x, y))

font_inicio = pygame.font.SysFont("Arial", 50)
for i in range(5, 0, -1): 
    tela.fill((0, 0, 0))
    texto_inicio = font_inicio.render(f"{i}...", True, (0, 255, 0))
    tela.blit(texto_inicio, (x // 2 - texto_inicio.get_width() // 2, y // 2 - texto_inicio.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1000)

# Inicializa os objetos principais
player = Jogador(x, y)
gerenciador_projetil = GerenciadorProjetil()
gerenciador_distancia = GerenciadorDistancia()
gerenciador_distancia2 = GerenciadorDistancia2()

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Função para criar objetos
def criarobjetos():
    objetos = []
    for _ in range(sprites):
        obj = Sprite(x, y)
        objetos.append(obj)
    return objetos

objetos = criarobjetos()

# Controle do disparo
atirando = False
ultimo_tiro = 0
intervalo_tiro = 0.2

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                atirando = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                atirando = False

    teclas = pygame.key.get_pressed()
    player.movimentacao(teclas)

    tela.fill((0, 0, 0))

    player.desenha(tela)

    #if player is not None:
        #if player.verifica_colisao(objetos):
            #player = None

    for obj in objetos:
        obj.movimentacao()

    # Escolha do método para encontrar o par mais próximo
    if metodo == 1:  # Força Bruta
        par_mais_proximo, num_verificacoes = gerenciador_distancia2.encontrar_par_mais_proximo(objetos)
    else:  # Close Pair
        par_mais_proximo, dist_min, num_verificacoes = gerenciador_distancia.encontrar_par_mais_proximo(objetos)

    # Destacar os objetos no par mais próximo
    for obj in objetos:
        if obj in par_mais_proximo:
            obj.desenha(tela, cor=(255, 0, 0))
        else:
            obj.desenha(tela)

    # Disparar projéteis continuamente
    tempo_atual = pygame.time.get_ticks() / 1000  # Tempo atual em segundos
    if atirando and tempo_atual - ultimo_tiro >= intervalo_tiro:
        player.atirar(gerenciador_projetil)
        ultimo_tiro = tempo_atual

    gerenciador_projetil.atualiza(tela, objetos, x, y)

    # FPS, contador de objetos e número de verificações
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 255, 100))
    contagem_text = font.render(f"Objetos: {len(objetos)}", True, (0, 255, 100))
    verificacoes_text = font.render(f"Verificações: {num_verificacoes}", True, (0, 255, 100))

    tela.blit(fps_text, (10, 10))
    tela.blit(contagem_text, (10, 35))
    tela.blit(verificacoes_text, (10, 60))

    pygame.display.update()

    clock.tick()