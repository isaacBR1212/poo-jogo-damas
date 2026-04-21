
Este projeto implementa uma arquitetura orientada a objetos para jogos de tabuleiro em Python, focada em extensibilidade e reuso de código.

## Integrantes
    Isaac Leonardo da Silva

## Arquitetura do Projeto
A solução foi dividida em dois pacotes principais para garantir o baixo acoplamento:

1.  **`src/core/` (O Núcleo):** Contém as classes abstratas e lógicas comuns a qualquer jogo de tabuleiro (regras de turno, estrutura de grade, gerenciamento de jogadores).
2.  **`src/jogos/` (As Implementações):** Contém as regras específicas. Aqui, as classes herdam do núcleo e implementam apenas o que muda (como o movimento das peças).

### Principais Classes
* **`JogoTabuleiro` (Classe Abstrata):** Define o "esqueleto" do jogo. Utiliza métodos abstratos (`@abstractmethod`) como `validar_jogada` que obrigam os novos jogos a seguir um padrão.
* **`Tabuleiro`:** Gerencia a grade bidimensional e a localização das peças.
* **`Peca`:** Classe base para representar qualquer elemento no tabuleiro.
* **`Jogada`:** Objeto de transferência que carrega as coordenadas de origem e destino.

## Jogos Implementados
1.  **Damas:** Jogo funcional com regras de captura obrigatória, promoção de damas e alternância de turnos.
2.  **Xadrez Simplificado:** Implementação básica focada na movimentação de diferentes tipos de peças sobre a mesma base do tabuleiro.

## Decisões de Projeto
* **Herança vs. Composição:** Utilizamos herança para especializar os jogos (`Damas` *é um* `JogoTabuleiro`) e composição para o tabuleiro (`Jogo` *tem um* `Tabuleiro`).
* **Polimorfismo:** O método `executar_turno` é genérico na base, mas se comporta de forma diferente dependendo se o objeto instanciado é Damas ou Xadrez.
* **Encapsulamento:** Atributos críticos como `_grade` e `_turno_atual` são protegidos (usando `_`), sendo acessados apenas por propriedades ou métodos específicos.

## Execucão
 Na raiz do projeto execute:

python main.py