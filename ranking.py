import json
import os

ARQUIVO_RANKING = "ranking_brainfruit.json"


def carregar_ranking():
    if os.path.exists(ARQUIVO_RANKING) == False:
        return {
            "FÁCIL (4x4)": [],
            "MÉDIO (6x6)": [],
            "DIFÍCIL (8x8)": []
        }

    with open(ARQUIVO_RANKING, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_ranking(dados_ranking):
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as arquivo:
        json.dump(dados_ranking, arquivo, indent=4, ensure_ascii=False)


def merece_top5(dados_ranking, dificuldade, tempo_segundos):
    lista = dados_ranking.get(dificuldade, [])
    if len(lista) < 5:
        return True
    if tempo_segundos < lista[-1]["tempo"]:
        return True
    return False


def criterio_ordenacao(recorde):
    return (recorde["tempo"], recorde["tentativas"])


def adicionar_ao_ranking(dados_ranking, dificuldade, nome, tempo_segundos, tentativas):
    lista = dados_ranking.get(dificuldade, [])
    lista.append({"nome": nome, "tempo": tempo_segundos, "tentativas": tentativas})

    lista.sort(key=criterio_ordenacao)
    dados_ranking[dificuldade] = lista[:5]

    salvar_ranking(dados_ranking)
