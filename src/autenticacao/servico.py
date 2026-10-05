import hashlib
import os

from autenticacao.excecoes import UsuarioJaExisteError
from autenticacao.modelos import Usuario
from autenticacao.validadores import validar_forca_senha, validar_tamanho_senha


class ServicoAutenticacao:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def cadastrar(self, username, senha):
        validar_tamanho_senha(senha)
        validar_forca_senha(senha)
        if self.repositorio.existe(username):
            raise UsuarioJaExisteError("já existe")
        sal = os.urandom(16).hex()
        senha_hash = hashlib.sha256((sal + senha).encode()).hexdigest()
        usuario = Usuario(username, senha_hash, sal)
        self.repositorio.salvar(usuario)
        return usuario
