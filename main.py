"""
Módulo principal do jogo BrainFruit (Jogo da Memória).
Gerencia o loop principal, máquina de estados do jogo, processamento de eventos,
temporizador de jogadas, ranking de recordes e alternância de telas.
"""

import pygame
import sys
from config import *
from menu import Menu
from logica import gerar_tabuleiro
from tabuleiro import Tabuleiro
from ranking import carregar_ranking, merece_top5, adicionar_ao_ranking
from creditos import Creditos
from audio import GerenciadorAudio


def todas_resolvidas(cartas):
    """
    Verifica se todas as cartas do tabuleiro já foram combinadas em pares corretos.

    Parâmetros:
        cartas (list): Lista de dicionários representando as cartas da partida.

    Retorna:
        bool: True se todos os pares foram encontrados, False caso reste alguma carta não resolvida.
    """
    for carta in cartas:
        if carta["resolvida"] == False:
            return False
    return True


# ==========================================
# Inicialização da Janela e Recursos Gráficos
# ==========================================
pygame.init()

largura_atual = LARGURA
altura_atual = ALTURA
tela_cheia = False

TELA = pygame.display.set_mode((largura_atual, altura_atual), pygame.RESIZABLE)
pygame.display.set_caption("BrainFruit - Jogo da Memória (Aperte F11 para Tela Cheia)")
relogio = pygame.time.Clock()

menu_principal = Menu()
tela_creditos = Creditos()
gerenciador_audio = GerenciadorAudio()

# ==========================================
# Variáveis de Estado do Jogo
# ==========================================
# Estados possíveis: "MENU", "CREDITOS", "JOGANDO", "ESPERANDO", "NOVO_RECORDE", "VITORIA"
estado = "MENU"
dificuldade = None
dados_cartas = []
tabuleiro_visual = None
cartas_ativas = []      # Armazena as cartas viradas na jogada atual (máximo 2)
tempo_erro = 0          # Marca o timestamp em que um par incorreto foi virado

fonte_hud = pygame.font.SysFont(None, 36)
fonte_titulo = pygame.font.SysFont(None, 54)

tentativas = 0
tempo_inicio = 0
segundos = 0

dados_ranking = carregar_ranking()
nome_digitado = ""

# Carrega os ícones visuais do botão de som com fallback seguro
try:
    img_volume = pygame.image.load("assets/Sprites/volume.png").convert_alpha()
    img_mute = pygame.image.load("assets/Sprites/mute.png").convert_alpha()
    img_volume = pygame.transform.smoothscale(img_volume, (32, 32))
    img_mute = pygame.transform.smoothscale(img_mute, (32, 32))
except (FileNotFoundError, pygame.error):
    img_volume = pygame.Surface((32, 32))
    img_volume.fill((100, 255, 100))
    img_mute = pygame.Surface((32, 32))
    img_mute.fill((255, 100, 100))

# Inicia a música de fundo do menu
gerenciador_audio.tocar_musica("MENU")


def iniciar_partida(pares=None, nova_dificuldade=None):
    """
    Inicializa ou reinicia uma partida de jogo, redefinindo contadores e gerando um novo tabuleiro.

    Parâmetros:
        pares (int, opcional): Quantidade de pares de cartas. Se omitido, usa a quantidade da partida anterior.
        nova_dificuldade (str, opcional): Nome da dificuldade escolhida. Se omitido, mantém a atual.
    """
    global dificuldade, dados_cartas, tabuleiro_visual
    global tentativas, segundos, tempo_inicio, estado

    if nova_dificuldade is not None:
        dificuldade = nova_dificuldade

    if pares is None:
        pares = len(dados_cartas) // 2

    dados_cartas = gerar_tabuleiro(pares)
    tabuleiro_visual = Tabuleiro(dados_cartas, largura_atual, altura_atual)
    cartas_ativas.clear()
    tentativas = 0
    segundos = 0
    tempo_inicio = pygame.time.get_ticks()
    estado = "JOGANDO"
    gerenciador_audio.tocar_musica("JOGANDO", dificuldade)


