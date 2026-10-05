"""Funções puras de validação: uma função por regra de negócio."""
import string

from autenticacao.excecoes import SenhaFracaError, SenhaInvalidaError

SENHA_TAMANHO_MIN = 8
SENHA_TAMANHO_MAX = 20
CARACTERES_ESPECIAIS = frozenset(string.punctuation)


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


def validar_forca_senha(senha: str) -> None:
    """RN03 – a senha deve ter ao menos 1 maiúscula, 1 dígito e 1 especial.

    As três condições são combinadas com E lógico: basta uma falhar para a
    senha ser rejeitada (ver tabela de decisão no relatório, seção 4.3).
    """
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_digito = any(c.isdigit() for c in senha)
    tem_especial = any(c in CARACTERES_ESPECIAIS for c in senha)

    if not (tem_maiuscula and tem_digito and tem_especial):
        faltando = [
            nome
            for nome, presente in (
                ("letra maiúscula", tem_maiuscula),
                ("dígito", tem_digito),
                ("caractere especial", tem_especial),
            )
            if not presente
        ]
        raise SenhaFracaError(f"RN03: a senha precisa de {', '.join(faltando)}.")
