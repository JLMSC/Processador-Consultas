"""Arquivo responsável pela exceção relacionada a
existência de parâmetros incorretos na cláusula FROM"""

class InvalidFromParametersException(Exception):
    """Exceção lançada quando há parâmetros incorretos
    na cláusula FROM.
    """

def raise_invalid_from_params_exception(sql_command: str) -> None:
    """Lança uma exceção quando há parâmetros incorretos
    na cláusula FROM.

    Args:
        sql_command (str): O comando SQL usado para
        validação dos parâmetros na cláusula FROM.

    Raises:
        InvalidFromParametersException: Exceção
        customizada para alertar a existência de
        parâmetros incorretos na cláusula FROM.
    """
    raise InvalidFromParametersException(
        sql_command +
        "\nOs parâmetros na cláusula FROM estão incorretos."
    )
