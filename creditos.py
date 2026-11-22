import pygame
from config import *


class Creditos:
    def __init__(self):
        self.fonte_titulo = pygame.font.SysFont(None, 54)
        self.fonte_texto = pygame.font.SysFont(None, 28)

        self.linhas_de_credito = [
            "Desenvolvimento e Programação:",
            "Manoel Roberto - Projeto BrainFruit (PBL)",
            "Disciplina: Algoritmos e Programação",
            "",
            "Orientação e Apoio Acadêmico:",
            "Coordenação do Projeto: Profa. Drª Claudia P. Pereira ",
            "Tutoria: Luana",
            "",
            "Agradecimentos Especiais:",
            "À minha esposa Camila, por todo o apoio e incentivo!",
            "",
            "Recursos Visuais e Sonoros (Assets Livres):",
            "Música: @wyver9 | SFX: Hungry Dino", #https://opengameart.org/content/good-mood-theme-8-bit | https://opengameart.org/content/hungry-dino-9-chiptune-tracks-10-sfx
            "Ícones: adrianadam | Frutas: Camila Freitas de Medeiros" #https://www.flaticon.com/authors/adrianadam
        ]

    def desenhar(self, tela, largura_tela, altura_tela):
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
