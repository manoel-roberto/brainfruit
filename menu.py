"""
Módulo do menu principal do jogo BrainFruit.
Renderiza botões de seleção de dificuldade, botão de créditos e plano de fundo animado (GIF).
"""

import pygame
import os

# Tenta importar PIL para decodificar quadros de arquivos GIF animados
try:
    from PIL import Image, ImageSequence
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

from config import *


class Menu:
    """
    Gerencia os botões, desenho do título, animação de fundo e detecção de cliques do menu principal.
    """

    def __init__(self):
        """
        Configura fontes, dimensões dos botões e carrega os quadros do GIF animado de fundo.
        """
        self.fonte_titulo = pygame.font.SysFont(None, 72)
        self.fonte_menu = pygame.font.SysFont(None, 48)
        self.fonte_pequena = pygame.font.SysFont(None, 32)

        # Botões de escolha de dificuldade e navegação
        self.btn_facil = pygame.Rect(0, 0, 300, 50)
        self.btn_medio = pygame.Rect(0, 0, 300, 50)
        self.btn_dificil = pygame.Rect(0, 0, 300, 50)
        self.btn_creditos = pygame.Rect(0, 0, 140, 40)

        # Controle de animação do plano de fundo
        self.fundo_frames = []
        self.frame_atual = 0
        self.ultimo_update = 0
        self.duracao_frame = 100

        caminho_gif = "assets/Sprites/fundo.gif"

        # Extrai os quadros do GIF animado utilizando a biblioteca Pillow
        if HAS_PIL == True and os.path.exists(caminho_gif):
            try:
                gif = Image.open(caminho_gif)
                duracao = gif.info.get("duration", 100)
                if duracao != None and duracao != 0:
                    self.duracao_frame = duracao

                for frame in ImageSequence.Iterator(gif):
                    rgba = frame.convert("RGBA")
                    img = pygame.image.fromstring(rgba.tobytes(), rgba.size, "RGBA").convert_alpha()
                    self.fundo_frames.append(img)
            except Exception:
                self.fundo_frames = []

    def atualizar_layout(self, largura_tela, altura_tela):
        """
        Recalcula as posições dos botões para manter o layout centralizado e responsivo.

        Parâmetros:
            largura_tela (int): Largura atual da janela.
            altura_tela (int): Altura atual da janela.
        """
        centro_x = largura_tela // 2
        centro_y = altura_tela // 2

        self.btn_facil.center = (centro_x, centro_y - 60)
        self.btn_medio.center = (centro_x, centro_y + 10)
        self.btn_dificil.center = (centro_x, centro_y + 80)
        # Posiciona o botão de créditos no canto inferior direito
        self.btn_creditos.bottomright = (largura_tela - 20, altura_tela - 20)

    def desenhar(self, tela, largura_tela, altura_tela):
        """
        Renderiza o fundo animado, o título e todos os botões do menu.

        Parâmetros:
            tela (pygame.Surface): Superfície de destino.
            largura_tela (int): Largura atual da janela.
            altura_tela (int): Altura atual da janela.
        """
        # Animação do GIF de fundo se disponível
        if len(self.fundo_frames) > 0:
            agora = pygame.time.get_ticks()

            if agora - self.ultimo_update > self.duracao_frame:
                self.frame_atual = (self.frame_atual + 1) % len(self.fundo_frames)
                self.ultimo_update = agora

            frame = pygame.transform.smoothscale(
                self.fundo_frames[self.frame_atual], (largura_tela, altura_tela)
            )
            tela.blit(frame, (0, 0))

        self.atualizar_layout(largura_tela, altura_tela)

        # Desenho do título principal
        texto_titulo = self.fonte_titulo.render("BrainFruit", True, BRANCO)
        tela.blit(texto_titulo, (largura_tela // 2 - texto_titulo.get_width() // 2, altura_tela // 2 - 180))

        # Textos e botões de dificuldade
        texto_facil = self.fonte_menu.render("Fácil (4x4)", True, BRANCO)
        tela.blit(texto_facil, texto_facil.get_rect(center=self.btn_facil.center))

        texto_medio = self.fonte_menu.render("Médio (6x6)", True, BRANCO)
        tela.blit(texto_medio, texto_medio.get_rect(center=self.btn_medio.center))

        texto_dificil = self.fonte_menu.render("Difícil (8x8)", True, BRANCO)
        tela.blit(texto_dificil, texto_dificil.get_rect(center=self.btn_dificil.center))

        pygame.draw.rect(tela, AZUL, self.btn_facil, 3, border_radius=10)
        pygame.draw.rect(tela, AZUL, self.btn_medio, 3, border_radius=10)
        pygame.draw.rect(tela, AZUL, self.btn_dificil, 3, border_radius=10)

        # Botão de Créditos no canto inferior direito
        pygame.draw.rect(tela, AZUL, self.btn_creditos, border_radius=10)
        pygame.draw.rect(tela, BRANCO, self.btn_creditos, 2, border_radius=10)
        texto_cred = self.fonte_pequena.render("Créditos", True, BRANCO)
        tela.blit(texto_cred, texto_cred.get_rect(center=self.btn_creditos.center))

    def verificar_clique(self, pos_mouse):
        """
        Identifica qual opção do menu foi clicada.

        Parâmetros:
            pos_mouse (tuple): Coordenadas (x, y) do cursor no momento do clique.

        Retorna:
            tuple: (nome_opcao, quantidade_de_pares) ou (None, None) se nada foi clicado.
        """
        if self.btn_facil.collidepoint(pos_mouse):
            return "FÁCIL (4x4)", 8
        elif self.btn_medio.collidepoint(pos_mouse):
            return "MÉDIO (6x6)", 18
        elif self.btn_dificil.collidepoint(pos_mouse):
            return "DIFÍCIL (8x8)", 32
        elif self.btn_creditos.collidepoint(pos_mouse):
            return "CREDITOS", None

        return None, None
