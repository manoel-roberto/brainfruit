# 🍎 BrainFruit - Jogo da Memória

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/pygame-2.5+-green.svg)](https://www.pygame.org/)
[![UEFS](https://img.shields.io/badge/UEFS-Extens%C3%A3o-red.svg)](https://www.uefs.br/)
[![Jedi Temple](https://img.shields.io/badge/PBL-Jedi%20Temple-yellow.svg)](https://sites.google.com/view/jeditemple/)

**BrainFruit** é um jogo da memória temático de frutas desenvolvido em Python utilizando a biblioteca **Pygame**. 

O projeto foi concebido e construído como trabalho final prático da disciplina de **Algoritmos e Programação em Python**, no formato **PBL (Aprendizado Baseado em Problemas)**, integrando o programa de extensão **JEDI TEMPLE** da **Universidade Estadual de Feira de Santana (UEFS)**.

---

## 🎮 O Jogo

BrainFruit exercita a memória visual e a agilidade do jogador em um ambiente descontraído e nostálgico em estilo *pixel art* / *chiptune*, com animações, efeitos sonoros dinâmicos, ranking local de recordes e trilha sonora retrô.

### 🕹️ Regras e Dificuldades

1. Escolha a dificuldade desejada no menu inicial.
2. Clique em duas cartas para revelá-las.
3. Se formarem um par idêntico, as cartas permanecem abertas.
4. Se forem frutas diferentes, as cartas desviram após um intervalo de 1 segundo.
5. O objetivo é encontrar todos os pares no menor tempo e com o menor número de tentativas.
6. Ao vencer, se o seu desempenho entrar para o **Top 5** daquela dificuldade, você poderá registrar seu nome no ranking de recordes!

| Dificuldade | Dimensão do Tabuleiro | Quantidade de Cartas | Total de Pares |
|:-----------:|:---------------------:|:-------------------:|:--------------:|
| **Fácil**   | 4x4                   | 16                  | 8 pares        |
| **Médio**   | 6x6                   | 36                  | 18 pares       |
| **Difícil** | 8x8                   | 64                  | 32 pares       |

---

## ⌨️ Controles e Interface

- **Mouse (Botão Esquerdo)**: Interage com as cartas, botões de menu e controles da tela.
- **Botão de Som (Canto inferior esquerdo)**: Alterna entre ativar/desativar áudio (Mute/Unmute).
- **Botão de Créditos (Canto inferior direito do menu)**: Abre o painel com os créditos e homenagens do projeto.
- **F11**: Alterna entre tela cheia (*fullscreen*) e modo janela redimensionável.
- **Botão Desistir**: Permite interromper a partida em andamento e retornar ao menu principal.

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- **Python 3.10** ou superior instalado.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/manoel-roberto/brainfruit.git
   cd brainfruit
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # No Linux / macOS:
   python3 -m venv .venv
   source .venv/bin/activate

   # No Windows:
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o jogo:**
   ```bash
   python main.py
   ```

> **Nota:** As dependências principais são `pygame` (motor gráfico e de áudio) e `pillow` (leitura e animação dos quadros do GIF de fundo do menu).

---

## 📁 Estrutura de Arquivos

| Arquivo / Diretório | Função |
|---|---|
| `main.py` | Loop principal, máquina de estados do jogo (Menu, Partida, Vitória, Créditos) e despacho de eventos |
| `menu.py` | Renderização do menu principal, layout responsivo, fundo animado em GIF e navegação |
| `tabuleiro.py` | Posicionamento responsivo das cartas, cálculo de grid e renderização |
| `logica.py` | Sorteio aleatório de pares de frutas e regras de validação das jogadas |
| `ranking.py` | Gerenciamento e persistência do Top 5 em arquivo JSON (`ranking_brainfruit.json`) |
| `audio.py` | Controlador de música de fundo, efeitos sonoros (SFX) e alternância de mudo |
| `creditos.py` | Tela dedicada de créditos, reconhecimentos e referências |
| `config.py` | Constantes de configuração global (resolução, FPS, paleta de cores) |
| `assets/` | Imagens e sprites (`Sprites/`, `Sprites/Fruits/`) e efeitos/trilhas sonoras (`Audio/`) |

---

## 🎓 Contexto Acadêmico: O Projeto JEDI TEMPLE

Este jogo foi desenvolvido no âmbito das atividades acadêmicas e de extensão da **Universidade Estadual de Feira de Santana (UEFS)**.

### O Curso
- **Curso:** Algoritmos e Programação em Python
- **Formato:** Extensão Universitária, com carga horária de **180 horas** (120 h síncronas + 60 h assíncronas), certificado emitido pela **Pró-Reitoria de Extensão da UEFS**.
- **Metodologias:**
  - **Aprendizagem Ativa e Sala de Aula Invertida (*Flipped Classroom*):** Os estudantes assistem a videoaulas assíncronas preparatórias (gravadas pelo Prof. Dr. Roberto Bittencourt no YouTube) antes dos encontros síncronos práticos.
  - **PBL (*Problem-Based Learning* / Aprendizado Baseado em Problemas):** Ensino orientado à resolução de desafios reais de programação, culminando na arquitetura e implementação completa de um jogo digital com Pygame.
- **Ambientes Utilizados:** Plataforma **Discord** para encontros virtuais síncronos e mentoria, **YouTube** para as aulas assíncronas e **Replit** para exercícios e práticas de codificação.

O projeto visa mitigar a carência de formação tecnológica nas escolas públicas do interior da Bahia, despertando vocações precoces para a área de Tecnologia da Informação, fortalecendo o **Pensamento Computacional** e reduzindo a evasão nos cursos superiores de Computação.

Inspirado no universo **Star Wars**, o projeto organiza sua estrutura de tutoria em uma hierarquia lúdica:
- **Yodas:** Coordenadores docentes e discentes veteranos responsáveis pela orientação pedagógica e gestão geral dos cursos.
- **Jedi Masters:** Estudantes do curso de Engenharia de Computação da UEFS que atuam como mentores/monitores diretos das turmas, guiando os encontros síncronos, tirando dúvidas e avaliando as atividades práticas.
- **Padawans:** Os aprendizes participantes dos cursos.

#### Equipe de Coordenação (Yodas 2026):
- **Profª Drª Pâmela M. Candida Cortez** – Coordenadora Geral do Projeto
- **Caio Bruno de Oliveira Matos** – Curso de Lógica de Programação
- **Paulo Henrique Dantas Barreto** – Curso de Algoritmos e Programação
- **Douglas Oliveira de Jesus** – Curso de Desenvolvimento Mobile

Para mais detalhes e inscrições:
- 🌐 [Site Oficial do Jedi Temple](https://sites.google.com/view/jeditemple/)
- 📸 [Instagram Engenharia de Computação UEFS (@ecompuefs)](https://www.instagram.com/ecompuefs/)

---

## 🌟 Créditos e Agradecimentos

### Desenvolvimento e Coordenação
- **Desenvolvimento e Programação:** Manoel Roberto
- **Coordenação e Orientação:** Profª Drª Pâmela M. Candida Cortez
- **Tutoria / Mentoria (Jedi Master):** **Luana**, com agradecimento especial por ter guiado com dedicação, carinho e imensa paciência a nossa **Turma Akiva** nos encontros de terças e quintas-feiras!
- **Videoaulas e Conteúdo:** Prof. Dr. Roberto Bittencourt

### Agradecimento Especial
> Um agradecimento muito especial à minha amada esposa, **Camila Freitas de Medeiros**, que desenhou com muito carinho as artes das frutas utilizadas no jogo e que sempre me apoiou e incentivou durante todas as noites de estudo e dedicação a este curso! ❤️

### Recursos Livres Utilizados (Assets & Áudio)
- **Música:** [*Good Mood Theme (8-bit)* por @wyver9](https://opengameart.org/content/good-mood-theme-8-bit) (OpenGameArt)
- **Efeitos Sonoros (SFX):** [*Hungry Dino - 9 Chiptune Tracks & 10 SFX*](https://opengameart.org/content/hungry-dino-9-chiptune-tracks-10-sfx) (OpenGameArt)
- **Ícones de Interface (Áudio / Mute):** Criados por [adrianadam](https://www.flaticon.com/authors/adrianadam) no Flaticon:
  - [Ícone de Volume](https://www.flaticon.com/free-icon/volume_16701461)
  - [Ícone de Mudo](https://www.flaticon.com/free-icon/mute_5381637)
- **Frutas (Pixel Art):** Camila Freitas de Medeiros
