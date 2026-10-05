"""Testes unitários das funções puras de validação (validadores.py)."""
import pytest

from autenticacao.excecoes import SenhaInvalidaError
from autenticacao.validadores import validar_tamanho_senha


# RN02 – A senha deve ter entre 8 e 20 caracteres (inclusive).
# Valores-limite: 7 | 8 | 9 ... 19 | 20 | 21
@pytest.mark.parametrize(
    "senha",
    ["A" * 8, "A" * 9, "A" * 19, "A" * 20],
    ids=["CT06_limite_inferior_8", "9_caracteres", "19_caracteres", "CT07_limite_superior_20"],
)
def test_rn02_senha_com_tamanho_valido_e_aceita(senha):
    validar_tamanho_senha(senha)  # não deve lançar exceção


@pytest.mark.parametrize(
    "senha",
    ["", "A" * 7, "A" * 21],
    ids=["vazia", "CT05_abaixo_do_minimo_7", "CT08_acima_do_maximo_21"],
)
def test_rn02_senha_com_tamanho_invalido_e_rejeitada(senha):
    with pytest.raises(SenhaInvalidaError):
        validar_tamanho_senha(senha)
