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


# ------------------------------------------------------------------ RN01
from autenticacao.excecoes import SenhaContemUsernameError, UsernameInvalidoError  # noqa: E402
from autenticacao.validadores import (  # noqa: E402
    validar_senha_sem_username,
    validar_username,
)


# RN01 – username com 4 a 15 caracteres. Valores-limite: 3 | 4 | 15 | 16
@pytest.mark.parametrize(
    "username",
    ["abcd", "abcde", "a" * 14, "a" * 15, "Jair_Rosa_2026"],
    ids=["limite_inferior_4", "5_caracteres", "14_caracteres", "limite_superior_15", "letras_digitos_underscore"],
)
def test_rn01_username_valido_e_aceito(username):
    validar_username(username)


@pytest.mark.parametrize(
    "username",
    ["", "abc", "a" * 16],
    ids=["vazio", "CT02_abaixo_do_minimo_3", "CT03_acima_do_maximo_16"],
)
def test_rn01_username_com_tamanho_invalido_e_rejeitado(username):
    with pytest.raises(UsernameInvalidoError):
        validar_username(username)


@pytest.mark.parametrize(
    "username",
    ["jair rosa", "jair@rosa", "jair-rosa", "joão_rosa"],
    ids=["CT04_espaco", "arroba", "hifen", "acento"],
)
def test_ct04_username_com_caractere_invalido_e_rejeitado(username):
    with pytest.raises(UsernameInvalidoError):
        validar_username(username)


# ------------------------------------------------------------------ RN06
def test_ct15_senha_que_contem_o_username_e_rejeitada():
    with pytest.raises(SenhaContemUsernameError):
        validar_senha_sem_username("Jair#2026xx", "jair")  # ignora maiúsc./minúsc.


def test_rn06_senha_sem_o_username_e_aceita():
    validar_senha_sem_username("Senha#2026", "jair_rosa")
