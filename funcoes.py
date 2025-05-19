import pygame
import random
from config import *

# Cores
AZUL = (135, 206, 235)
VERDE = (0, 200, 0)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)

def criar_cano():
    abertura = 200  # Espaço entre os canos
    y = random.randint(abertura + 50, ALTURA - 50)
    return {'x': LARGURA, 'topo': y - abertura, 'base': y}

def desenhar_texto(tela, texto, tamanho, x, y):
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, BRANCO)
    texto_rect = texto_surface.get_rect(center=(x, y))
    tela.blit(texto_surface, texto_rect)

def desenhar_pontuacao(tela, pontuacao):
    desenhar_texto(tela, str(pontuacao), 50, LARGURA // 2, 50)

def criar_botao(tela, texto, x, y, largura, altura, cor_normal, cor_hover):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    
    # Verifica se o mouse está sobre o botão
    if x < mouse[0] < x + largura and y < mouse[1] < y + altura:
        pygame.draw.rect(tela, cor_hover, (x, y, largura, altura))
        if clique[0] == 1:  # Se o botão esquerdo do mouse foi clicado
            return True
    else:
        pygame.draw.rect(tela, cor_normal, (x, y, largura, altura))
    
    # Desenha o texto do botão
    fonte = pygame.font.Font(None, 36)
    texto_surface = fonte.render(texto, True, BRANCO)
    texto_rect = texto_surface.get_rect(center=(x + largura/2, y + altura/2))
    tela.blit(texto_surface, texto_rect)
    return False

def tela_menu(tela):
    esperando = True
    while esperando:
        tela.fill(AZUL)
        desenhar_texto(tela, "FLAPPY STAR WARS", 50, LARGURA // 2, 100)
        
        # Criar os três botões
        botao_jogar = criar_botao(tela, "JOGAR", LARGURA//2 - 100, 250, 200, 50, VERDE, (0, 200, 0))
        botao_naves = criar_botao(tela, "NAVES", LARGURA//2 - 100, 320, 200, 50, VERDE, (0, 200, 0))
        botao_funcoes = criar_botao(tela, "FUNÇÕES", LARGURA//2 - 100, 390, 200, 50, VERDE, (0, 200, 0))
        
        # Adicionar texto no canto inferior direito
        fonte = pygame.font.Font(None, 24)
        texto_surface = fonte.render("APERTE ESC PARA SAIR", True, BRANCO)
        texto_rect = texto_surface.get_rect(bottomright=(LARGURA - 10, ALTURA - 10))
        tela.blit(texto_surface, texto_rect)
        
        pygame.display.update()
        
        # Verificar cliques nos botões
        if botao_jogar:
            esperando = False
        elif botao_naves:
            selecionar_nave(tela)
        elif botao_funcoes:
            # Aqui você pode adicionar a lógica para a tela de funções
            pass
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

def selecionar_nave(tela):
    selecionando = True
    indice_atual = nave_selecionada
    
    while selecionando:
        tela.fill(AZUL)
        desenhar_texto(tela, "SELECIONE SUA NAVE", 50, LARGURA // 2, 100)
        
        # Desenhar nave atual
        if NAVE_IMGS:
            nave_img = NAVE_IMGS[indice_atual]
            # Desenhar a nave em tamanho maior para melhor visualização (3x o tamanho do jogo)
            nave_grande = pygame.transform.scale(nave_img, (120, 120))
            rect = nave_grande.get_rect(center=(LARGURA // 2, ALTURA // 2))
            tela.blit(nave_grande, rect)
            
            # Desenhar nome da nave
            nome_nave = NAVES[indice_atual].replace("nave_", "").replace(".png", "").upper()
            desenhar_texto(tela, nome_nave, 30, LARGURA // 2, ALTURA // 2 + 100)
            
            # Desenhar instruções
            desenhar_texto(tela, "← → para mudar", 24, LARGURA // 2, ALTURA // 2 + 150)
            desenhar_texto(tela, "ENTER para confirmar", 24, LARGURA // 2, ALTURA // 2 + 180)
            desenhar_texto(tela, "ESC para voltar", 24, LARGURA // 2, ALTURA // 2 + 210)
        else:
            desenhar_texto(tela, "Nenhuma nave disponível", 30, LARGURA // 2, ALTURA // 2)
        
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    set_nave_selecionada(indice_atual)  # Salva a seleção
                    selecionando = False
                elif evento.key == pygame.K_LEFT and NAVE_IMGS:
                    indice_atual = (indice_atual - 1) % len(NAVE_IMGS)
                elif evento.key == pygame.K_RIGHT and NAVE_IMGS:
                    indice_atual = (indice_atual + 1) % len(NAVE_IMGS)
                elif evento.key == pygame.K_ESCAPE:
                    selecionando = False

def tela_game_over(tela, pontuacao):
    # Removida a tela de game over, retorna imediatamente
    return
