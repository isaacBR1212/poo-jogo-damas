from app.models.jogada import Jogada, Jogador
from app.models.damas import Damas
from app.models.tema import Tema, TEMA_CLASSICO


class GameController:
    """Faz a ponte entre a interface gráfica e a lógica do jogo."""

    def __init__(self):
        self.game = None          # objeto Damas (criado em iniciar_partida)
        self.on_update = None     
        self.tema = TEMA_CLASSICO  # tema visual atual (cores do tabuleiro/peças)

    # Iniciar 

    def iniciar_partida(self, nome1: str, nome2: str) -> None:
        j1 = Jogador(1, nome1 or "Jogador 1")
        j2 = Jogador(2, nome2 or "Jogador 2")
        self.game = Damas(j1, j2)
        self.game.iniciar()
        self._notificar()

    # Ações do jogo 

    def executar_jogada(self, ol: int, oc: int, dl: int, dc: int) -> bool:
        if not self.game:
            return False
        ok = self.game.executar_turno(Jogada(ol, oc, dl, dc))
        if ok:
            self._notificar()
        return ok

    def reiniciar(self) -> None:
        if self.game:
            self.game.iniciar()
            self._notificar()

    def definir_tema(self, tema: Tema) -> None:
        self.tema = tema
        self._notificar()


    def get_tabuleiro(self) -> list[list]:
        """Retorna matriz 8x8 com símbolo de cada peça ou None."""
        if not self.game:
            return [[None] * 8 for _ in range(8)]
        return [
            [self.game.tabuleiro.obter(l, c) for c in range(8)]
            for l in range(8)
        ]

    def get_jogador_atual(self) -> str:
        if not self.game:
            return ""
        return self.game.jogador_atual.nome

    def get_numero_jogador_atual(self) -> int:
        if not self.game:
            return 1
        return self.game.jogador_atual.numero

    def get_fim(self) -> bool:
        """True se o jogo terminou."""
        return self.game.fim if self.game else False

    def get_vencedor(self) -> str | None:
        if not self.game or not self.game.vencedor:
            return None
        return self.game.vencedor.nome

    def get_pecas_count(self, jogador: int) -> int:
        if not self.game:
            return 0
        count = 0
        for l in range(8):
            for c in range(8):
                p = self.game.tabuleiro.obter(l, c)
                if p and p.jogador == jogador:
                    count += 1
        return count

    def get_jogadas_possiveis(self, l: int, c: int) -> list[tuple]:
        if not self.game:
            return []
        jogadas = self.game._jogadas_possiveis_peca(l, c)
        return [(j.dest_l, j.dest_c) for j in jogadas]


    def _notificar(self) -> None:
        if self.on_update:
            self.on_update()