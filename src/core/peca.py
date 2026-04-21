from abc import ABC, abstractmethod


class Peca(ABC):
    def __init__(self, jogador: int):
        self._jogador = jogador  # 1 ou 2

    @property
    def jogador(self) -> int:
        return self._jogador

    @abstractmethod
    def simbolo(self) -> str:
        pass

    def __str__(self) -> str:
        return self.simbolo()