"""Modelos de dados (dataclasses) do módulo de autenticação."""
from dataclasses import dataclass


@dataclass
class Usuario:
    username: str
    senha_hash: str
    sal: str
    tentativas_falhas: int = 0
    bloqueado: bool = False
