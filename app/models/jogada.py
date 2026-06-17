class Jogada:
    def __init__(self, orig_l: int, orig_c: int, dest_l: int, dest_c: int):
        self.orig_l = orig_l
        self.orig_c = orig_c
        self.dest_l = dest_l
        self.dest_c = dest_c

    def __repr__(self) -> str:
        return f"Jogada(({self.orig_l},{self.orig_c}) -> ({self.dest_l},{self.dest_c}))"


class Jogador:
    def __init__(self, numero: int, nome: str):
        self._numero = numero
        self._nome = nome

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def nome(self) -> str:
        return self._nome

    def __str__(self) -> str:
        return self._nome