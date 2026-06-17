# Jogo de Damas — Interface Visual com KivyMD

Projeto Final de Programação Orientada a Objetos — Fase 2 (Interface Visual).
Implementação do jogo de Damas com interface gráfica em KivyMD, construída sobre a
lógica de jogo desenvolvida na Fase 1 (terminal).

## Integrantes

|---|---|
| [Isaac Leonardo da Silva] | [2840482421016] |

## Descrição do Jogo

Damas é um jogo de tabuleiro 8×8 para dois jogadores. Cada jogador começa com 12 peças
posicionadas nas casas escuras das três primeiras linhas do seu lado. As peças se movem
na diagonal, capturam saltando sobre peças adversárias (captura obrigatória quando
disponível) e são promovidas a "dama" ao atingir a última linha do tabuleiro, podendo
então se mover em todas as direções diagonais.

## Ferramentas de Inteligência Artificial Utilizadas

Em conformidade com a seção 13 do enunciado do projeto, declaramos abaixo o uso de IA:

| Ferramenta | Finalidade |
|---|---|
| Claude (Anthropic) | Apoio na estruturação da arquitetura MVC, geração de trechos de código das telas KivyMD (menu, configuração, tabuleiro, tema), revisão de bugs de layout (posicionamento de widgets, cores), e organização da documentação (README, diagrama UML). |

## Arquitetura

O projeto segue o padrão **MVC (Model–View–Controller)**, isolando completamente a
lógica do jogo da interface gráfica.

```
poo-jogo-damas/
├── main.py                          # Ponto de entrada (MDApp + ScreenManager)
├── requirements.txt                 # Dependências do projeto
├── README.md
├── app/
│   ├── models/                      # Lógica do jogo (Fase 1, intacta)
│   │   ├── peca.py                  # Classe abstrata Peca
│   │   ├── tabuleiro.py             # Grade 8x8 e operações de posição
│   │   ├── jogada.py                # Jogada e Jogador
│   │   ├── jogo_tabuleiro.py        # Classe abstrata JogoTabuleiro
│   │   ├── damas.py                 # PecaDamas e Damas (regras concretas)
│   │   └── tema.py                  # Tema visual (cores do tabuleiro/peças)
│   ├── views/
│   │   ├── menu_screen.py           # Tela inicial
│   │   ├── config_screen.py         # Configuração dos jogadores
│   │   ├── board_screen.py          # Tabuleiro interativo
│   │   └── theme_screen.py          # Seleção de tema visual
│   └── controllers/
│       └── game_controller.py       # Ponte entre View e Model
├── docs/
│   ├── uml_damas.png                # Diagrama UML de classes
│   └── screenshots/                 # Capturas de tela do aplicativo
├── slides/
│   └── apresentacao.pdf             # Slides da apresentação final
└── tests/
    └── test_jogos.py                # Testes unitários da lógica do jogo
```

### Camadas

**Model** (`app/models/`) — contém toda a lógica de regras do jogo, sem nenhuma
dependência de Kivy. As classes principais são `Peca`, `Tabuleiro`, `Jogada`,
`Jogador`, `JogoTabuleiro` (base abstrata) e `Damas`/`PecaDamas` (implementação
concreta). Essa camada não foi alterada em relação à Fase 1 — apenas os imports foram
ajustados para a nova estrutura de pastas.

**View** (`app/views/`) — telas construídas com componentes KivyMD. Nenhuma tela
acessa atributos internos do modelo diretamente; toda leitura de estado passa por
métodos públicos do `GameController`.

**Controller** (`app/controllers/game_controller.py`) — única classe que conhece
tanto o modelo quanto a necessidade da interface. Expõe métodos como
`iniciar_partida()`, `executar_jogada()`, `get_tabuleiro()` e `definir_tema()`, e usa
um callback (`on_update`) para notificar a View sempre que o estado do jogo muda.

### Conceitos de POO Aplicados

- **Encapsulamento:** atributos protegidos com prefixo `_` em todas as classes;
  acesso externo apenas via `@property` (ex.: `peca.jogador`, `tabuleiro.linhas`).
- **Herança:** `PecaDamas` herda de `Peca`; `Damas` herda de `JogoTabuleiro` e recebe
  `executar_turno()`/`iniciar()` prontos, implementando apenas os métodos abstratos
  específicos das regras de Damas.
- **Polimorfismo:** `simbolo()` se comporta diferente conforme o estado da peça
  (normal ou promovida); os métodos abstratos de `JogoTabuleiro`
  (`validar_jogada()`, `aplicar_jogada()`, `verificar_fim_de_jogo()`) têm
  implementação própria em `Damas`.
