"""Testes de integração: serviço + repositório em memória (sem Mock)."""
import pytest

from autenticacao.excecoes import (
    ContaBloqueadaError,
    CredenciaisInvalidasError,
    UsuarioJaExisteError,
)
from autenticacao.repositorio import RepositorioEmMemoria
from autenticacao.servico import ServicoAutenticacao


@pytest.fixture
def servico():
    return ServicoAutenticacao(RepositorioEmMemoria())


def test_int_cadastro_seguido_de_login(servico):
    servico.cadastrar("jair_rosa", "Senha#2026")
    assert servico.login("jair_rosa", "Senha#2026") is True


def test_int_cadastro_duplicado(servico):
    servico.cadastrar("jair_rosa", "Senha#2026")
    with pytest.raises(UsuarioJaExisteError):
        servico.cadastrar("jair_rosa", "Outra#2026")


def test_int_fluxo_completo_de_bloqueio(servico):
    servico.cadastrar("jair_rosa", "Senha#2026")
    for _ in range(3):
        with pytest.raises(CredenciaisInvalidasError):
            servico.login("jair_rosa", "Errada#2026")
    with pytest.raises(ContaBloqueadaError):
        servico.login("jair_rosa", "Senha#2026")


def test_int_sucesso_no_meio_zera_contador(servico):
    servico.cadastrar("jair_rosa", "Senha#2026")
    for _ in range(2):
        with pytest.raises(CredenciaisInvalidasError):
            servico.login("jair_rosa", "Errada#2026")
    assert servico.login("jair_rosa", "Senha#2026") is True
    for _ in range(2):  # mais 2 falhas: total consecutivo = 2, não bloqueia
        with pytest.raises(CredenciaisInvalidasError):
            servico.login("jair_rosa", "Errada#2026")
    assert servico.login("jair_rosa", "Senha#2026") is True
