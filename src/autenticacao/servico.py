"""Serviço de cadastro e login. A dependência externa (repositório) é injetada
no construtor, o que permite substituí-la por um Mock nos testes."""
import hashlib
import os

from autenticacao.excecoes import UsuarioJaExisteError
from autenticacao.modelos import Usuario
from autenticacao.repositorio import RepositorioUsuarios
from autenticacao.validadores import validar_forca_senha, validar_tamanho_senha


def gerar_hash_senha(senha: str, sal: str) -> str:
    """Hash SHA-256 de sal + senha. A senha nunca é armazenada em texto puro."""
    return hashlib.sha256((sal + senha).encode("utf-8")).hexdigest()


class ServicoAutenticacao:
    def __init__(self, repositorio: RepositorioUsuarios) -> None:
        self._repositorio = repositorio

    def cadastrar(self, username: str, senha: str) -> Usuario:
        """Valida as regras de cadastro e persiste o novo usuário."""
        self._validar_regras_senha(senha)
        self._garantir_username_disponivel(username)

        sal = os.urandom(16).hex()
        usuario = Usuario(username, gerar_hash_senha(senha, sal), sal)
        self._repositorio.salvar(usuario)
        return usuario

    @staticmethod
    def _validar_regras_senha(senha: str) -> None:
        validar_tamanho_senha(senha)  # RN02
        validar_forca_senha(senha)    # RN03

    def _garantir_username_disponivel(self, username: str) -> None:
        if self._repositorio.existe(username):  # RN04
            raise UsuarioJaExisteError(f"RN04: o usuário '{username}' já está cadastrado.")
