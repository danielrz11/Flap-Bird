import pygame
pygame.init()  # Inicializa antes de qualquer uso de fonte

from funcoes import (
    tela_menu, 
    tela_game_over, 
    criar_cano, 
    desenhar_pontuacao, 
    AZUL, VERDE, AMARELO
)

# Configurações
LARGURA, ALTURA = 400, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Bird Simples")

def jogo():
    gravidade = 0.5
    pulo = -8
    velocidade_cano = 2
    distancia_entre_canos = 300
    largura_cano = 70
    passaro_x = 50
    passaro_y = ALTURA // 2
    velocidade_y = 0
    canos = [criar_cano()]
    pontuacao = 0
    passou_cano = False

    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        relogio.tick(60)
        TELA.fill(AZUL)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                velocidade_y = pulo

        velocidade_y += gravidade
        passaro_y += velocidade_y
        pygame.draw.circle(TELA, AMARELO, (passaro_x, int(passaro_y)), 20)

        for cano in canos:
            cano['x'] -= velocidade_cano
            pygame.draw.rect(TELA, VERDE, (cano['x'], 0, largura_cano, cano['topo']))
            pygame.draw.rect(TELA, VERDE, (cano['x'], cano['base'], largura_cano, ALTURA))

        if canos[-1]['x'] < LARGURA - distancia_entre_canos:
            canos.append(criar_cano())
        if canos[0]['x'] < -largura_cano:
            canos.pop(0)

        for cano in canos:
            if not passou_cano and cano['x'] + largura_cano < passaro_x:
                pontuacao += 1
                passou_cano = True
        if canos[0]['x'] + largura_cano < passaro_x:
            passou_cano = False

        for cano in canos:
            if passaro_x + 20 > cano['x'] and passaro_x - 20 < cano['x'] + largura_cano:
                if passaro_y - 20 < cano['topo'] or passaro_y + 20 > cano['base']:
                    rodando = False
        if passaro_y > ALTURA or passaro_y < 0:
            rodando = False

        desenhar_pontuacao(TELA, pontuacao)
        pygame.display.update()

    return pontuacao

# Loop principal
while True:
    tela_menu(TELA)
    pontos = jogo()
    esperando = True
    while esperando:
        tela_game_over(TELA, pontos)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
