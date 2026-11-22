import random

todas_frutas = [
    "Maca", "Banana", "Laranja", "Uva", "Morango", "Abacaxi", "Manga", "Melancia",
    "Pera", "Kiwi", "Cereja", "Limao", "Pessego", "Ameixa", "Goiaba", "Mamao",
    "Coco", "Caju", "Amora", "Framboesa", "Mirtilo", "Melao", "Maracuja", "Tangerina",
    "Figo", "Roma", "Graviola", "Acerola", "Pitanga", "Seriguela", "Umbu", "Caja"
]


def gerar_tabuleiro(total_pares):
    frutas = random.sample(todas_frutas, total_pares)
    pares = frutas + frutas
    random.shuffle(pares)

    tabuleiro = []
    cont = 0
    for fruta in pares:
        carta = {"id": cont, "nome": fruta, "virada": False, "resolvida": False, "rect": None}
        tabuleiro.append(carta)
        cont += 1

    return tabuleiro
