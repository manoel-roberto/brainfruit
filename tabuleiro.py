"""
Módulo de renderização e posicionamento visual do tabuleiro de cartas.
Calcula dimensões dinâmicas das cartas e renderiza imagens ou nomes de frutas,
com suporte a efeito de hover nas cartas fechadas.
"""

import pygame
import math
from config import *


class Tabuleiro:
    """
    Gerencia a disposição visual, o dimensionamento responsivo das cartas e o desenho na tela.
    """

    def __init__(self, cartas, largura_tela, altura_tela):
        """
        Inicializa o tabuleiro calculando o número de colunas e pré-carregando imagens das frutas.

        Parâmetros:
            cartas (list): Lista de dicionários representando as cartas da partida.
            largura_tela (int): Largura atual da janela.
            altura_tela (int): Altura atual da janela.
        """
        self.cartas = cartas
        # Em grades quadradas (ex: 16 cartas -> 4 colunas; 36 cartas -> 6; 64 -> 8)
        self.colunas = int(math.sqrt(len(cartas)))
        self.espacamento = 10

        self.imagens_originais = {}
        self.imagens_redimensionadas = {}

        # Coleta a lista única de frutas presentes nesta partida
        nomes_frutas = []
        for carta in self.cartas:
            if carta["nome"] not in nomes_frutas:
                nomes_frutas.append(carta["nome"])

        # Pré-carrega as imagens das frutas; caso o arquivo não exista, armazena None
        # e renderiza o nome textual da fruta como fallback seguro
        for nome in nomes_frutas:
            caminho = f"assets/Sprites/Fruits/{nome}.png"
            try:
                self.imagens_originais[nome] = pygame.image.load(caminho).convert_alpha()
            except (FileNotFoundError, pygame.error):
                self.imagens_originais[nome] = None

        # Posiciona e dimensiona as cartas com base no tamanho inicial da janela
        self.atualizar_layout(largura_tela, altura_tela)

    def atualizar_layout(self, largura_tela, altura_tela):
        """
        Recalcula as dimensões e as coordenadas (Rect) de cada carta para se
        adaptar a redimensionamentos da janela ou alternância de tela cheia.

        Parâmetros:
            largura_tela (int): Nova largura da janela.
            altura_tela (int): Nova altura da janela.
        """
        espaco_topo = 90  # Espaço reservado para o HUD superior (tempo, desistir, tentativas)
        livre_y = altura_tela - espaco_topo - 20
        livre_x = largura_tela - 40

        # Calcula o tamanho máximo que cada carta pode ter para caber na grade
        max_x = (livre_x // self.colunas) - self.espacamento
        max_y = (livre_y // self.colunas) - self.espacamento

        base = min(max_x, max_y, 100)
        self.larg_carta = base
        self.alt_carta = base * 0.85

        # Ajusta proporcionalmente o tamanho da fonte para o texto de fallback
        tam_fonte = max(12, int(self.alt_carta * 0.35))
        self.fonte_carta = pygame.font.SysFont(None, tam_fonte)

        largura_img = max(1, int(self.larg_carta - 15))
        altura_img = max(1, int(self.alt_carta - 15))

        # Redimensiona suavemente as imagens para caberem nas cartas
        for nome, img in self.imagens_originais.items():
            if img != None:
                self.imagens_redimensionadas[nome] = pygame.transform.smoothscale(
                    img, (largura_img, altura_img)
                )
            else:
                self.imagens_redimensionadas[nome] = None

        largura_total = (self.colunas * self.larg_carta) + ((self.colunas - 1) * self.espacamento)
        altura_total = (self.colunas * self.alt_carta) + ((self.colunas - 1) * self.espacamento)

        # Centraliza o bloco do tabuleiro na área disponível
        self.margem_x = (largura_tela - largura_total) // 2
        self.margem_y = espaco_topo + (livre_y - altura_total) // 2

        # Atribui o retângulo de colisão (pygame.Rect) a cada carta
        i = 0
        for carta in self.cartas:
            linha = i // self.colunas
            col = i % self.colunas
            i += 1

            pos_x = self.margem_x + (col * (self.larg_carta + self.espacamento))
            pos_y = self.margem_y + (linha * (self.alt_carta + self.espacamento))

            carta["rect"] = pygame.Rect(pos_x, pos_y, self.larg_carta, self.alt_carta)

    def desenhar(self, tela):
        """
        Desenha todas as cartas na tela com base no seu estado (virada/resolvida ou oculta).
        Aplica efeito de hover em cartas disponíveis para clique.

        Parâmetros:
            tela (pygame.Surface): Superfície de destino onde as cartas serão desenhadas.

        Retorna:
            bool: True se o mouse estiver sobre alguma carta clicável (oculta e não resolvida).
        """
        pos_mouse = pygame.mouse.get_pos()
        hover_carta = False

        for carta in self.cartas:
            # Carta revelada (virada pelo jogador ou já resolvida)
            if carta["virada"] == True or carta["resolvida"] == True:
                pygame.draw.rect(tela, BRANCO, carta["rect"], border_radius=8)

                imagem = self.imagens_redimensionadas.get(carta["nome"])
                if imagem != None:
                    tela.blit(imagem, imagem.get_rect(center=carta["rect"].center))
                else:
                    texto = self.fonte_carta.render(carta["nome"], True, AZUL_ACO)
                    tela.blit(texto, texto.get_rect(center=carta["rect"].center))
            # Carta com o verso voltado para cima (disponível para clique)
            else:
                if carta["rect"].collidepoint(pos_mouse):
                    hover_carta = True
                    # Efeito de hover: azul mais claro e borda branca de destaque
                    pygame.draw.rect(tela, AZUL_HOVER, carta["rect"], border_radius=8)
                    pygame.draw.rect(tela, BRANCO, carta["rect"], 3, border_radius=8)
                else:
                    pygame.draw.rect(tela, AZUL, carta["rect"], border_radius=8)
                    pygame.draw.rect(tela, BRANCO, carta["rect"], 2, border_radius=8)

        return hover_carta