# ==========================================
# Loop Principal do Jogo
# ==========================================
rodando = True
while rodando:
    relogio.tick(FPS)

    # Coordenadas responsivas dos botões de interface
    btn_desistir = pygame.Rect(largura_atual // 2 - 70, 15, 140, 40)
    btn_reiniciar = pygame.Rect(largura_atual // 2 - 230, altura_atual // 2 + 160, 210, 50)
    btn_menu = pygame.Rect(largura_atual // 2 + 20, altura_atual // 2 + 160, 210, 50)
    btn_som = pygame.Rect(20, altura_atual - 52, 32, 32)

    # ----------------------------------------------------
    # 1. Tratamento de Eventos (Teclado, Mouse e Janela)
    # ----------------------------------------------------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # Redimensionamento manual da janela
        if evento.type == pygame.VIDEORESIZE:
            if tela_cheia == False:
                largura_atual, altura_atual = evento.w, evento.h
                TELA = pygame.display.set_mode((largura_atual, altura_atual), pygame.RESIZABLE)
                if tabuleiro_visual != None:
                    tabuleiro_visual.atualizar_layout(largura_atual, altura_atual)

        # Eventos de teclado
        if evento.type == pygame.KEYDOWN:
            # F11: Alternar tela cheia (Fullscreen)
            if evento.key == pygame.K_F11:
                if tela_cheia == True:
                    tela_cheia = False
                else:
                    tela_cheia = True
                if tela_cheia == True:
                    info = pygame.display.Info()
                    largura_atual, altura_atual = info.current_w, info.current_h
                    TELA = pygame.display.set_mode((largura_atual, altura_atual), pygame.FULLSCREEN)
                else:
                    largura_atual, altura_atual = LARGURA, ALTURA
                    TELA = pygame.display.set_mode((largura_atual, altura_atual), pygame.RESIZABLE)

                if tabuleiro_visual != None:
                    tabuleiro_visual.atualizar_layout(largura_atual, altura_atual)

            # Digitação do nome na tela de novo recorde
            if estado == "NOVO_RECORDE":
                if evento.key == pygame.K_RETURN:
                    if nome_digitado.strip() == "":
                        nome_digitado = "Anônimo"

                    adicionar_ao_ranking(dados_ranking, dificuldade, nome_digitado, segundos, tentativas)
                    nome_digitado = ""
                    estado = "VITORIA"

                elif evento.key == pygame.K_BACKSPACE:
                    nome_digitado = nome_digitado[:-1]
                else:
                    # Limita o nome a no máximo 12 caracteres
                    if len(nome_digitado) < 12:
                        nome_digitado += evento.unicode

        # Eventos de clique do mouse (apenas botão esquerdo: button == 1)
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Alterna áudio (Mute/Unmute)
            if btn_som.collidepoint(evento.pos):
                gerenciador_audio.alternar_mute()
                continue

            # Cliques no Menu Principal
            if estado == "MENU":
                dif_escolhida, pares = menu_principal.verificar_clique(evento.pos)
                if dif_escolhida == "CREDITOS":
                    estado = "CREDITOS"
                    gerenciador_audio.tocar_musica("CREDITOS")
                elif dif_escolhida != None:
                    iniciar_partida(pares, dif_escolhida)

            # Cliques na Tela de Créditos (qualquer clique retorna ao menu)
            elif estado == "CREDITOS":
                estado = "MENU"
                gerenciador_audio.tocar_musica("MENU")

            # Cliques durante a Partida (Jogando ou aguardando par incorreto)
            elif estado in ["JOGANDO", "ESPERANDO"]:
                # Botão de desistência
                if btn_desistir.collidepoint(evento.pos):
                    estado = "MENU"
                    cartas_ativas.clear()
                    gerenciador_audio.tocar_musica("MENU")
                    continue

                # Clique nas cartas do tabuleiro
                if estado == "JOGANDO":
                    for carta in dados_cartas:
                        if carta["rect"].collidepoint(evento.pos):
                            if carta["virada"] == False and carta["resolvida"] == False and len(cartas_ativas) < 2:
                                carta["virada"] = True
                                cartas_ativas.append(carta)
                                gerenciador_audio.tocar_sfx("virar_carta")

            # Cliques na Tela de Vitória
            elif estado == "VITORIA":
                if btn_reiniciar.collidepoint(evento.pos):
                    iniciar_partida()
                elif btn_menu.collidepoint(evento.pos):
                    estado = "MENU"
                    gerenciador_audio.tocar_musica("MENU")

    # ----------------------------------------------------
    # 2. Lógica do Jogo (Validação de Pares e Vitória)
    # ----------------------------------------------------
    if estado == "JOGANDO" and len(cartas_ativas) == 2:
        tentativas += 1

        # Acerto: as duas cartas viradas têm a mesma fruta
        if cartas_ativas[0]["nome"] == cartas_ativas[1]["nome"]:
            cartas_ativas[0]["resolvida"] = True
            cartas_ativas[1]["resolvida"] = True
            cartas_ativas.clear()
            gerenciador_audio.tocar_sfx("acerto")

            # Verifica se todas as cartas foram encontradas (fim de jogo)
            if todas_resolvidas(dados_cartas):
                segundos = (pygame.time.get_ticks() - tempo_inicio) // 1000
                if merece_top5(dados_ranking, dificuldade, segundos):
                    nome_digitado = ""
                    estado = "NOVO_RECORDE"
                    gerenciador_audio.tocar_musica("NOVO_RECORDE")
                else:
                    estado = "VITORIA"
                    gerenciador_audio.tocar_musica("NOVO_RECORDE")
        # Erro: frutas diferentes, entra em estado de espera antes de desvirar
        else:
            gerenciador_audio.tocar_sfx("erro")
            tempo_erro = pygame.time.get_ticks()
            estado = "ESPERANDO"

    # Aguarda 1 segundo exibindo o par incorreto antes de desvirar as cartas
    if estado == "ESPERANDO":
        if pygame.time.get_ticks() - tempo_erro > 1000:
            cartas_ativas[0]["virada"] = False
            cartas_ativas[1]["virada"] = False
            cartas_ativas.clear()
            estado = "JOGANDO"

    # ----------------------------------------------------
    # 3. Renderização Gráfica por Estado
    # ----------------------------------------------------
    TELA.fill(AZUL_ACO)

    if estado == "MENU":
        menu_principal.desenhar(TELA, largura_atual, altura_atual)

    elif estado == "CREDITOS":
        tela_creditos.desenhar(TELA, largura_atual, altura_atual)
        aviso = fonte_hud.render("Clique em qualquer lugar para voltar", True, BRANCO)
        TELA.blit(aviso, aviso.get_rect(center=(largura_atual // 2, altura_atual - 30)))

    elif estado in ["JOGANDO", "ESPERANDO"]:
        tabuleiro_visual.desenhar(TELA)

        segundos = (pygame.time.get_ticks() - tempo_inicio) // 1000

        texto_tempo = fonte_hud.render(f"Tempo: {segundos}s", True, BRANCO)
        texto_tentativas = fonte_hud.render(f"Tentativas: {tentativas}", True, BRANCO)
        TELA.blit(texto_tempo, (20, 20))
        TELA.blit(texto_tentativas, (largura_atual - texto_tentativas.get_width() - 20, 20))

        # Botão Desistir
        pygame.draw.rect(TELA, AZUL, btn_desistir, border_radius=10)
        pygame.draw.rect(TELA, BRANCO, btn_desistir, 2, border_radius=10)
        texto_btn = fonte_hud.render("Desistir", True, BRANCO)
        TELA.blit(texto_btn, texto_btn.get_rect(center=btn_desistir.center))

    elif estado == "NOVO_RECORDE":
        tabuleiro_visual.desenhar(TELA)

        painel = pygame.Rect(largura_atual // 2 - 260, altura_atual // 2 - 140, 520, 280)
        pygame.draw.rect(TELA, AZUL, painel, border_radius=15)
        pygame.draw.rect(TELA, BRANCO, painel, 3, border_radius=15)

        txt_rec = fonte_titulo.render("NOVO RECORDE!", True, BRANCO)
        TELA.blit(txt_rec, txt_rec.get_rect(center=(largura_atual // 2, altura_atual // 2 - 90)))

        txt_info = fonte_hud.render(f"Tempo: {segundos}s | Tentativas: {tentativas}", True, BRANCO)
        TELA.blit(txt_info, txt_info.get_rect(center=(largura_atual // 2, altura_atual // 2 - 35)))

        txt_pedir = fonte_hud.render("Digite seu nome e aperte ENTER:", True, BRANCO)
        TELA.blit(txt_pedir, txt_pedir.get_rect(center=(largura_atual // 2, altura_atual // 2 + 15)))

        caixa_texto = pygame.Rect(largura_atual // 2 - 150, altura_atual // 2 + 45, 300, 45)
        pygame.draw.rect(TELA, BRANCO, caixa_texto, border_radius=8)
        txt_nome = fonte_hud.render(nome_digitado + "|", True, AZUL_ACO)
        TELA.blit(txt_nome, txt_nome.get_rect(center=caixa_texto.center))

    elif estado == "VITORIA":
        tabuleiro_visual.desenhar(TELA)

        painel = pygame.Rect(largura_atual // 2 - 260, altura_atual // 2 - 220, 520, 450)
        pygame.draw.rect(TELA, AZUL, painel, border_radius=15)
        pygame.draw.rect(TELA, BRANCO, painel, 3, border_radius=15)

        texto_vitoria = fonte_titulo.render("VOCÊ VENCEU!", True, BRANCO)
        TELA.blit(texto_vitoria, texto_vitoria.get_rect(center=(largura_atual // 2, altura_atual // 2 - 175)))

        texto_fim = fonte_hud.render(f"Tempo: {segundos}s | Tentativas: {tentativas}", True, BRANCO)
        TELA.blit(texto_fim, texto_fim.get_rect(center=(largura_atual // 2, altura_atual // 2 - 125)))

        titulo_rank = fonte_hud.render(f"Top 5 - {dificuldade}", True, BRANCO)
        TELA.blit(titulo_rank, titulo_rank.get_rect(center=(largura_atual // 2, altura_atual // 2 - 75)))

        top5 = dados_ranking.get(dificuldade, [])
        idx = 0
        for item in top5:
            linha = f"{idx + 1}. {item['nome']} - {item['tempo']}s ({item['tentativas']} tent.)"
            surf = fonte_hud.render(linha, True, BRANCO)
            TELA.blit(surf, surf.get_rect(center=(largura_atual // 2, altura_atual // 2 - 30 + idx * 34)))
            idx += 1

        # Botão Reiniciar
        pygame.draw.rect(TELA, AZUL_ACO, btn_reiniciar, border_radius=10)
        pygame.draw.rect(TELA, BRANCO, btn_reiniciar, 2, border_radius=10)
        texto_reiniciar = fonte_hud.render("Reiniciar", True, BRANCO)
        TELA.blit(texto_reiniciar, texto_reiniciar.get_rect(center=btn_reiniciar.center))

        # Botão Voltar ao Menu
        pygame.draw.rect(TELA, AZUL_ACO, btn_menu, border_radius=10)
        pygame.draw.rect(TELA, BRANCO, btn_menu, 2, border_radius=10)
        texto_voltar = fonte_hud.render("Voltar ao Menu", True, BRANCO)
        TELA.blit(texto_voltar, texto_voltar.get_rect(center=btn_menu.center))

    # Desenha o ícone de áudio no canto inferior esquerdo
    if gerenciador_audio.mutado == True:
        TELA.blit(img_mute, btn_som)
    else:
        TELA.blit(img_volume, btn_som)

    pygame.display.flip()

# Encerramento gracioso do jogo
pygame.quit()
sys.exit()
