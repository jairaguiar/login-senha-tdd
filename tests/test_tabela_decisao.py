"""RN03 – Tabela de decisão da força da senha.

Condições: C1 = tem letra maiúscula, C2 = tem dígito, C3 = tem caractere especial.
Ação: aceitar somente quando C1, C2 e C3 forem verdadeiras.
Cada linha abaixo é uma coluna (R1..R8) da tabela de decisão completa (2^3 = 8).
"""
import pytest

from autenticacao.excecoes import SenhaFracaError
from autenticacao.validadores import validar_forca_senha

TABELA_DECISAO = [
    # (id da regra, senha,        C1,    C2,    C3,    aceita)
    ("R1_TTT", "Senha#2026",  True,  True,  True,  True),
    ("R2_TTF_CT09", "Senha2026x",  True,  True,  False, False),
    ("R3_TFT", "Senha#Forte", True,  False, True,  False),
    ("R4_TFF", "SenhaForte",  True,  False, False, False),
    ("R5_FTT", "senha#2026",  False, True,  True,  False),
    ("R6_FTF", "senha2026x",  False, True,  False, False),
    ("R7_FFT_CT10", "senha#forte", False, False, True,  False),
    ("R8_FFF", "senhaforte",  False, False, False, False),
]


@pytest.mark.parametrize(
    "senha,aceita",
    [(senha, aceita) for _, senha, _, _, _, aceita in TABELA_DECISAO],
    ids=[regra for regra, *_ in TABELA_DECISAO],
)
def test_rn03_tabela_decisao_forca_senha(senha, aceita):
    if aceita:
        validar_forca_senha(senha)
    else:
        with pytest.raises(SenhaFracaError):
            validar_forca_senha(senha)
