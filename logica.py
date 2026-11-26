"""
Módulo de lógica do jogo BrainFruit.
Responsável pela lista de frutas disponíveis e geração do tabuleiro embaralhado.
"""

import random

# Banco de dados com os nomes das frutas disponíveis para os pares
todas_frutas = [
    "Maca", "Banana", "Laranja", "Uva", "Morango", "Abacaxi", "Manga", "Melancia",
    "Pera", "Kiwi", "Cereja", "Limao", "Pessego", "Ameixa", "Goiaba", "Mamao",
    "Coco", "Caju", "Amora", "Framboesa", "Mirtilo", "Melao", "Maracuja", "Tangerina",
    "Figo", "Roma", "Graviola", "Acerola", "Pitanga", "Seriguela", "Umbu", "Caja"
]


def gerar_tabuleiro(total_pares):
    """
    Sorteia as frutas e monta a estrutura de dados inicial de todas as cartas.

    Parâmetros:
        total_pares (int): Quantidade de pares necessários para a dificuldade
                           (ex: 8 para 4x4, 18 para 6x6, 32 para 8x8).

    Retorna:
        list: Lista de dicionários representando cada carta do tabuleiro com:
              - id: identificador único
              - nome: nome da fruta
              - virada: estado atual (True se estiver com a face visível)
              - resolvida: True se o par já foi encontrado e finalizado
              - rect: objeto pygame.Rect para detecção de colisão (definido no Tabuleiro)
    """
    # 1. Sorteia N frutas únicas da lista de opções
    frutas = random.sample(todas_frutas, total_pares)

    # 2. Duplica cada fruta para criar os pares e embaralha aleatoriamente
    pares = frutas + frutas
    random.shuffle(pares)

    # 3. Cria a lista de dicionários representando o estado individual de cada carta
    tabuleiro = []
    cont = 0
    for fruta in pares:
        carta = {
            "id": cont,
            "nome": fruta,
            "virada": False,
            "resolvida": False,
            "rect": None
        }
        tabuleiro.append(carta)
        cont += 1

    return tabuleiro
