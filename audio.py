"""
Módulo de áudio do jogo BrainFruit.
Controla a execução de músicas de fundo (BGM), efeitos sonoros (SFX) e recurso de mudo.
"""

import pygame


class GerenciadorAudio:
    """
    Gerencia o carregamento, reprodução contínua de trilhas sonoras e efeitos de áudio.
    """

    def __init__(self):
        """
        Inicializa o mixer do Pygame, volumes padrões e mapeamento dos arquivos de áudio.
        """
        pygame.mixer.init()

        self.mutado = False
        self.volume_sfx = 1.0
        self.volume_musica = 0.1
        self.musica_atual = None

        # Trilha sonora temática por tela/dificuldade
        self.trilhas = {
            "MENU": "assets/Audio/Music_0/Music/main_theme_01.wav",
            "CREDITOS": "assets/Audio/Music_0/Music/SubduedTheme.wav",
            "FÁCIL (4x4)": "assets/Audio/Music_0/Music/SwingingLevel.wav",
            "MÉDIO (6x6)": "assets/Audio/Music_0/Music/FranticLevel.wav",
            "DIFÍCIL (8x8)": "assets/Audio/Music_0/Music/8BitMetal.wav",
            "NOVO_RECORDE": "assets/Audio/Music_0/Music/MainTheme.wav",
            "DERROTA": "assets/Audio/Music_0/Music/SeriousCutScene.wav"
        }

        # Efeitos sonoros das ações do jogador
        caminhos_sfx = {
            "virar_carta": "assets/Audio/SFX_1/SFX/beep.wav",
            "acerto": "assets/Audio/SFX_1/SFX/confirmbeep.wav",
            "erro": "assets/Audio/SFX_1/SFX/oops.wav"
        }

        self.efeitos = {}
        for nome, caminho in caminhos_sfx.items():
            try:
                som = pygame.mixer.Sound(caminho)
                som.set_volume(self.volume_sfx)
                self.efeitos[nome] = som
            except (FileNotFoundError, pygame.error):
                self.efeitos[nome] = None

    def tocar_musica(self, estado, dificuldade=None):
        """
        Inicia a reprodução em loop da música apropriada para o estado do jogo ou dificuldade.

        Parâmetros:
            estado (str): Estado atual do jogo (ex: 'MENU', 'JOGANDO', 'CREDITOS').
            dificuldade (str, opcional): Dificuldade selecionada quando o estado for 'JOGANDO'.
        """
        if estado == "JOGANDO":
            chave = dificuldade
        else:
            chave = estado

        # Evita reiniciar a mesma música caso ela já esteja em execução
        if self.musica_atual == chave:
            return

        caminho = self.trilhas.get(chave)
        if caminho != None:
            try:
                pygame.mixer.music.load(caminho)
                if self.mutado == True:
                    pygame.mixer.music.set_volume(0.0)
                else:
                    pygame.mixer.music.set_volume(self.volume_musica)
                pygame.mixer.music.play(-1)  # -1 = reprodução contínua em loop
                self.musica_atual = chave
            except (FileNotFoundError, pygame.error):
                pass

    def tocar_sfx(self, nome_efeito):
        """
        Reproduz um efeito sonoro instantâneo, respeitando o estado de mudo.

        Parâmetros:
            nome_efeito (str): Identificador do efeito (ex: 'virar_carta', 'acerto', 'erro').
        """
        som = self.efeitos.get(nome_efeito)
        if self.mutado == False and som != None:
            som.play()

    def alternar_mute(self):
        """
        Alterna entre o modo mudo (silenciado) e áudio ativo.

        Retorna:
            bool: Novo estado de `self.mutado`.
        """
        if self.mutado == True:
            self.mutado = False
        else:
            self.mutado = True

        if self.mutado == True:
            vol_musica = 0.0
            vol_sfx = 0.0
        else:
            vol_musica = self.volume_musica
            vol_sfx = self.volume_sfx

        pygame.mixer.music.set_volume(vol_musica)
        for som in self.efeitos.values():
            if som != None:
                som.set_volume(vol_sfx)

        return self.mutado
