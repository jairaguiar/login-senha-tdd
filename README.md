# Cadastro e login de usuários com regras de senha

Trabalho de **Testes de Software** (IFPR – Campus Pinhais), Aproveitamento de
Conhecimentos. Aluno: **Jair Rosa de Aguiar Neto**. Prof.: Gerson Peres.

## Regras de negócio

| ID | Regra |
|---|---|
| RN01 | Username com 4 a 15 caracteres, apenas letras sem acento, dígitos e `_`. |
| RN02 | Senha com 8 a 20 caracteres (inclusive). |
| RN03 | Senha com ao menos 1 letra maiúscula, 1 dígito e 1 caractere especial. |
| RN04 | Username único: o cadastro é recusado se já existir no repositório. |
| RN05 | A 3ª tentativa de login falha consecutiva bloqueia a conta; login correto zera o contador. |
| RN06 | A senha não pode conter o username (sem diferenciar maiúsculas). |

Toda violação lança uma subclasse de `RegraNegocioError`.

## Estrutura

```
src/autenticacao/
  excecoes.py     exceções de regra de negócio
  modelos.py      dataclass Usuario
  validadores.py  uma função pura por regra (RN01, RN02, RN03, RN06)
  repositorio.py  Protocol do repositório + implementação em memória
  servico.py      ServicoAutenticacao (repositório injetado): cadastrar() e login()
tests/
  test_validadores.py    particionamento de equivalência e valor-limite
  test_tabela_decisao.py tabela de decisão da RN03 (8 combinações)
  test_servico.py        serviço com o repositório substituído por Mock
  test_integracao.py     serviço + repositório em memória
```

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                                                     # suíte completa
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

## TDD

Os ciclos Red-Green-Refactor estão no histórico (`git log --oneline`), com
commits `test(red)`, `feat(green)` e `refactor` para cada ciclo.

## Defeitos propositais

A branch `defeitos` contém os 2 defeitos introduzidos de propósito para a
Parte 4 do trabalho. A `main` permanece sem defeitos.
