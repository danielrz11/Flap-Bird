import pygame
import random


pygame.init()
LARGURA, ALTURA = 400, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Bird Simples")

AZUL = (135, 206, 235)
VERDE = (0, 200, 0)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

fonte = pygame.font.SysFont(None, 48)
pequena = pygame.font.SysFont(None, 32)


def desenhar_texto(texto, fonte, cor, y_offset=0):
    texto_img = fonte.render(texto, True, cor)
    rect = texto_img.get_rect(center=(LARGURA//2, ALTURA//2 + y_offset))
    TELA.blit(texto_img, rect)

def tela_menu():
    esperando = True
    while esperando:
        TELA.fill(AZUL)
        desenhar_texto("Flappy Bird Simples", fonte, PRETO, -50)
        desenhar_texto("Pressione ESPAÇO para jogar", pequena, PRETO, 20)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False

def tela_game_over():
    esperando = True
    while esperando:
        TELA.fill(AZUL)
        desenhar_texto("Game Over", fonte, PRETO, -50)
        desenhar_texto("Pressione ESPAÇO para reiniciar", pequena, PRETO, 20)
        desenhar_texto("ESC para sair", pequena, PRETO, 60)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def criar_cano():
    altura_topo = random.randint(100, 400)
    return {'x': LARGURA, 'topo': altura_topo, 'base': altura_topo + 150}

def jogo():
    gravidade = 0.5
    pulo = -10
    velocidade_cano = 3
    distancia_entre_canos = 200
    largura_cano = 70
    passaro_x = 50
    passaro_y = ALTURA // 2
    velocidade_y = 0
    canos = [criar_cano()]

    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        relogio.tick(60)
        TELA.fill(AZUL)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
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
            if passaro_x + 20 > cano['x'] and passaro_x - 20 < cano['x'] + largura_cano:
                if passaro_y - 20 < cano['topo'] or passaro_y + 20 > cano['base']:
                    rodando = False
        if passaro_y > ALTURA or passaro_y < 0:
            rodando = False

        pygame.display.update()
