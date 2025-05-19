import pygame
pygame.init()  # Inicializa antes de qualquer uso de fonte

from funcoes import (
    tela_menu, 
    tela_game_over, 
    criar_cano, 
    desenhar_pontuacao, 
    AZUL, VERDE, AMARELO, get_nave_atual
)
from config import *

# Configurações
LARGURA, ALTURA = 400, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Star Wars")

def jogo():
    gravidade = GRAVIDADE
    pulo = PULO
    velocidade_cano = VELOCIDADE_CANO
    distancia_entre_canos = DISTANCIA_ENTRE_CANOS
    largura_cano = LARGURA_CANO
    passaro_x = 50
    passaro_y = ALTURA // 2
    velocidade_y = 0
    canos = [criar_cano()]
    pontuacao = 0
    canos_passados = set()  # Conjunto para rastrear canos já pontuados

    relogio = pygame.time.Clock()
    rodando = True

    # Obter a nave selecionada
    nave_atual = get_nave_atual()

    while rodando:
        relogio.tick(60)
        
        # Desenhar fundo
        if BG_IMG:
            TELA.blit(BG_IMG, (0, 0))
        else:
            TELA.fill(AZUL)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                velocidade_y = pulo

        velocidade_y += gravidade
        passaro_y += velocidade_y

        # Desenhar nave
        if nave_atual:
            # Ajustar o tamanho da nave para 40x40 pixels
            nave_redimensionada = pygame.transform.scale(nave_atual, (80, 80))
            nave_rect = nave_redimensionada.get_rect(center=(passaro_x, int(passaro_y)))
            TELA.blit(nave_redimensionada, nave_rect)
        else:
            pygame.draw.circle(TELA, AMARELO, (passaro_x, int(passaro_y)), 20)

        # Desenhar canos
        for cano in canos:
            cano['x'] -= velocidade_cano
            if PIPE_IMG and PIPE_IMG_INV:
                # Cano superior
                TELA.blit(PIPE_IMG_INV, (cano['x'], cano['topo'] - 500))
                # Cano inferior
                TELA.blit(PIPE_IMG, (cano['x'], cano['base']))
            else:
                pygame.draw.rect(TELA, VERDE, (cano['x'], 0, largura_cano, cano['topo']))
                pygame.draw.rect(TELA, VERDE, (cano['x'], cano['base'], largura_cano, ALTURA))

        if canos[-1]['x'] < LARGURA - distancia_entre_canos:
            canos.append(criar_cano())
        if canos[0]['x'] < -largura_cano:
            canos.pop(0)

        # Verificar pontuação
        for cano in canos:
            # Cria uma identificação única para cada cano
            cano_id = id(cano)
            # Se o cano ainda não foi pontuado e o jogador passou por ele
            if cano_id not in canos_passados and cano['x'] + largura_cano < passaro_x:
                pontuacao += 1
                canos_passados.add(cano_id)

        # Verificar colisões
        passaro_rect = pygame.Rect(passaro_x - 20, passaro_y - 20, 40, 40)  # Hitbox de 40x40 pixels
        for cano in canos:
            cano_superior = pygame.Rect(cano['x'], 0, largura_cano, cano['topo'])
            cano_inferior = pygame.Rect(cano['x'], cano['base'], largura_cano, ALTURA - cano['base'])
            if passaro_rect.colliderect(cano_superior) or passaro_rect.colliderect(cano_inferior):
                rodando = False

        if passaro_y > ALTURA or passaro_y < 0:
            rodando = False

        desenhar_pontuacao(TELA, pontuacao)
        pygame.display.update()

# Loop principal
while True:
    tela_menu(TELA)
    jogo()  # Removido o retorno da pontuação já que não vamos mais mostrar a tela de game over
