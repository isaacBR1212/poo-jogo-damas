import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.core.jogada import Jogada, Jogador
from src.jogos.damas import Damas, PecaDamas
from src.jogos.xadrez import XadrezSimplificado, Peao, Rei, Torre, Rainha


# ── Helpers ────────────────────────────────────────────────────────────────────

def novo_damas():
    j1 = Jogador(1, "J1")
    j2 = Jogador(2, "J2")
    jogo = Damas(j1, j2)
    jogo.iniciar()
    return jogo


def novo_xadrez():
    j1 = Jogador(1, "Brancas")
    j2 = Jogador(2, "Pretas")
    jogo = XadrezSimplificado(j1, j2)
    jogo.iniciar()
    return jogo


# ── Testes Damas ───────────────────────────────────────────────────────────────

def test_damas_jogada_valida():
    jogo = novo_damas()
    # Brancas estão em linhas 5-7, casas ímpares
    assert jogo.executar_turno(Jogada(5, 0, 4, 1))
    print("PASS: test_damas_jogada_valida")


def test_damas_jogada_invalida_casa_propria():
    jogo = novo_damas()
    # Tentar mover para casa ocupada por aliado
    resultado = jogo.validar_jogada(Jogada(5, 0, 6, 1))
    assert not resultado
    print("PASS: test_damas_jogada_invalida_casa_propria")


def test_damas_peca_errada():
    jogo = novo_damas()
    # J1 tenta mover peça de J2
    resultado = jogo.validar_jogada(Jogada(2, 1, 3, 0))
    assert not resultado
    print("PASS: test_damas_peca_errada")


def test_damas_captura_obrigatoria():
    jogo = novo_damas()
    t = jogo.tabuleiro
    # Limpa e posiciona captura forçada
    t.limpar()
    t.colocar(4, 1, PecaDamas(1))
    t.colocar(3, 2, PecaDamas(2))
    # Movimento simples deve ser recusado
    resultado = jogo.validar_jogada(Jogada(4, 1, 3, 0))
    assert not resultado
    print("PASS: test_damas_captura_obrigatoria")


def test_damas_captura_executada():
    jogo = novo_damas()
    t = jogo.tabuleiro
    t.limpar()
    t.colocar(4, 1, PecaDamas(1))
    t.colocar(3, 2, PecaDamas(2))
    ok = jogo.executar_turno(Jogada(4, 1, 2, 3))
    assert ok
    assert t.obter(3, 2) is None  # Peça capturada removida
    print("PASS: test_damas_captura_executada")


def test_damas_promocao():
    jogo = novo_damas()
    t = jogo.tabuleiro
    t.limpar()
    t.colocar(1, 0, PecaDamas(1))
    jogo.executar_turno(Jogada(1, 0, 0, 1))
    peca = t.obter(0, 1)
    assert isinstance(peca, PecaDamas) and peca.dama
    print("PASS: test_damas_promocao")


def test_damas_vitoria():
    jogo = novo_damas()
    t = jogo.tabuleiro
    t.limpar()
    # J1 em (2,1), J2 em (1,2) → J1 captura pulando para (0,3)
    t.colocar(2, 1, PecaDamas(1))
    t.colocar(1, 2, PecaDamas(2))
    ok = jogo.executar_turno(Jogada(2, 1, 0, 3))
    assert ok, "Captura deveria ser aceita"
    assert t.obter(1, 2) is None, "Peça capturada deve ser removida"
    assert jogo.fim, "Jogo deve ter terminado"
    assert jogo.vencedor and jogo.vencedor.numero == 1
    print("PASS: test_damas_vitoria")


# ── Testes Xadrez ──────────────────────────────────────────────────────────────

def test_xadrez_peca_errada():
    jogo = novo_xadrez()
    resultado = jogo.validar_jogada(Jogada(1, 0, 2, 0))  # Peão preto, vez das brancas
    assert not resultado
    print("PASS: test_xadrez_peca_errada")


def test_xadrez_peao_avanca():
    jogo = novo_xadrez()
    assert jogo.executar_turno(Jogada(6, 4, 4, 4))  # e2-e4
    print("PASS: test_xadrez_peao_avanca")


def test_xadrez_movimento_invalido_peca():
    jogo = novo_xadrez()
    # Torre não pode mover com peões bloqueando
    resultado = jogo.validar_jogada(Jogada(7, 0, 5, 0))
    assert not resultado
    print("PASS: test_xadrez_movimento_invalido_peca")


def test_xadrez_rei_nao_anda_para_xeque():
    jogo = novo_xadrez()
    t = jogo.tabuleiro
    t.limpar()
    t.colocar(7, 4, Rei(1))
    t.colocar(5, 5, Torre(2))
    # Rei mover para coluna 5 entraria em xeque da torre
    resultado = jogo.validar_jogada(Jogada(7, 4, 6, 5))
    assert not resultado
    print("PASS: test_xadrez_rei_nao_anda_para_xeque")


def test_xadrez_xequemate_simples():
    jogo = novo_xadrez()
    t = jogo.tabuleiro
    t.limpar()
    # Rei branco encurralado no canto, duas torres pretas
    t.colocar(7, 7, Rei(1))
    t.colocar(0, 7, Torre(2))
    t.colocar(0, 6, Torre(2))
    t.colocar(0, 0, Rei(2))
    # Simula fim: rei branco não tem movimentos legais com torres cobrindo
    jogo.verificar_fim_de_jogo()
    assert jogo.fim
    print("PASS: test_xadrez_xequemate_simples")


# ── Runner ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    testes = [
        test_damas_jogada_valida,
        test_damas_jogada_invalida_casa_propria,
        test_damas_peca_errada,
        test_damas_captura_obrigatoria,
        test_damas_captura_executada,
        test_damas_promocao,
        test_damas_vitoria,
        test_xadrez_peca_errada,
        test_xadrez_peao_avanca,
        test_xadrez_movimento_invalido_peca,
        test_xadrez_rei_nao_anda_para_xeque,
        test_xadrez_xequemate_simples,
    ]
    falhas = 0
    for t in testes:
        try:
            t()
        except AssertionError as e:
            print(f"FAIL: {t.__name__} — {e}")
            falhas += 1
        except Exception as e:
            print(f"ERROR: {t.__name__} — {e}")
            falhas += 1
    print(f"\n{'='*40}")
    print(f"Resultado: {len(testes) - falhas}/{len(testes)} testes passaram.")