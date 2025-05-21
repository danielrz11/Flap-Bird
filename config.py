import pygame
import os

# Configurações da tela
LARGURA = 400
ALTURA = 600

# Cores
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (135, 206, 235)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Configurações do jogo
GRAVIDADE = 0.08  # Aproximadamente 1/6 da gravidade original (0.5)
PULO = -4  # Reduzido pela metade para combinar com a gravidade menor
VELOCIDADE_CANO = 2
DISTANCIA_ENTRE_CANOS = 300
LARGURA_CANO = 70  # Aumentado de 70 para 100

# Carregando imagens
ASSETS_DIR = "assets"

# Lista de naves disponíveis
NAVES = [
    "nave_xwing.png",
    "nave_mileniumfalcon.png",
    "nave_cacaTIE.png",
    "nave_cinza.png",
    "nave_laranja.png"
]

# Lista de fundos disponíveis
FUNDOS = [
    "fundo_estrela da morte.png"
]

# Lista de canos correspondentes aos fundos
CANOS = [
    "cano_estrela da morte.png"
]

# Carregando imagens das naves
NAVE_IMGS = []
try:
    for nave in NAVES:
        img = pygame.image.load(os.path.join(ASSETS_DIR, nave))
        # Ajustando o tamanho para ser aproximadamente igual ao círculo do pássaro (raio 20 = diâmetro 40)
        img = pygame.transform.scale(img, (40, 40))  # Tamanho fixo de 40x40 pixels
        NAVE_IMGS.append(img)
    print(f"Carregadas {len(NAVE_IMGS)} naves com sucesso!")
except FileNotFoundError as e:
    print(f"Erro ao carregar imagens das naves: {e}")
    NAVE_IMGS = []
except pygame.error as e:
    print(f"Erro do Pygame ao carregar imagens: {e}")
    NAVE_IMGS = []

# Carregando imagens dos fundos
BG_IMGS = []
try:
    for fundo in FUNDOS:
        img = pygame.image.load(os.path.join(ASSETS_DIR, fundo))
        img = pygame.transform.scale(img, (LARGURA, ALTURA))
        BG_IMGS.append(img)
    print(f"Carregados {len(BG_IMGS)} fundos com sucesso!")
except FileNotFoundError as e:
    print(f"Erro ao carregar imagens dos fundos: {e}")
    BG_IMGS = []
except pygame.error as e:
    print(f"Erro do Pygame ao carregar imagens: {e}")
    BG_IMGS = []

# Carregando imagens dos canos
PIPE_IMGS = []
try:
    for cano in CANOS:
        img = pygame.image.load(os.path.join(ASSETS_DIR, cano))
        img = pygame.transform.scale(img, (LARGURA_CANO, 500))
        PIPE_IMGS.append(img)
    print(f"Carregados {len(PIPE_IMGS)} canos com sucesso!")
except FileNotFoundError as e:
    print(f"Erro ao carregar imagens dos canos: {e}")
    PIPE_IMGS = []
except pygame.error as e:
    print(f"Erro do Pygame ao carregar imagens: {e}")
    PIPE_IMGS = []

# Variável global para a nave selecionada
nave_selecionada = 0
fundo_selecionado = 0
melhor_pontuacao = 0

def get_nave_atual():
    """Retorna a imagem da nave atualmente selecionada"""
    if NAVE_IMGS and 0 <= nave_selecionada < len(NAVE_IMGS):
        return NAVE_IMGS[nave_selecionada]
    return None

def get_fundo_atual():
    """Retorna a imagem do fundo atualmente selecionado"""
    if BG_IMGS and 0 <= fundo_selecionado < len(BG_IMGS):
        return BG_IMGS[fundo_selecionado]
    return None

def get_cano_atual():
    """Retorna a imagem do cano correspondente ao fundo atual"""
    if PIPE_IMGS and 0 <= fundo_selecionado < len(PIPE_IMGS):
        return PIPE_IMGS[fundo_selecionado]
    return None

def set_nave_selecionada(indice):
    """Define a nave selecionada"""
    global nave_selecionada
    if NAVE_IMGS:
        nave_selecionada = indice % len(NAVE_IMGS)

def set_fundo_selecionado(indice):
    """Define o fundo selecionado"""
    global fundo_selecionado
    if BG_IMGS:
        fundo_selecionado = indice % len(BG_IMGS)

def get_melhor_pontuacao():
    """Retorna a melhor pontuação"""
    return melhor_pontuacao

def set_melhor_pontuacao(pontos):
    """Define a melhor pontuação"""
    global melhor_pontuacao
    if pontos > melhor_pontuacao:
        melhor_pontuacao = pontos 