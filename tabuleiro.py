import pygame
import math
from config import *


class Tabuleiro:
    def __init__(self, cartas, largura_tela, altura_tela):
        self.cartas = cartas
        self.colunas = int(math.sqrt(len(cartas)))
        self.espacamento = 10

        self.imagens_originais = {}
        self.imagens_redimensionadas = {}

        nomes_frutas = []
        for carta in self.cartas:
            if carta["nome"] not in nomes_frutas:
                nomes_frutas.append(carta["nome"])

        # sem arquivo da fruta, guarda None e desenha o nome como texto
        for nome in nomes_frutas:
            caminho = f"assets/Sprites/Fruits/{nome}.png"
            try:
                self.imagens_originais[nome] = pygame.image.load(caminho).convert_alpha()
            except (FileNotFoundError, pygame.error):
                self.imagens_originais[nome] = None

        self.atualizar_layout(largura_tela, altura_tela)

    def atualizar_layout(self, largura_tela, altura_tela):
        espaco_topo = 90
        livre_y = altura_tela - espaco_topo - 20
        livre_x = largura_tela - 40

        max_x = (livre_x // self.colunas) - self.espacamento
        max_y = (livre_y // self.colunas) - self.espacamento

        base = min(max_x, max_y, 100)
        self.larg_carta = base
        self.alt_carta = base * 0.85

        tam_fonte = max(12, int(self.alt_carta * 0.35))
        self.fonte_carta = pygame.font.SysFont(None, tam_fonte)

        largura_img = max(1, int(self.larg_carta - 15))
        altura_img = max(1, int(self.alt_carta - 15))

        for nome, img in self.imagens_originais.items():
            if img != None:
                self.imagens_redimensionadas[nome] = pygame.transform.smoothscale(
                    img, (largura_img, altura_img)
                )
            else:
                self.imagens_redimensionadas[nome] = None

        largura_total = (self.colunas * self.larg_carta) + ((self.colunas - 1) * self.espacamento)
        altura_total = (self.colunas * self.alt_carta) + ((self.colunas - 1) * self.espacamento)

        self.margem_x = (largura_tela - largura_total) // 2
        self.margem_y = espaco_topo + (livre_y - altura_total) // 2

        i = 0
        for carta in self.cartas:
            linha = i // self.colunas
            col = i % self.colunas
            i += 1

            pos_x = self.margem_x + (col * (self.larg_carta + self.espacamento))
            pos_y = self.margem_y + (linha * (self.alt_carta + self.espacamento))

            carta["rect"] = pygame.Rect(pos_x, pos_y, self.larg_carta, self.alt_carta)

    def desenhar(self, tela):
        for carta in self.cartas:
            if carta["virada"] == True or carta["resolvida"] == True:
                pygame.draw.rect(tela, BRANCO, carta["rect"], border_radius=8)

                imagem = self.imagens_redimensionadas.get(carta["nome"])
                if imagem != None:
                    tela.blit(imagem, imagem.get_rect(center=carta["rect"].center))
                else:
                    texto = self.fonte_carta.render(carta["nome"], True, AZUL_ACO)
                    tela.blit(texto, texto.get_rect(center=carta["rect"].center))
            else:
                pygame.draw.rect(tela, AZUL, carta["rect"], border_radius=8)
                pygame.draw.rect(tela, BRANCO, carta["rect"], 2, border_radius=8)
