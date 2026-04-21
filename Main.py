import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.core.jogada import Jogada, Jogador
from src.jogos.damas import Damas
from src.jogos.xadrez import XadrezSimplificado


def pedir_jogada(prompt: str) -> tuple[int, int, int, int] | None:
    entrada = input(prompt).strip()
    if entrada.lower() in ("sair", "q"):
        return None
    partes = entrada.replace(",", " ").split()
    if len(partes) != 4:
        print("Formato inválido. Use: orig_l orig_c dest_l dest_c")
        return pedir_jogada(prompt)
    try:
        return tuple(int(x) for x in partes)
    except ValueError:
        print("Digite apenas números.")
        return pedir_jogada(prompt)


def pedir_jogada_xadrez(prompt: str) -> tuple[int, int, int, int] | None:
    colunas = "abcdefgh"
    entrada = input(prompt).strip().lower()
    if entrada in ("sair", "q"):
        return None
    # Aceita formato algébrico (e2 e4) ou numérico (6 4 4 4)
    partes = entrada.split()
    try:
        if len(partes) == 2 and len(partes[0]) == 2 and len(partes[1]) == 2:
            orig_c = colunas.index(partes[0][0])
            orig_l = 8 - int(partes[0][1])
            dest_c = colunas.index(partes[1][0])
            dest_l = 8 - int(partes[1][1])
            return orig_l, orig_c, dest_l, dest_c
        elif len(partes) == 4:
            return tuple(int(x) for x in partes)
        else:
            raise ValueError
    except (ValueError, IndexError):
        print("Formato inválido. Use notação algébrica (ex: e2 e4) ou linha/col (ex: 6 4 4 4)")
        return pedir_jogada_xadrez(prompt)


def jogar_damas():
    j1 = Jogador(1, "Jogador 1 (o/D)")
    j2 = Jogador(2, "Jogador 2 (x/D)")
    jogo = Damas(j1, j2)
    jogo.iniciar()

    print("\n=== DAMAS ===")
    print("Peças: o=normal, D=dama | jogador1=o, jogador2=x")
    print("Formato de jogada: orig_linha orig_col dest_linha dest_col")
    print("Digite 'sair' para encerrar.\n")

    while not jogo.fim:
        jogo.exibir_tabuleiro()
        print(f"Vez de: {jogo.jogador_atual}")
        coords = pedir_jogada("Jogada: ")
        if coords is None:
            break
        ol, oc, dl, dc = coords
        if not jogo.executar_turno(Jogada(ol, oc, dl, dc)):
            print("Jogada recusada, tente novamente.\n")

    jogo.exibir_tabuleiro()
    if jogo.vencedor:
        print(f"🏆 Vencedor: {jogo.vencedor}")
    else:
        print("Empate ou jogo encerrado.")


def jogar_xadrez():
    j1 = Jogador(1, "Brancas (maiúsculas)")
    j2 = Jogador(2, "Pretas (minúsculas)")
    jogo = XadrezSimplificado(j1, j2)
    jogo.iniciar()

    print("\n=== XADREZ SIMPLIFICADO ===")
    print("Peças: P/p=Peão, T/t=Torre, B/b=Bispo, C/c=Cavalo, Q/q=Rainha, K/k=Rei")
    print("Formato: notação algébrica (ex: e2 e4) ou linha/col (ex: 6 4 4 4)")
    print("Digite 'sair' para encerrar.\n")

    while not jogo.fim:
        jogo.exibir_tabuleiro()
        print(f"Vez de: {jogo.jogador_atual}")
        coords = pedir_jogada_xadrez("Jogada: ")
        if coords is None:
            break
        ol, oc, dl, dc = coords
        if not jogo.executar_turno(Jogada(ol, oc, dl, dc)):
            print("Jogada recusada, tente novamente.\n")

    jogo.exibir_tabuleiro()
    if jogo.vencedor:
        print(f"🏆 Vencedor: {jogo.vencedor}")
    else:
        print("Afogamento ou jogo encerrado.")


def menu():
    print("-" * 30)
    print("      JOGOS DE TABULEIRO")
    print("-" * 30)
    print("  1. Damas")
    print("  2. Xadrez Simplificado")
    print("  0. Sair")
    print("-" * 30)
    
    opcao = input("Escolha: ").strip()
    if opcao == "1":
        jogar_damas()
    elif opcao == "2":
        jogar_xadrez()
    elif opcao == "0":
        print("Até mais!")
        return
    else:
        print("Opção inválida.")
    menu()


if __name__ == "__main__":
    menu()