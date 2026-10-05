"""Contrato do repositório de usuários (dependência externa do serviço).

Em produção seria um banco de dados; nos testes unitários é substituído por um
Mock, e nos testes de integração pela implementação em memória abaixo.
"""
from typing import Dict, Optional, Protocol

from autenticacao.modelos import Usuario


class RepositorioUsuarios(Protocol):
    def existe(self, username: str) -> bool: ...
    def buscar(self, username: str) -> Optional[Usuario]: ...
    def salvar(self, usuario: Usuario) -> None: ...


class RepositorioEmMemoria:
    """Implementação simples (dicionário) usada nos testes de integração."""

    def __init__(self) -> None:
        self._dados: Dict[str, Usuario] = {}

    def existe(self, username: str) -> bool:
        return username in self._dados

    def buscar(self, username: str) -> Optional[Usuario]:
        return self._dados.get(username)

    def salvar(self, usuario: Usuario) -> None:
        self._dados[usuario.username] = usuario
