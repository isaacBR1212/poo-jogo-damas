from src.core.peca import Peca
from src.core.tabuleiro import Tabuleiro
from src.core.jogada import Jogada, Jogador
from src.core.jogo_tabuleiro import JogoTabuleiro


# ── Peças ──────────────────────────────────────────────────────────────────────

class PecaXadrez(Peca):
    NOMES = {1: "branca", 2: "preta"}

    def movimentos_validos(self, l: int, c: int, tabuleiro: Tabuleiro) -> list[tuple[int, int]]:
        raise NotImplementedError


class Peao(PecaXadrez):
    def simbolo(self) -> str:
        return "P" if self._jogador == 1 else "p"

    def movimentos_validos(self, l: int, c: int, t: Tabuleiro) -> list[tuple[int, int]]:
        destinos = []
        direcao = -1 if self._jogador == 1 else 1
        # Avançar uma casa
        nl = l + direcao
        if t.posicao_valida(nl, c) and t.obter(nl, c) is None:
            destinos.append((nl, c))
            # Avanço inicial de duas casas
            inicio = 6 if self._jogador == 1 else 1
            nl2 = l + 2 * direcao
            if l == inicio and t.obter(nl2, c) is None:
                destinos.append((nl2, c))
        for dc in [-1, 1]:
            nl, nc = l + direcao, c + dc
            if t.posicao_valida(nl, nc):
                alvo = t.obter(nl, nc)
                if alvo and alvo.jogador != self._jogador:
                    destinos.append((nl, nc))
        return destinos


class Torre(PecaXadrez):
    def simbolo(self) -> str:
        return "T" if self._jogador == 1 else "t"

    def movimentos_validos(self, l: int, c: int, t: Tabuleiro) -> list[tuple[int, int]]:
        return _deslizante(self._jogador, l, c, t, [(0, 1), (0, -1), (1, 0), (-1, 0)])


class Bispo(PecaXadrez):
    def simbolo(self) -> str:
        return "B" if self._jogador == 1 else "b"

    def movimentos_validos(self, l: int, c: int, t: Tabuleiro) -> list[tuple[int, int]]:
        return _deslizante(self._jogador, l, c, t, [(1, 1), (1, -1), (-1, 1), (-1, -1)])


class Rainha(PecaXadrez):
    def simbolo(self) -> str:
        return "Q" if self._jogador == 1 else "q"

    def movimentos_validos(self, l: int, c: int, t: Tabuleiro) -> list[tuple[int, int]]:
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return _deslizante(self._jogador, l, c, t, dirs)


class Rei(PecaXadrez):
    def simbolo(self) -> str:
        return "K" if self._jogador == 1 else "k"

    def movimentos_validos(self, l: int, c: int, t: Tabuleiro) -> list[tuple[int, int]]:
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        destinos = []
        for dl, dc in dirs:
            nl, nc = l + dl, c + dc
            if t.posicao_valida(nl, nc):
                alvo = t.obter(nl, nc)
                if alvo is None or alvo.jogador != self._jogador:
                    destinos.append((nl, nc))
        return destinos


class Cavalo(PecaXadrez):
    def simbolo(self) -> str:
        return "C" if self._jogador == 1 else "c"

    def movimentos_validos(self, l: int, c: int, t: Tabuleiro) -> list[tuple[int, int]]:
        saltos = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        destinos = []
        for dl, dc in saltos:
            nl, nc = l + dl, c + dc
            if t.posicao_valida(nl, nc):
                alvo = t.obter(nl, nc)
                if alvo is None or alvo.jogador != self._jogador:
                    destinos.append((nl, nc))
        return destinos


def _deslizante(jogador: int, l: int, c: int, t: Tabuleiro, dirs: list) -> list[tuple[int, int]]:
    destinos = []
    for dl, dc in dirs:
        nl, nc = l + dl, c + dc
        while t.posicao_valida(nl, nc):
            alvo = t.obter(nl, nc)
            if alvo is None:
                destinos.append((nl, nc))
            else:
                if alvo.jogador != jogador:
                    destinos.append((nl, nc))
                break
            nl += dl
            nc += dc
    return destinos


# ── Jogo ───────────────────────────────────────────────────────────────────────

