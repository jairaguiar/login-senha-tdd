"""Exceções de regra de negócio do módulo de autenticação.

Todas herdam de RegraNegocioError, o que permite ao chamador tratar qualquer
violação de regra de forma genérica ou específica.
"""


class RegraNegocioError(Exception):
    """Base para qualquer violação de regra de negócio."""


class SenhaInvalidaError(RegraNegocioError):
    """RN02 – tamanho da senha fora da faixa permitida."""
