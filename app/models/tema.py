class Tema:

    def __init__(self, nome: str, casa_clara: tuple, casa_escura: tuple,
                 peca_j1: tuple, peca_j2: tuple, dama_anel: tuple = (0.85, 0.65, 0.10, 1)):
        self.nome = nome
        self.casa_clara = casa_clara
        self.casa_escura = casa_escura
        self.peca_j1 = peca_j1
        self.peca_j2 = peca_j2
        self.dama_anel = dama_anel   

# Temas 

TEMA_CLASSICO = Tema(
    nome="Clássico",
    casa_clara=(0.94, 0.85, 0.71, 1),
    casa_escura=(0.55, 0.37, 0.24, 1),
    peca_j1=(0.95, 0.95, 0.90, 1),
    peca_j2=(0.15, 0.12, 0.10, 1),
)

TEMA_AZUL = Tema(
    nome="Azul",
    casa_clara=(0.85, 0.90, 0.96, 1),
    casa_escura=(0.20, 0.35, 0.55, 1),
    peca_j1=(0.98, 0.98, 0.98, 1),
    peca_j2=(0.08, 0.10, 0.20, 1),
)

TEMA_VERDE = Tema(
    nome="Verde",
    casa_clara=(0.90, 0.94, 0.85, 1),
    casa_escura=(0.25, 0.45, 0.20, 1),
    peca_j1=(0.97, 0.96, 0.88, 1),
    peca_j2=(0.10, 0.20, 0.10, 1),
)

TEMA_VINHO = Tema(
    nome="Vinho",
    casa_clara=(0.96, 0.90, 0.88, 1),
    casa_escura=(0.45, 0.15, 0.18, 1),
    peca_j1=(0.98, 0.96, 0.94, 1),
    peca_j2=(0.20, 0.08, 0.08, 1),
)

TEMAS_DISPONIVEIS = [TEMA_CLASSICO, TEMA_AZUL, TEMA_VERDE, TEMA_VINHO]