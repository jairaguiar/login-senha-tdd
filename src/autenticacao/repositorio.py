"""Contrato do repositório de usuários (dependência externa do serviço).

Em produção seria um banco de dados; nos testes unitários é substituído por um
Mock, e nos testes de integração pela implementação em memória abaixo.
"""
from typing import Optional, Protocol

from autenticacao.modelos import Usuario


class RepositorioUsuarios(Protocol):
    def existe(self, username: str) -> bool: ...
    def buscar(self, username: str) -> Optional[Usuario]: ...
    def salvar(self, usuario: Usuario) -> None: ...
