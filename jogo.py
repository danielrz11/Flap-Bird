import pygame
import random
import os
pygame.init()  # Inicializa antes de qualquer uso de fonte

from funcoes import *
from config import *

# Configurações
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
    tiros = []  # Lista para armazenar os tiros
    velocidade_tiro = 10  # Velocidade dos tiros
    inimigos = []  # Lista para armazenar os inimigos
    contador_frames = 0  # Contador para controlar o spawn de inimigos
    explosoes = []  # Lista local para armazenar explosões

    relogio = pygame.time.Clock()
    rodando = True
    colisao = False  # Inicializa colisao para evitar erro de variável não definida

    # Obter a nave selecionada
    nave_atual = get_nave_atual()
    indice_nave = get_indice_nave_atual()
    # Obter o fundo selecionado
    fundo_atual = get_fundo_atual()
    # Obter o cano correspondente ao fundo
    cano_atual = get_cano_atual()
    cano_atual_inv = pygame.transform.rotate(cano_atual, 180) if cano_atual else None

    if nave_atual:
        largura, altura = nave_atual.get_size()
    else:
        largura, altura = 40, 40  # valores padrão caso nave_atual seja None

    if indice_nave == 0:
         pulo *= 0.75
    if indice_nave == 1:
        passaro_x = 30
    if indice_nave == 2:
        velocidade_tiro *= 4
    if indice_nave == 3:   
        velocidade_cano *= 2
        velocidade_tiro *= 2

    while rodando:
        try:
            relogio.tick(60)
            contador_frames += 1
            
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
                    if evento.key == pygame.K_RIGHT:
                        # Criar novo tiro quando a seta direita é pressionada
                        tiros.append({
                            'x': passaro_x + 20,  # Posição x do tiro (à direita da nave)
                            'y': passaro_y,       # Posição y do tiro (mesma altura da nave)
                            'largura': 20,        # Largura do tiro
                            'altura': 5           # Altura do tiro
                        })
                        som_blaster.play()  # Tocar som do blaster ao atirar
                    if indice_nave == 3:
                        if evento.key == pygame.K_f:
                            gravidade *= 2  # Aumentar a gravidade
                    
                if evento.type == pygame.KEYUP and indice_nave == 3:
                    if evento.key == pygame.K_f:
                        gravidade /= 2


            velocidade_y += gravidade
            passaro_y += velocidade_y

            # Atualizar e desenhar tiros
            for tiro in tiros[:]:
                tiro['x'] += velocidade_tiro
                # Desenhar tiro
                pygame.draw.rect(TELA, VERMELHO, (tiro['x'], tiro['y'], tiro['largura'], tiro['altura']))
                
                # Verificar colisão do tiro com inimigos
                tiro_rect = pygame.Rect(tiro['x'], tiro['y'], tiro['largura'], tiro['altura'])
                for inimigo in inimigos[:]:
                    inimigo_rect = pygame.Rect(inimigo['x'], inimigo['y'], inimigo['largura'], inimigo['altura'])
                    if tiro_rect.colliderect(inimigo_rect):
                        # Criar explosão no centro do inimigo
                        criar_explosao(explosoes, inimigo['x'] + inimigo['largura']//2, inimigo['y'] + inimigo['altura']//2)
                        som_explosao.play()
                        inimigos.remove(inimigo)
                        tiros.remove(tiro)
                        pontuacao += 1 
                        break
                
                # Remover tiros que saíram da tela
                if tiro['x'] > LARGURA:
                    tiros.remove(tiro)

            # Atualizar e desenhar explosões
            for explosao in explosoes[:]:
                try:
                    explosao['raio'] += explosao['velocidade']
                    explosao['alpha'] -= 10  # Diminuir a transparência
                    
                    # Criar uma superfície para a explosão com transparência
                    explosao_surface = pygame.Surface((explosao['raio'] * 2, explosao['raio'] * 2), pygame.SRCALPHA)
                    pygame.draw.circle(explosao_surface, (255, 165, 0, explosao['alpha']), 
                                     (explosao['raio'], explosao['raio']), explosao['raio'])
                    
                    # Desenhar a explosão
                    TELA.blit(explosao_surface, 
                             (explosao['x'] - explosao['raio'], explosao['y'] - explosao['raio']))
                    
                    # Remover explosão quando ela terminar
                    if explosao['raio'] >= explosao['max_raio'] or explosao['alpha'] <= 0:
                        explosoes.remove(explosao)
                except:
                    # Se houver qualquer erro com a explosão, remova-a
                    if explosao in explosoes:
                        explosoes.remove(explosao)

            # Limitar o número máximo de explosões
            if len(explosoes) > 10:
                explosoes = explosoes[-10:]

            # Spawn de inimigos
            if indice_nave == 1:    
                TEMPO_MIN_INIMIGO = 30
            else:
                TEMPO_MIN_INIMIGO = 60

            if contador_frames >= TEMPO_MIN_INIMIGO:
                if random.random() < PROBABILIDADE_INIMIGO:
                    inimigos.append({
                        'x': LARGURA,
                        'y': random.randint(50, ALTURA - 50),
                        'largura': 80,
                        'altura': 80
                    })
                    contador_frames = 0

            # Atualizar e desenhar inimigos
            for inimigo in inimigos[:]:
                inimigo['x'] -= velocidade_cano * 1.25
                # Desenhar inimigo
                if INIMIGO_IMG:
                    try:
                        inimigo_redimensionado = pygame.transform.scale(INIMIGO_IMG, (80, 80))
                        TELA.blit(inimigo_redimensionado, (inimigo['x'], inimigo['y']))
                    except:
                        pygame.draw.rect(TELA, VERMELHO, (inimigo['x'], inimigo['y'], inimigo['largura'], inimigo['altura']))
                else:
                    pygame.draw.rect(TELA, VERMELHO, (inimigo['x'], inimigo['y'], inimigo['largura'], inimigo['altura']))
                # Remover inimigos que saíram da tela
                if inimigo['x'] < -inimigo['largura']:
                    inimigos.remove(inimigo)

            # Desenhar nave
            if nave_atual:
                try:
                    nave_redimensionada = nave_atual
                    nave_rect = nave_redimensionada.get_rect(center=(passaro_x, int(passaro_y)))
                    TELA.blit(nave_redimensionada, nave_rect)
                except:
                    pygame.draw.circle(TELA, AMARELO, (passaro_x, int(passaro_y)), 20)
            else:
                pygame.draw.circle(TELA, AMARELO, (passaro_x, int(passaro_y)), 20)

            # Desenhar canos
            for cano in canos:
                cano['x'] = int(cano['x'] - velocidade_cano)
                if cano_atual and cano_atual_inv:
                    try:
                        # Cano superior
                        TELA.blit(cano_atual_inv, (cano['x'], cano['topo'] - 500))
                        # Cano inferior
                        TELA.blit(cano_atual, (cano['x'], cano['base']))
                    except:
                        pygame.draw.rect(TELA, VERDE, (cano['x'], 0, largura_cano, cano['topo']))
                        pygame.draw.rect(TELA, VERDE, (cano['x'], cano['base'], largura_cano, ALTURA))
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
                if cano['x'] + largura_cano < passaro_x and not cano.get('pontuado', False):
                    pontuacao += 1
                    cano['pontuado'] = True

            # Verificar colisões
            if nave_atual:
                passaro_rect = pygame.Rect(passaro_x - largura/2, passaro_y - altura/2, largura, altura)
            else:
                # Se não houver nave, usar um retângulo padrão
                passaro_rect = pygame.Rect(passaro_x - 20, passaro_y - 20, 40, 40)
                
            colisao = False
            for cano in canos:
                cano_superior = pygame.Rect(cano['x'], 0, largura_cano, cano['topo'])
                cano_inferior = pygame.Rect(cano['x'], cano['base'], largura_cano, ALTURA - cano['base'])
                if passaro_rect.colliderect(cano_superior) or passaro_rect.colliderect(cano_inferior):
                    colisao = True
                    rodando = False

            if passaro_y > ALTURA or passaro_y < 0:
                rodando = False

            desenhar_texto(TELA, str(pontuacao), 50, LARGURA // 2, 50)
            pygame.display.update()

        except Exception as e:
            print(f"Erro no jogo: {e}")
            rodando = False

        if not rodando and colisao:  # Só mostra a explosão se houve colisão com cano
            # Animação de explosão final
            explosion_folder = os.path.join("assets", "Circle_explosion")
            explosion_imgs = []
            for i in range(1, 11):
                img_path = os.path.join(explosion_folder, f"Circle_explosion{i}.png")
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path).convert_alpha()
                    explosion_imgs.append(img)
            nave_centro_x = passaro_x
            nave_centro_y = int(passaro_y)
            som_explosao.play()
            for img in explosion_imgs:
                rect = img.get_rect(center=(nave_centro_x, nave_centro_y))
                TELA.blit(img, rect)
                pygame.display.update()
                pygame.time.delay(60)
            pygame.time.delay(500)

    return pontuacao

# Loop principal
while True:
    tela_menu(TELA)
    pontos = jogo()
    set_melhor_pontuacao(pontos)
    resultado = tela_game_over(TELA, pontos)
    if resultado == "menu":
        continue  # Volta para o menu principal
    if pontos > melhor_pontuacao:
        melhor_pontuacao = pontos
        print(f"Novo recorde: {melhor_pontuacao}")
