"""Serviço de cadastro e login. A dependência externa (repositório) é injetada
no construtor, o que permite substituí-la por um Mock nos testes."""
import hashlib
import hmac
import os

from autenticacao.excecoes import (
    ContaBloqueadaError,
    CredenciaisInvalidasError,
    UsuarioJaExisteError,
)
from autenticacao.modelos import Usuario
from autenticacao.repositorio import RepositorioUsuarios
from autenticacao.validadores import (
    validar_forca_senha,
    validar_senha_sem_username,
    validar_tamanho_senha,
    validar_username,
)

LIMITE_TENTATIVAS = 3
MSG_CREDENCIAIS_INVALIDAS = "RN05: usuário ou senha inválidos."


def gerar_hash_senha(senha: str, sal: str) -> str:
    """Hash SHA-256 de sal + senha. A senha nunca é armazenada em texto puro."""
    return hashlib.sha256((sal + senha).encode("utf-8")).hexdigest()


class ServicoAutenticacao:
    def __init__(self, repositorio: RepositorioUsuarios) -> None:
        self._repositorio = repositorio

    def cadastrar(self, username: str, senha: str) -> Usuario:
        """Valida as regras de cadastro e persiste o novo usuário."""
        validar_username(username)                     # RN01
        self._validar_regras_senha(senha, username)    # RN02, RN03, RN06
        self._garantir_username_disponivel(username)   # RN04 (consulta externa)

        sal = os.urandom(16).hex()
        usuario = Usuario(username, gerar_hash_senha(senha, sal), sal)
        self._repositorio.salvar(usuario)
        return usuario

    @staticmethod
    def _validar_regras_senha(senha: str, username: str) -> None:
        validar_tamanho_senha(senha)                  # RN02
        validar_forca_senha(senha)                    # RN03
        validar_senha_sem_username(senha, username)   # RN06

    def _garantir_username_disponivel(self, username: str) -> None:
        if self._repositorio.existe(username):
            raise UsuarioJaExisteError(f"RN04: o usuário '{username}' já está cadastrado.")

    def login(self, username: str, senha: str) -> bool:
        """RN05 – autentica o usuário; a 3ª falha consecutiva bloqueia a conta.

        Usuário inexistente e senha errada geram a mesma exceção, para não
        revelar a um atacante quais usernames existem.
        """
        usuario = self._repositorio.buscar(username)
        if usuario is None:
            raise CredenciaisInvalidasError(MSG_CREDENCIAIS_INVALIDAS)
        if usuario.bloqueado:
            raise ContaBloqueadaError(
                f"RN05: conta '{username}' bloqueada após "
                f"{LIMITE_TENTATIVAS} tentativas falhas."
            )
        if self._senha_confere(usuario, senha):
            self._registrar_sucesso(usuario)
            return True
        self._registrar_falha(usuario)
        raise CredenciaisInvalidasError(MSG_CREDENCIAIS_INVALIDAS)

    @staticmethod
    def _senha_confere(usuario: Usuario, senha: str) -> bool:
        # compare_digest evita ataques de tempo (timing attacks).
        return hmac.compare_digest(gerar_hash_senha(senha, usuario.sal), usuario.senha_hash)

    def _registrar_sucesso(self, usuario: Usuario) -> None:
        usuario.tentativas_falhas = 0
        self._repositorio.salvar(usuario)

    def _registrar_falha(self, usuario: Usuario) -> None:
        usuario.tentativas_falhas += 1
        if usuario.tentativas_falhas >= LIMITE_TENTATIVAS:
            usuario.bloqueado = True
        self._repositorio.salvar(usuario)
