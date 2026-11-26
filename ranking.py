"""
Módulo de persistência e gerenciamento do ranking local de recordes.
Salva e recupera o Top 5 de cada nível de dificuldade em formato JSON.
"""

import json
import os

# Nome do arquivo local de persistência do ranking
ARQUIVO_RANKING = "ranking_brainfruit.json"


def carregar_ranking():
    """
    Carrega os recordes salvos do arquivo JSON.
    Se o arquivo ainda não existir, inicializa e retorna a estrutura vazia.

    Retorna:
        dict: Dicionário contendo uma lista de recordes por nível de dificuldade.
    """
    if os.path.exists(ARQUIVO_RANKING) == False:
        return {
            "FÁCIL (4x4)": [],
            "MÉDIO (6x6)": [],
            "DIFÍCIL (8x8)": []
        }

    with open(ARQUIVO_RANKING, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_ranking(dados_ranking):
    """
    Escreve a estrutura atualizada de recordes no arquivo JSON.

    Parâmetros:
        dados_ranking (dict): Dicionário com os recordes por dificuldade.
    """
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as arquivo:
        json.dump(dados_ranking, arquivo, indent=4, ensure_ascii=False)


def merece_top5(dados_ranking, dificuldade, tempo_segundos):
    """
    Verifica se o tempo alcançado pelo jogador qualifica para o Top 5 da dificuldade.

    Parâmetros:
        dados_ranking (dict): Dicionário de rankings atuais.
        dificuldade (str): Nome da dificuldade jogada (ex: 'FÁCIL (4x4)').
        tempo_segundos (int): Tempo total gasto pelo jogador para completar o jogo.

    Retorna:
        bool: True se houver menos de 5 registros ou se o tempo for menor que o último colocado.
    """
    lista = dados_ranking.get(dificuldade, [])
    # Se ainda houver vagas disponíveis no Top 5
    if len(lista) < 5:
        return True
    # Se bateu o tempo do 5º colocado
    if tempo_segundos < lista[-1]["tempo"]:
        return True
    return False


def criterio_ordenacao(recorde):
    """
    Função auxiliar de ordenação: prioriza menor tempo, seguido de menor número de tentativas.
    """
    return (recorde["tempo"], recorde["tentativas"])


def adicionar_ao_ranking(dados_ranking, dificuldade, nome, tempo_segundos, tentativas):
    """
    Insere o novo recorde no ranking da dificuldade, ordena e mantém apenas os 5 melhores.

    Parâmetros:
        dados_ranking (dict): Dicionário de rankings.
        dificuldade (str): Nome da dificuldade.
        nome (str): Nome ou apelido informado pelo jogador.
        tempo_segundos (int): Tempo em segundos.
        tentativas (int): Total de tentativas realizadas.
    """
    lista = dados_ranking.get(dificuldade, [])
    lista.append({"nome": nome, "tempo": tempo_segundos, "tentativas": tentativas})

    # Ordena pelo menor tempo e menor número de tentativas
    lista.sort(key=criterio_ordenacao)

    # Mantém apenas os 5 melhores
    dados_ranking[dificuldade] = lista[:5]

    salvar_ranking(dados_ranking)
