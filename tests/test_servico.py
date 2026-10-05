"""Testes do ServicoAutenticacao com o repositório substituído por um Mock."""
from unittest.mock import Mock

import pytest

from autenticacao.excecoes import UsuarioJaExisteError
from autenticacao.servico import ServicoAutenticacao


@pytest.fixture
def repo():
    """Dublê do repositório de usuários (dependência externa)."""
    repositorio = Mock()
    repositorio.existe.return_value = False
    return repositorio


def test_ct01_cadastro_valido_salva_usuario_uma_vez(repo):
    servico = ServicoAutenticacao(repo)

    usuario = servico.cadastrar("jair_rosa", "Senha#2026")

    repo.existe.assert_called_once_with("jair_rosa")
    repo.salvar.assert_called_once_with(usuario)
    assert usuario.username == "jair_rosa"
    assert usuario.senha_hash != "Senha#2026"  # senha nunca é guardada em texto puro


def test_ct11_username_ja_cadastrado_e_rejeitado(repo):
    repo.existe.return_value = True
    servico = ServicoAutenticacao(repo)

    with pytest.raises(UsuarioJaExisteError):
        servico.cadastrar("jair_rosa", "Senha#2026")

    repo.salvar.assert_not_called()
