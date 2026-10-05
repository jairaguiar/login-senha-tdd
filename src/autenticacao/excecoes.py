"""Exceções de regra de negócio do módulo de autenticação.

Todas herdam de RegraNegocioError, o que permite ao chamador tratar qualquer
violação de regra de forma genérica ou específica.
"""


class RegraNegocioError(Exception):
    """Base para qualquer violação de regra de negócio."""


class SenhaInvalidaError(RegraNegocioError):
    """RN02 – tamanho da senha fora da faixa permitida."""


class SenhaFracaError(RegraNegocioError):
    """RN03 – senha sem maiúscula, dígito ou caractere especial."""


class UsuarioJaExisteError(RegraNegocioError):
    """RN04 – username já cadastrado."""


class CredenciaisInvalidasError(RegraNegocioError):
    """RN05 – usuário inexistente ou senha incorreta (mensagem única)."""


class ContaBloqueadaError(RegraNegocioError):
    """RN05 – conta bloqueada por excesso de tentativas falhas."""
