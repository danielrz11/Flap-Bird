import pygame
import random

# Cores
AZUL = (135, 206, 235)
VERDE = (0, 200, 0)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)

def desenhar_texto(tela, texto, tamanho, cor, y_offset=0):
    fonte = pygame.font.SysFont(None, tamanho)
    texto_img = fonte.render(texto, True, cor)
    rect = texto_img.get_rect(center=(400 // 2, 600 // 2 + y_offset))
    tela.blit(texto_img, rect)

def tela_menu(tela):
    tela.fill(AZUL)
    desenhar_texto(tela, "Flappy Bird Simples", 48, PRETO, -50)
    desenhar_texto(tela, "Pressione ESPAÇO para jogar", 32, PRETO, 20)
    pygame.display.flip()

def tela_game_over(tela, pontuacao):
    tela.fill(AZUL)
    desenhar_texto(tela, "Game Over", 48, PRETO, -60)
    desenhar_texto(tela, f"Pontuação: {pontuacao}", 32, PRETO, -10)
    desenhar_texto(tela, "Pressione R para reiniciar", 32, PRETO, 40)
    desenhar_texto(tela, "ESC para sair", 32, PRETO, 80)
    pygame.display.flip()

def desenhar_pontuacao(tela, pontuacao):
    fonte = pygame.font.SysFont(None, 32)
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))

def criar_cano():
    altura_topo = random.randint(100, 400)
    return {
        'x': 400,
        'topo': altura_topo,
        'base': altura_topo + 150
    }