- **Abstração / Interface:** `JogoTabuleiro` e `Peca` são classes abstratas (ABC) que
  definem contratos via `@abstractmethod`, obrigando qualquer jogo ou peça concreta a
  implementar um conjunto mínimo de comportamentos.
- **Composição:** `JogoTabuleiro` cria e possui um `Tabuleiro` — este nasce e morre
  junto com o jogo.
- **Agregação:** os objetos `Jogador` são criados fora do jogo e passados a ele;
  existem de forma independente.

Diagrama UML completo disponível em https://docs.google.com/presentation/d/1BV1fp0jRnuGTTSIVTVbdJms2yjKBSV5a/edit?usp=sharing&ouid=109479687600813829656&rtpof=true&sd=true.

## Telas Implementadas

| Tela | Descrição |
|---|---|
| Menu Principal | Tela inicial com nome do jogo e botões de navegação |
| Configuração de Partida | Entrada dos nomes dos dois jogadores |
| Tabuleiro | Tabuleiro 8×8 interativo, com destaque de peça selecionada e jogadas possíveis, painel de status e indicador de turno |
| Personalização de Tema | Seleção entre 4 temas de cores (Clássico, Azul, Verde, Vinho) para tabuleiro e peças |
| Resultado | Diálogo exibido ao fim da partida, com nome do vencedor e opções de novo jogo ou voltar ao menu |

### Capturas de Tela

![Telas] https://docs.google.com/presentation/d/1BV1fp0jRnuGTTSIVTVbdJms2yjKBSV5a/edit?usp=sharing&ouid=109479687600813829656&rtpof=true&sd=true


## Instalação e Execução

### Pré-requisitos

- Python 3.11 (o Kivy ainda não possui suporte estável para versões mais recentes)

### Passo a passo

```bash
# 1. Clonar o repositório
git clone https://github.com/isaacBR1212/poo-jogo-damas.git
cd poo-jogo-damas

# 2. Criar e ativar o ambiente virtual
python -m venv venv
# Windows (Git Bash):
source venv/Scripts/activate
# Linux/macOS:
source venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Executar o jogo
python main.py
```

## Como Jogar

1. Na tela inicial, clique em **NOVO JOGO**.
2. Informe os nomes dos dois jogadores e clique em **INICIAR JOGO**.
3. Clique em uma peça própria para selecioná-la — os destinos possíveis são
   destacados em amarelo.
4. Clique em uma casa destacada para mover a peça até lá.
5. Capturas são obrigatórias quando disponíveis: se houver uma captura possível, o
   jogo não permite movimentos simples.
6. Ao atingir a última linha do tabuleiro, a peça é promovida a Dama automaticamente.
7. O jogo termina quando um jogador perde todas as peças ou fica sem jogadas
   possíveis. Um diálogo exibe o resultado, com opção de nova partida.

Para trocar o tema visual, use o botão **CONFIGURAÇÕES** no menu ou o ícone de
paleta 🎨 na barra superior durante a partida.

## Testes

A lógica do jogo (camada Model) possui testes unitários cobrindo validação de
jogadas, captura obrigatória, promoção a dama e detecção de fim de jogo:

```bash
python tests/test_jogos.py
```

## Decisões de Projeto

- A lógica da Fase 1 foi mantida intacta, apenas com ajuste dos caminhos de import
  para a nova estrutura de pastas (`app/models/`).
- O padrão de comunicação View → Model é feito exclusivamente através do
  `GameController`, nunca por acesso direto a atributos do jogo.
- O tema visual (`app/models/tema.py`) foi modelado como uma classe de dados simples,
  sem nenhuma dependência de Kivy, permitindo trocar a paleta de cores sem qualquer
  acoplamento com a lógica de desenho das telas.
- O tabuleiro é renderizado com `canvas` do Kivy (formas geométricas), e não com
  imagens, simplificando a troca de temas em tempo real.

## Limitações e Melhorias Futuras

- Não há suporte a desfazer jogadas.
- Não há modo online ou contra IA.
- O segundo jogo proposto na atividade original (Xadrez Simplificado) não recebeu
  interface gráfica nesta fase, por limitação de tempo — a lógica de terminal já está
  implementada e poderia ser integrada futuramente seguindo o mesmo padrão MVC usado
  para Damas.
- Animações de movimento das peças poderiam ser adicionadas com a API `Animation` do
  Kivy.

## Tecnologias

- Python 3.11
- KivyMD 1.1.1
- Kivy 2.3.1
