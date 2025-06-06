import pygame
import random
from config import *
import os

# Cores
AZUL = (135, 206, 235)
VERDE = (0, 200, 0)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)

# Lista para armazenar explosões
explosoes = []

# Lista para armazenar explosões pendentes
explosoes_pendentes = []

# Inicializar o sistema de música
pygame.mixer.init()

# Carregar músicas e efeitos sonoros
try:
    pygame.mixer.music.load(os.path.join("assets", "inicial.mp3"))
    pygame.mixer.music.set_volume(0.5)  # Volume em 50%
except:
    print("Erro ao carregar música inicial")

# Carregar som do blaster
try:
    som_blaster = pygame.mixer.Sound(os.path.join("assets", "blaster.mp3"))
    som_blaster.set_volume(0.3)  # Volume em 30%
except:
    print("Erro ao carregar som do blaster")
    som_blaster = None

# Carregar som da explosão
try:
    som_explosao = pygame.mixer.Sound(os.path.join("assets", "explosion_old.mp3"))
    som_explosao.set_volume(0.3)  # Volume em 30%
    print("Som da explosão carregado com sucesso!")  # Debug print
except Exception as e:
    print(f"Erro ao carregar som da explosão: {e}")  # Debug print com erro específico
    som_explosao = None

def iniciar_musica_menu():
    try:
        pygame.mixer.music.load(os.path.join("assets", "inicial.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 significa loop infinito
    except:
        print("Erro ao iniciar música do menu")

def iniciar_musica_jogo():
    try:
        pygame.mixer.music.load(os.path.join("assets", "música do bar.mp3"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # -1 significa loop infinito
    except:
        print("Erro ao iniciar música do jogo")

def criar_cano():
    abertura = 200  # Espaço entre os canos
    y = random.randint(abertura + 50, ALTURA - 50)
    return {'x': LARGURA, 'topo': y - abertura, 'base': y}

def criar_explosao(explosoes, x, y):
    explosoes.append({
        'x': x,
        'y': y,
        'raio': 5,
        'max_raio': 40,
        'velocidade': 2,
        'alpha': 255  # Para controlar a transparência
    })

def desenhar_texto(tela, texto, tamanho, x, y):
    # Tenta carregar uma fonte TTF personalizada, senão usa a padrão
    try:
        fonte = pygame.font.Font(os.path.join("assets", "Death Star.otf"), tamanho)
    except:
        fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, AMARELO)
    texto_rect = texto_surface.get_rect(center=(x, y))
    tela.blit(texto_surface, texto_rect)

# def desenhar_pontuacao(tela, pontuacao):
#     desenhar_texto(tela, str(pontuacao), 50, LARGURA // 2, 50)

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
    texto_surface = fonte.render(texto, True, PRETO)
    texto_rect = texto_surface.get_rect(center=(x + largura/2, y + altura/2))
    tela.blit(texto_surface, texto_rect)
    return False

def tela_menu(tela):
    esperando = True
    # Iniciar música de fundo do menu
    iniciar_musica_menu()
    
    # Carregar imagem de fundo do menu
    try:
        fundo_menu = pygame.image.load(os.path.join("assets", "tela de início.png"))
        fundo_menu = pygame.transform.scale(fundo_menu, (LARGURA, ALTURA))
    except:
        fundo_menu = None

    while esperando:
        # Desenhar fundo do menu
        if fundo_menu:
            tela.blit(fundo_menu, (0, 0))
        else:
            tela.fill(AZUL)
        
        # Mostrar melhor pontuação na parte inferior
        melhor_pontuacao = get_melhor_pontuacao()
        desenhar_texto(tela, f"RECORDE: {melhor_pontuacao}", 36, LARGURA // 2, ALTURA - 50)
        
        # Criar os três botões centralizados
        botao_jogar = criar_botao(tela, "JOGAR", LARGURA//2 - 100, 250, 200, 50, AMARELO, (200, 200, 0))
        botao_naves = criar_botao(tela, "NAVES", LARGURA//2 - 100, 320, 200, 50, AMARELO, (200, 200, 0))
        botao_fundos = criar_botao(tela, "FUNDOS", LARGURA//2 - 100, 390, 200, 50, AMARELO, (200, 200, 0))
        
        # Adicionar texto no canto inferior direito
        fonte = pygame.font.Font(None, 24)
        texto_surface = fonte.render("APERTE ESC PARA SAIR", True, BRANCO)
        texto_rect = texto_surface.get_rect(bottomright=(LARGURA - 10, ALTURA - 10))
        tela.blit(texto_surface, texto_rect)
        
        pygame.display.update()
        
        # Verificar cliques nos botões
        if botao_jogar:
            pygame.mixer.music.stop()  # Parar música do menu
            iniciar_musica_jogo()  # Iniciar música do jogo
            esperando = False
        elif botao_naves:
            selecionar_nave(tela)
        elif botao_fundos:
            selecionar_fundo(tela)
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Parar música ao sair
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()  # Parar música ao sair
                pygame.quit()
                exit()

def selecionar_nave(tela):
    selecionando = True
    global indice_nave
    
    while selecionando:
        tela.fill(PRETO)
        desenhar_texto(tela, "SELECIONE SUA NAVE", 30, LARGURA // 2, 100)
        
        # Desenhar nave atual
        if NAVE_IMGS:
            nave_img = NAVE_IMGS[indice_nave]
            # Desenhar a nave em tamanho maior para melhor visualização (3x o tamanho do jogo)
            largura, altura = nave_img.get_size()
            escala = 3
            medidas = (largura*escala, altura*escala)
            nave_grande = pygame.transform.scale(nave_img, medidas)
            rect = nave_grande.get_rect(center=(LARGURA // 2, ALTURA // 2))
            tela.blit(nave_grande, rect)
            
            # Desenhar nome da nave
            nome_nave = NAVES[indice_nave].replace("nave_", "").replace(".png", "").upper()
            desenhar_texto(tela, nome_nave, 30, LARGURA // 2, ALTURA // 2 + 100)
            
            # Desenhar instruções
            if indice_nave == 3:
                desenhar_texto(tela, "Modo dificil!   Use a Forca (F)", 24, LARGURA // 2, ALTURA // 2 + 150)
            desenhar_texto(tela, "< > para mudar", 24, LARGURA // 2, ALTURA // 2 + 180)
            desenhar_texto(tela, "ENTER para confirmar", 24, LARGURA // 2, ALTURA // 2 + 210)
            desenhar_texto(tela, "ESC para voltar", 24, LARGURA // 2, ALTURA // 2 + 230)
        else:
            desenhar_texto(tela, "Nenhuma nave disponível", 30, LARGURA // 2, ALTURA // 2)
        
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Parar música ao sair
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    set_indice_nave(indice_nave)  # Salva a seleção
                    selecionando = False
                elif evento.key == pygame.K_LEFT and NAVE_IMGS:
                    indice_nave = (indice_nave - 1) % len(NAVE_IMGS)
                elif evento.key == pygame.K_RIGHT and NAVE_IMGS:
                    indice_nave = (indice_nave + 1) % len(NAVE_IMGS)
                elif evento.key == pygame.K_ESCAPE:
                    selecionando = False

                    

def selecionar_fundo(tela):
    selecionando = True
    indice_atual = fundo_selecionado
    
    while selecionando:
        tela.fill(PRETO)
        desenhar_texto(tela, "SELECIONE O FUNDO", 30, LARGURA // 2, 100)
        
        # Desenhar fundo atual
        if BG_IMGS:
            fundo_img = BG_IMGS[indice_atual]
            # Calcular dimensões mantendo proporção 2:3
            preview_largura = 200  # Reduzido de 300 para 200
            preview_altura = int(preview_largura * 1.5)  # 2:3 proporção
            # Desenhar o fundo em tamanho menor para visualização
            fundo_preview = pygame.transform.scale(fundo_img, (preview_largura, preview_altura))
            rect = fundo_preview.get_rect(center=(LARGURA // 2, ALTURA // 2))
            tela.blit(fundo_preview, rect)
            
            # Desenhar nome do fundo
            nome_fundo = FUNDOS[indice_atual].replace("fundo_", "").replace(".png", "").replace("_", " ")
            desenhar_texto(tela, nome_fundo, 30, LARGURA // 2, ALTURA // 2 + preview_altura//2 + 30)
            
            # Desenhar instruções
            desenhar_texto(tela, "< > para mudar", 24, LARGURA // 2, ALTURA // 2 + preview_altura//2 + 70)
            desenhar_texto(tela, "ENTER para confirmar", 24, LARGURA // 2, ALTURA // 2 + preview_altura//2 + 100)
            desenhar_texto(tela, "ESC para voltar", 24, LARGURA // 2, ALTURA // 2 + preview_altura//2 + 130)
        else:
            desenhar_texto(tela, "Nenhum fundo disponível", 30, LARGURA // 2, ALTURA // 2)
        
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.mixer.music.stop()  # Parar música ao sair
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    set_fundo_selecionado(indice_atual)  # Salva a seleção
                    selecionando = False
                elif evento.key == pygame.K_LEFT and BG_IMGS:
                    indice_atual = (indice_atual - 1) % len(BG_IMGS)
                elif evento.key == pygame.K_RIGHT and BG_IMGS:
                    indice_atual = (indice_atual + 1) % len(BG_IMGS)
                elif evento.key == pygame.K_ESCAPE:
                    selecionando = False

def tela_game_over(tela, pontuacao):
    esperando = True
    
    # Carregar imagem de fundo do game over
    try:
        fundo_game_over = pygame.image.load(os.path.join("assets", "tela de início.png"))
        fundo_game_over = pygame.transform.scale(fundo_game_over, (LARGURA, ALTURA))
    except:
        fundo_game_over = None

    while esperando:
        # Desenhar fundo
        if fundo_game_over:
            tela.blit(fundo_game_over, (0, 0))
        else:
            tela.fill(PRETO)
        
        # Desenhar título e pontuação na parte inferior
        desenhar_texto(tela, "GAME OVER", 60, LARGURA // 2, ALTURA - 300)
        desenhar_texto(tela, f"Pontuacao: {pontuacao}", 36, LARGURA // 2, ALTURA - 200)
        
        # Mostrar melhor pontuação
        melhor_pontuacao = get_melhor_pontuacao()
        if pontuacao > melhor_pontuacao:
            desenhar_texto(tela, "NOVO RECORDE!", 30, LARGURA // 2, ALTURA - 150)
        else:
            desenhar_texto(tela, f"Recorde: {melhor_pontuacao}", 30, LARGURA // 2, ALTURA - 150)
        
        # Criar botão do menu principal
        botao_menu = criar_botao(tela, "MENU PRINCIPAL", LARGURA//2 - 150, ALTURA - 100, 300, 50, AMARELO, (200, 200, 0))
        
        # Adicionar texto no canto inferior direito
        fonte = pygame.font.Font(None, 24)
        texto_surface = fonte.render("APERTE ESC PARA SAIR", True, BRANCO)
        texto_rect = texto_surface.get_rect(bottomright=(LARGURA - 10, ALTURA - 10))
        tela.blit(texto_surface, texto_rect)
        
        pygame.display.update()
        
        # Verificar cliques nos botões
        if botao_menu:
            return "menu"  # Retorna para o menu principal
            
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN: 
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if evento.key == pygame.K_SPACE:
                    return "menu"
