# 🍎 BrainFruit - Jogo da Memória

Jogo da memória com frutas feito em Python com Pygame. Projeto da disciplina de **Algoritmos e Programação**, no formato PBL (Aprendizado Baseado em Problemas) do curso do [JEDI TEMPLE](https://sites.google.com/view/jeditemple/algoritmos-e-programação).

## Como jogar

1. Escolha a dificuldade no menu.
2. Clique em duas cartas para virar.
3. Se forem a mesma fruta, o par fica aberto. Se não forem, as cartas desviram depois de 1 segundo.
4. Ache todos os pares no menor tempo e com menos tentativas.
5. Se entrar no Top 5 da dificuldade, digite seu nome e aperte **ENTER**.

| Dificuldade | Tabuleiro | Pares |
|-------------|-----------|-------|
| Fácil       | 4x4       | 8     |
| Médio       | 6x6       | 18    |
| Difícil     | 8x8       | 32    |

### Controles

- **Mouse**: clicar nas cartas, botões e no ícone de som (canto inferior esquerdo)
- **F11**: alterna tela cheia
- **Desistir**: volta ao menu durante a partida
- A janela pode ser redimensionada

## Como rodar

Precisa de Python 3.10 ou mais novo.

```bash
python -m venv .venv
source .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Dependências: `pygame` (jogo) e `pillow` (para animar o GIF de fundo do menu).

## Estrutura do projeto

| Arquivo | O que faz |
|---------|-----------|
| `main.py` | Loop principal, estados do jogo e eventos |
| `menu.py` | Menu inicial com fundo animado e botões |
| `tabuleiro.py` | Desenha e posiciona as cartas na tela |
| `logica.py` | Sorteia as frutas e monta o tabuleiro |
| `ranking.py` | Lê e salva o Top 5 em `ranking_brainfruit.json` |
| `audio.py` | Músicas, efeitos sonoros e mute |
| `creditos.py` | Tela de créditos |
| `config.py` | Tamanho da tela, FPS e cores |
| `assets/` | Imagens (`Sprites/`, `Sprites/Fruits/`) e áudio (`Audio/`) |

Se a imagem de uma fruta não for encontrada, o jogo mostra o nome dela escrito na carta.

## Créditos

- **Desenvolvimento**: Manoel Roberto
- **Coordenação do projeto**: Profa. Drª Claudia P. Pereira
- **Tutoria**: Luana
- **Música**: [@wyver9](https://opengameart.org/content/good-mood-theme-8-bit)
- **Efeitos sonoros**: [Hungry Dino](https://opengameart.org/content/hungry-dino-9-chiptune-tracks-10-sfx)
- **Ícones**: [adrianadam](https://www.flaticon.com/authors/adrianadam)
- **Frutas**: Camila Freitas de Medeiros

Agradecimento especial à minha esposa Camila, pelo apoio e incentivo!
