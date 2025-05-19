import pygame
import os

# Configurações da tela
LARGURA = 400
ALTURA = 600

# Cores
AZUL = (135, 206, 235)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

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

# Carregando outras imagens
try:
    PIPE_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "pipe.png"))
    PIPE_IMG = pygame.transform.scale(PIPE_IMG, (70, 500))
    PIPE_IMG_INV = pygame.transform.rotate(PIPE_IMG, 180)
    
    BG_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "background.png.png"))
    BG_IMG = pygame.transform.scale(BG_IMG, (LARGURA, ALTURA))
except FileNotFoundError:
    print("Aviso: Algumas imagens não encontradas. Usando formas geométricas simples.")
    PIPE_IMG = None
    PIPE_IMG_INV = None
    BG_IMG = None

# Configurações do jogo
GRAVIDADE = 0.08  # Aproximadamente 1/6 da gravidade original (0.5)
PULO = -4  # Reduzido pela metade para combinar com a gravidade menor
VELOCIDADE_CANO = 2
DISTANCIA_ENTRE_CANOS = 300
LARGURA_CANO = 70

# Variável global para a nave selecionada
nave_selecionada = 0
melhor_pontuacao = 0  # Variável para armazenar a melhor pontuação

def get_nave_atual():
    """Retorna a imagem da nave atualmente selecionada"""
    if NAVE_IMGS and 0 <= nave_selecionada < len(NAVE_IMGS):
        return NAVE_IMGS[nave_selecionada]
    return None

def set_nave_selecionada(indice):
    """Define a nave selecionada"""
    global nave_selecionada
    if NAVE_IMGS:
        nave_selecionada = indice % len(NAVE_IMGS)

def atualizar_melhor_pontuacao(pontuacao):
    """Atualiza a melhor pontuação se necessário"""
    global melhor_pontuacao
    if pontuacao > melhor_pontuacao:
        melhor_pontuacao = pontuacao 