import pygame
pygame.init()  # Inicializa antes de qualquer uso de fonte

from funcoes import (
    tela_menu, 
    tela_game_over, 
    criar_cano, 
    desenhar_pontuacao, 
    AZUL, VERDE, AMARELO, get_nave_atual, get_fundo_atual, get_cano_atual
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
    tiros = []  # Lista para armazenar os tiros
    velocidade_tiro = 10  # Velocidade dos tiros

    relogio = pygame.time.Clock()
    rodando = True

    # Obter a nave selecionada
    nave_atual = get_nave_atual()
    # Obter o fundo selecionado
    fundo_atual = get_fundo_atual()
    # Obter o cano correspondente ao fundo
    cano_atual = get_cano_atual()
    cano_atual_inv = pygame.transform.rotate(cano_atual, 180) if cano_atual else None

    while rodando:
        relogio.tick(60)
        
        # Desenhar fundo
        if fundo_atual:
            TELA.blit(fundo_atual, (0, 0))
        else:
            TELA.fill(AZUL)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    velocidade_y = pulo
                elif evento.key == pygame.K_RIGHT:
                    # Criar novo tiro quando a seta direita é pressionada
                    tiros.append({
                        'x': passaro_x + 40,  # Posição x do tiro (à direita da nave)
                        'y': passaro_y,       # Posição y do tiro (mesma altura da nave)
                        'largura': 20,        # Largura do tiro
                        'altura': 5           # Altura do tiro
                    })

        velocidade_y += gravidade
        passaro_y += velocidade_y

        # Atualizar e desenhar tiros
        for tiro in tiros[:]:
            tiro['x'] += velocidade_tiro
            # Desenhar tiro
            pygame.draw.rect(TELA, VERDE, (tiro['x'], tiro['y'], tiro['largura'], tiro['altura']))
            # Remover tiros que saíram da tela
            if tiro['x'] > LARGURA:
                tiros.remove(tiro)

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
            if cano_atual and cano_atual_inv:
                # Cano superior
                TELA.blit(cano_atual_inv, (cano['x'], cano['topo'] - 500))
                # Cano inferior
                TELA.blit(cano_atual, (cano['x'], cano['base']))
            else:
                pygame.draw.rect(TELA, VERDE, (cano['x'], 0, largura_cano, cano['topo']))
                pygame.draw.rect(TELA, VERDE, (cano['x'], cano['base'], largura_cano, ALTURA))

        if canos[-1]['x'] < LARGURA - distancia_entre_canos:
            canos.append(criar_cano())
        if canos[0]['x'] < -largura_cano:
            canos.pop(0)

        # Verificar pontuação
        for cano in canos:
            # Verifica se o jogador passou pelo cano
            if cano['x'] + largura_cano < passaro_x:
                # Cria uma identificação única para cada cano usando sua posição inicial
                cano_id = f"{cano['x']}_{cano['topo']}_{cano['base']}"
                if cano_id not in canos_passados:
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

        desenhar_pontuacao(TELA, pontuacao // 25)  # Dividindo a pontuação por 25
        pygame.display.update()

    return pontuacao // 25  # Também retornando a pontuação dividida por 25

# Loop principal
while True:
    tela_menu(TELA)
    pontos = jogo()
    if pontos > melhor_pontuacao:
        melhor_pontuacao = pontos
        print(f"Novo recorde: {melhor_pontuacao}")  # Debug para verificar se está atualizando
