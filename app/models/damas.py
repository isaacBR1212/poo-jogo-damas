from app.models.peca import Peca
from app.models.tabuleiro import Tabuleiro
from app.models.jogada import Jogada, Jogador
from app.models.jogo_tabuleiro import JogoTabuleiro

class PecaDamas(Peca):  #classe filho de peça
    def __init__(self, jogador: int, dama: bool = False):
        super().__init__(jogador)  # chama Peca.__init__
        self._dama = dama

    @property
    def dama(self) -> bool:
        return self._dama

    def promover(self) -> None:
        self._dama = True  # método de muda de estado

    def simbolo(self) -> str:
        if self._jogador == 1:
            return "D" if self._dama else "o"
        return "D" if self._dama else "x"


class Damas(JogoTabuleiro):
    def _criar_tabuleiro(self) -> Tabuleiro:
        return Tabuleiro(8, 8)

    def inicializar_tabuleiro(self) -> None:
        self._tabuleiro.limpar()

        # Player 2
        for linha in range(3):
            for col in range(8):
                if (linha + col) % 2 == 1:   # condição casa escura
                    
                    self._tabuleiro.colocar(linha, col, PecaDamas(2))

        # Player 1
        for linha in range(5, 8):
            for col in range(8):
                if (linha + col) % 2 == 1:   # condição casa escura

                    self._tabuleiro.colocar(linha, col, PecaDamas(1))

    def _pecas_do_jogador(self, numero: int) -> list[tuple[int, int]]:
        resultado = []
        for l in range(8):
            for c in range(8):
                p = self._tabuleiro.obter(l, c)
                if p and p.jogador == numero:
                    resultado.append((l, c))
        return resultado

    def _jogadas_possiveis_peca(self, l: int, c: int) -> list[Jogada]:
        peca = self._tabuleiro.obter(l, c)
        if not peca:
            return []
        jogadas = []
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        # Peças simples se movem apenas "para frente"
        if not peca.dama:
            direcoes = [(-1, -1), (-1, 1)] if peca.jogador == 1 else [(1, -1), (1, 1)]

        for dl, dc in direcoes:
            nl, nc = l + dl, c + dc
            if self._tabuleiro.posicao_valida(nl, nc):
                if self._tabuleiro.obter(nl, nc) is None:
                    jogadas.append(Jogada(l, c, nl, nc))
                else:
                    # Captura da peça
                    al, ac = nl + dl, nc + dc
                    alvo = self._tabuleiro.obter(nl, nc)
                    if (alvo and alvo.jogador != peca.jogador
                            and self._tabuleiro.posicao_valida(al, ac)
                            and self._tabuleiro.obter(al, ac) is None):
                        jogadas.append(Jogada(l, c, al, ac))
        return jogadas

    def _capturas_disponiveis(self) -> list[Jogada]:
        capturas = []
        jogador = self.jogador_atual.numero
        for l, c in self._pecas_do_jogador(jogador):
            for j in self._jogadas_possiveis_peca(l, c):
                if abs(j.dest_l - j.orig_l) == 2:
                    capturas.append(j)
        return capturas

    def validar_jogada(self, jogada: Jogada) -> bool:
        t = self._tabuleiro
        orig_l, orig_c = jogada.orig_l, jogada.orig_c
        dest_l, dest_c = jogada.dest_l, jogada.dest_c

        if not t.posicao_valida(orig_l, orig_c) or not t.posicao_valida(dest_l, dest_c):
            print("Posição fora do tabuleiro.")
            return False

        peca = t.obter(orig_l, orig_c)
        if not peca:
            print("Não há peça na posição de origem.")
            return False
        if peca.jogador != self.jogador_atual.numero:
            print("Essa peça não pertence ao jogador atual.")
            return False
        if t.obter(dest_l, dest_c) is not None:
            print("Destino ocupado.")
            return False

        jogadas_validas = self._jogadas_possiveis_peca(orig_l, orig_c)
        if jogada not in [Jogada(j.orig_l, j.orig_c, j.dest_l, j.dest_c) for j in jogadas_validas]:
            if not any(j.orig_l == orig_l and j.orig_c == orig_c and
                       j.dest_l == dest_l and j.dest_c == dest_c
                       for j in jogadas_validas):
                print("Jogada inválida.")
                return False

        capturas = self._capturas_disponiveis()
        if capturas:
            eh_captura = abs(dest_l - orig_l) == 2
            if not eh_captura:
                print("Captura é obrigatória!")
                return False

        return True

    def aplicar_jogada(self, jogada: Jogada) -> None:
        t = self._tabuleiro
        dl = jogada.dest_l - jogada.orig_l
        dc = jogada.dest_c - jogada.orig_c

        if abs(dl) == 2:
            meio_l = jogada.orig_l + dl // 2
            meio_c = jogada.orig_c + dc // 2
            t.colocar(meio_l, meio_c, None)

        peca = t.obter(jogada.orig_l, jogada.orig_c)
        t.mover(jogada.orig_l, jogada.orig_c, jogada.dest_l, jogada.dest_c)

        # Promoção
        if isinstance(peca, PecaDamas):
            if peca.jogador == 1 and jogada.dest_l == 0:
                peca.promover()
            elif peca.jogador == 2 and jogada.dest_l == 7:
                peca.promover()

    def verificar_fim_de_jogo(self) -> None:
        for numero in [1, 2]:
            pecas = self._pecas_do_jogador(numero)
            if not pecas:               # lista vazia?

                self._fim = True
                outro = 1 if numero == 2 else 2
                self._vencedor = self._jogadores[outro - 1]
                return

        proximo = 1 - self._turno_atual
        jogador_prox = self._jogadores[proximo].numero
        tem_jogada = any(
            self._jogadas_possiveis_peca(l, c)
            for l, c in self._pecas_do_jogador(jogador_prox)
        )
        if not tem_jogada:
            self._fim = True
            self._vencedor = self._jogadores[self._turno_atual]

    def exibir_tabuleiro(self) -> None:
        t = self._tabuleiro
        print("  0 1 2 3 4 5 6 7")
        for l in range(8):
            linha_str = f"{l} "
            for c in range(8):
                p = t.obter(l, c)
                if p:
                    linha_str += p.simbolo() + " "
                elif (l + c) % 2 == 0:
                    linha_str += ". "
                else:
                    linha_str += "  "
            print(linha_str)
        print()