from typing import Optional
from app.models.peca import Peca


class Tabuleiro:
    def __init__(self, linhas: int, colunas: int):
        self._linhas = linhas
        self._colunas = colunas
        self._grade: list[list[Optional[Peca]]] = [
            [None] * colunas for _ in range(linhas)
        ]

    @property
    def linhas(self) -> int:
        return self._linhas

    @property
    def colunas(self) -> int:
        return self._colunas

    def posicao_valida(self, linha: int, col: int) -> bool:
        return 0 <= linha < self._linhas and 0 <= col < self._colunas

    def obter(self, linha: int, col: int) -> Optional[Peca]:
        if not self.posicao_valida(linha, col):
            raise ValueError(f"Posição ({linha},{col}) fora do tabuleiro.")
        return self._grade[linha][col]

    def colocar(self, linha: int, col: int, peca: Optional[Peca]) -> None:
        if not self.posicao_valida(linha, col):
            raise ValueError(f"Posição ({linha},{col}) fora do tabuleiro.")
        self._grade[linha][col] = peca

    def mover(self, orig_l: int, orig_c: int, dest_l: int, dest_c: int) -> None:
        peca = self.obter(orig_l, orig_c)
        self.colocar(dest_l, dest_c, peca)
        self.colocar(orig_l, orig_c, None)

    def limpar(self) -> None:
        self._grade = [[None] * self._colunas for _ in range(self._linhas)]