class XadrezSimplificado(JogoTabuleiro):
    def _criar_tabuleiro(self) -> Tabuleiro:
        return Tabuleiro(8, 8)

    def _fila_pecas(self, jogador: int) -> list[PecaXadrez]:
        return [Torre(jogador), Cavalo(jogador), Bispo(jogador), Rainha(jogador),
                Rei(jogador), Bispo(jogador), Cavalo(jogador), Torre(jogador)]

    def inicializar_tabuleiro(self) -> None:
        self._tabuleiro.limpar()
        # Jogador 2 
        for c, peca in enumerate(self._fila_pecas(2)):
            self._tabuleiro.colocar(0, c, peca)
        for c in range(8):
            self._tabuleiro.colocar(1, c, Peao(2))
        # Jogador 1 
        for c in range(8):
            self._tabuleiro.colocar(6, c, Peao(1))
        for c, peca in enumerate(self._fila_pecas(1)):
            self._tabuleiro.colocar(7, c, peca)

    def _posicao_rei(self, jogador: int) -> tuple[int, int] | None:
        for l in range(8):
            for c in range(8):
                p = self._tabuleiro.obter(l, c)
                if isinstance(p, Rei) and p.jogador == jogador:
                    return (l, c)
        return None

    def _rei_em_xeque(self, jogador: int) -> bool:
        pos_rei = self._posicao_rei(jogador)
        if pos_rei is None:
            return True
        oponente = 2 if jogador == 1 else 1
        for l in range(8):
            for c in range(8):
                p = self._tabuleiro.obter(l, c)
                if isinstance(p, PecaXadrez) and p.jogador == oponente:
                    if pos_rei in p.movimentos_validos(l, c, self._tabuleiro):
                        return True
        return False

    def _simular_jogada(self, jogada: Jogada) -> bool:
        t = self._tabuleiro
        peca_orig = t.obter(jogada.orig_l, jogada.orig_c)
        peca_dest = t.obter(jogada.dest_l, jogada.dest_c)
        t.mover(jogada.orig_l, jogada.orig_c, jogada.dest_l, jogada.dest_c)
        em_xeque = self._rei_em_xeque(self.jogador_atual.numero)
        t.colocar(jogada.orig_l, jogada.orig_c, peca_orig)
        t.colocar(jogada.dest_l, jogada.dest_c, peca_dest)
        return not em_xeque

    def validar_jogada(self, jogada: Jogada) -> bool:
        t = self._tabuleiro
        orig_l, orig_c = jogada.orig_l, jogada.orig_c
        dest_l, dest_c = jogada.dest_l, jogada.dest_c

        if not t.posicao_valida(orig_l, orig_c) or not t.posicao_valida(dest_l, dest_c):
            print("Posição fora do tabuleiro.")
            return False

        peca = t.obter(orig_l, orig_c)
        if not isinstance(peca, PecaXadrez):
            print("Não há peça na posição de origem.")
            return False
        if peca.jogador != self.jogador_atual.numero:
            print("Essa peça não pertence ao jogador atual.")
            return False

        destinos = peca.movimentos_validos(orig_l, orig_c, t)
        if (dest_l, dest_c) not in destinos:
            print("Movimento inválido para essa peça.")
            return False

        if not self._simular_jogada(jogada):
            print("Essa jogada deixa seu rei em xeque!")
            return False

        return True

    def aplicar_jogada(self, jogada: Jogada) -> None:
        self._tabuleiro.mover(jogada.orig_l, jogada.orig_c, jogada.dest_l, jogada.dest_c)
        # Promoção de peão
        peca = self._tabuleiro.obter(jogada.dest_l, jogada.dest_c)
        if isinstance(peca, Peao):
            if peca.jogador == 1 and jogada.dest_l == 0:
                self._tabuleiro.colocar(jogada.dest_l, jogada.dest_c, Rainha(1))
            elif peca.jogador == 2 and jogada.dest_l == 7:
                self._tabuleiro.colocar(jogada.dest_l, jogada.dest_c, Rainha(2))

    def verificar_fim_de_jogo(self) -> None:
        proximo_idx = 1 - self._turno_atual
        proximo_jogador = self._jogadores[proximo_idx].numero

        if self._posicao_rei(proximo_jogador) is None:
            self._fim = True
            self._vencedor = self._jogadores[self._turno_atual]
            return

        tem_legal = False
        for l in range(8):
            if tem_legal:
                break
            for c in range(8):
                p = self._tabuleiro.obter(l, c)
                if not isinstance(p, PecaXadrez) or p.jogador != proximo_jogador:
                    continue
                for (dl, dc) in p.movimentos_validos(l, c, self._tabuleiro):
                    if self._simular_jogada(Jogada(l, c, dl, dc)):
                        tem_legal = True
                        break

        if not tem_legal:
            self._fim = True
            if self._rei_em_xeque(proximo_jogador):
                self._vencedor = self._jogadores[self._turno_atual]
            else:
                self._vencedor = None 

    def exibir_tabuleiro(self) -> None:
        t = self._tabuleiro
        print("  a b c d e f g h")
        for l in range(8):
            linha_str = f"{8 - l} "
            for c in range(8):
                p = t.obter(l, c)
                linha_str += (p.simbolo() if p else ".") + " "
            print(linha_str + f"{8 - l}")
        print("  a b c d e f g h")
        print()