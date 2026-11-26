"""
Módulo de exibição da tela de créditos do jogo BrainFruit.
Apresenta informações sobre a disciplina, autoria, tutoria, agradecimentos e atribuições de assets.
"""

import pygame
from config import *


class Creditos:
    """
    Renderiza um painel centralizado com os créditos e reconhecimentos do projeto.
    """

    def __init__(self):
        """
        Define as fontes e as linhas de texto exibidas no painel de créditos.
        """
        self.fonte_titulo = pygame.font.SysFont(None, 54)
        self.fonte_texto = pygame.font.SysFont(None, 28)

        self.linhas_de_credito = [
            "Desenvolvimento e Programação:",
            "Manoel Roberto - Projeto BrainFruit (PBL)",
            "Disciplina: Algoritmos e Programação",
            "",
            "Orientação e Apoio Acadêmico:",
            "Coordenação do Projeto: Profa. Drª Claudia P. Pereira",
            "Tutoria (Jedi Master): Luana (Turma Akiva)",
            "",
            "Agradecimentos Especiais:",
            "À minha esposa Camila Freitas de Medeiros,",
            "pelas artes das frutas e por todo apoio no curso noturno! ❤️",
            "",
            "Recursos Visuais e Sonoros (Assets Livres):",
            "Música: @wyver9 | SFX: Hungry Dino",
            "Ícones: adrianadam | Frutas: Camila Freitas de Medeiros"
        ]

    def desenhar(self, tela, largura_tela, altura_tela):
        """
        Desenha o painel azul e centraliza cada linha de texto dos créditos.

        Parâmetros:
            tela (pygame.Surface): Superfície de destino.
            largura_tela (int): Largura atual da janela.
            altura_tela (int): Altura atual da janela.
        """
        painel = pygame.Rect(largura_tela // 2 - 320, altura_tela // 2 - 270, 640, 540)
        pygame.draw.rect(tela, AZUL, painel, border_radius=15)
        pygame.draw.rect(tela, BRANCO, painel, 3, border_radius=15)

        titulo = self.fonte_titulo.render("CRÉDITOS", True, BRANCO)
        tela.blit(titulo, titulo.get_rect(center=(largura_tela // 2, altura_tela // 2 - 220)))

        y_linha = altura_tela // 2 - 150
        for linha in self.linhas_de_credito:
            txt = self.fonte_texto.render(linha, True, BRANCO)
            tela.blit(txt, txt.get_rect(center=(largura_tela // 2, y_linha)))
            y_linha += 28
