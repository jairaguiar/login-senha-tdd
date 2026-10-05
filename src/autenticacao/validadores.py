"""Funções puras de validação: uma função por regra de negócio."""
from autenticacao.excecoes import SenhaInvalidaError

SENHA_TAMANHO_MIN = 8
SENHA_TAMANHO_MAX = 20


def _tamanho_na_faixa(texto: str, minimo: int, maximo: int) -> bool:
    """Retorna True se minimo <= len(texto) <= maximo."""
    return minimo <= len(texto) <= maximo


def validar_tamanho_senha(senha: str) -> None:
    """RN02 – a senha deve ter entre 8 e 20 caracteres (inclusive)."""
    if not _tamanho_na_faixa(senha, SENHA_TAMANHO_MIN, SENHA_TAMANHO_MAX):
        raise SenhaInvalidaError(
            f"RN02: a senha deve ter entre {SENHA_TAMANHO_MIN} e "
            f"{SENHA_TAMANHO_MAX} caracteres (recebido: {len(senha)})."
        )
