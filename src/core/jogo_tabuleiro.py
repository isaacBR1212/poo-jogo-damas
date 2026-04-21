from abc import ABC, abstractmethod
from src.core.tabuleiro import Tabuleiro
from src.core.jogada import Jogada, Jogador


class JogoTabuleiro(ABC):
    def __init__(self, jogador1: Jogador, jogador2: Jogador):
        self._jogadores = [jogador1, jogador2]
        self._turno_atual = 0  
        self._tabuleiro: Tabuleiro = self._criar_tabuleiro()
        self._fim = False
        self._vencedor: Jogador | None = None

    @property
    def jogador_atual(self) -> Jogador:
        return self._jogadores[self._turno_atual]

    @property
    def tabuleiro(self) -> Tabuleiro:
        return self._tabuleiro

    @property
    def fim(self) -> bool:
        return self._fim

    @property
    def vencedor(self) -> Jogador | None:
        return self._vencedor

    @abstractmethod
    def _criar_tabuleiro(self) -> Tabuleiro:
        pass

    @abstractmethod
    def inicializar_tabuleiro(self) -> None:
        pass

    @abstractmethod
    def validar_jogada(self, jogada: Jogada) -> bool:
        pass

    @abstractmethod
    def aplicar_jogada(self, jogada: Jogada) -> None:
        pass

    @abstractmethod
    def verificar_fim_de_jogo(self) -> None:
        pass

    @abstractmethod
    def exibir_tabuleiro(self) -> None:
        pass

    def _avancar_turno(self) -> None:
        self._turno_atual = 1 - self._turno_atual

    def executar_turno(self, jogada: Jogada) -> bool:
        """Valida, aplica e avança o turno. """
        if self._fim:
            print("O jogo já terminou.")
            return False
        if not self.validar_jogada(jogada):
            return False
        self.aplicar_jogada(jogada)
        self.verificar_fim_de_jogo()
        if not self._fim:
            self._avancar_turno()
        return True

    def iniciar(self) -> None:
        self._fim = False
        self._vencedor = None
        self._turno_atual = 0
        self.inicializar_tabuleiro()