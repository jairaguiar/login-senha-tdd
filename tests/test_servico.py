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


# ---------------------------------------------------------------- RN05 (login)
from autenticacao.excecoes import ContaBloqueadaError, CredenciaisInvalidasError  # noqa: E402
from autenticacao.modelos import Usuario  # noqa: E402
from autenticacao.servico import gerar_hash_senha  # noqa: E402

SENHA_CORRETA = "Senha#2026"


def _usuario(tentativas_falhas=0, bloqueado=False):
    return Usuario(
        username="jair_rosa",
        senha_hash=gerar_hash_senha(SENHA_CORRETA, "sal-fixo"),
        sal="sal-fixo",
        tentativas_falhas=tentativas_falhas,
        bloqueado=bloqueado,
    )


def test_ct12_login_correto_autentica_e_zera_tentativas(repo):
    usuario = _usuario(tentativas_falhas=2)
    repo.buscar.return_value = usuario

    assert ServicoAutenticacao(repo).login("jair_rosa", SENHA_CORRETA) is True
    assert usuario.tentativas_falhas == 0
    repo.salvar.assert_called_once_with(usuario)


# RN05 – valores-limite do contador: a 3ª falha consecutiva bloqueia a conta.
@pytest.mark.parametrize(
    "falhas_anteriores,deve_bloquear",
    [(0, False), (1, False), (2, True)],
    ids=["1a_falha", "2a_falha_limite_menos_1", "CT13_3a_falha_no_limite"],
)
def test_ct13_senha_errada_conta_falha_e_bloqueia_na_terceira(repo, falhas_anteriores, deve_bloquear):
    usuario = _usuario(tentativas_falhas=falhas_anteriores)
    repo.buscar.return_value = usuario

    with pytest.raises(CredenciaisInvalidasError):
        ServicoAutenticacao(repo).login("jair_rosa", "SenhaErrada#1")

    assert usuario.tentativas_falhas == falhas_anteriores + 1
    assert usuario.bloqueado is deve_bloquear
    repo.salvar.assert_called_once_with(usuario)


def test_ct14_conta_bloqueada_rejeita_mesmo_com_senha_correta(repo):
    repo.buscar.return_value = _usuario(tentativas_falhas=3, bloqueado=True)

    with pytest.raises(ContaBloqueadaError):
        ServicoAutenticacao(repo).login("jair_rosa", SENHA_CORRETA)

    repo.salvar.assert_not_called()


def test_ct16_login_de_usuario_inexistente_e_rejeitado(repo):
    repo.buscar.return_value = None

    with pytest.raises(CredenciaisInvalidasError):
        ServicoAutenticacao(repo).login("fantasma", SENHA_CORRETA)

    repo.buscar.assert_called_once_with("fantasma")
