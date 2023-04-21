"""Arquivo responsável pela exceção relacionada a
existência de parâmetros incorretos em uma condicional
"""

class InvalidStatementParametersException(Exception):
    """Exceção lançada quando há parâmetros incorretos
    em uma condicional.
    """

def raise_invalid_statement_params_exception(statement: str) -> None:
    """Lança uma exceção quando há parâmetros incorretos
    em uma condicional.

    Args:
        statement (str): A condicional usada por alguma
        cláusula no comando SQL fornecido.

    Raises:
        InvalidStatementParametersException: Exceção
        customizada para alertar a existência de
        parâmetros incorretos em uma condicional.
    """
    raise InvalidStatementParametersException(
        statement +
        "\nA condicional fornecida é inválida."
    )
