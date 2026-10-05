from dataclasses import dataclass


@dataclass
class Usuario:
    username: str
    senha_hash: str
    sal: str
