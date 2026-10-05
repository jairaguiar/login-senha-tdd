from autenticacao.excecoes import SenhaInvalidaError


def validar_tamanho_senha(senha):
    if len(senha) < 8:
        raise SenhaInvalidaError("senha curta")
    if len(senha) > 20:
        raise SenhaInvalidaError("senha longa")
