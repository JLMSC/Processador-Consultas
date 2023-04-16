"""Arquivo responsável pela exceção relacionada a
existência de parâmetros incorretos na cláusula SELECT"""

class InvalidSelectParametersException(Exception):
    """Exceção lançada quando há parâmetros incorretos
    na cláusula SELECT.
    """

def raise_invalid_select_params(sql_command: str) -> None:
    """Lança uma exceção quando há parâmetros incorretos
    na cláusula SELECT.

    Args:
        sql_command (str): O comando SQL usado para
        validação dos parâmetros na cláusula SELECT.

    Raises:
        MissingSelectParametersException: Exceção 
        customizada para alertar a existência de 
        parâmetros incorretos na cláusula SELECT.
    """
    raise InvalidSelectParametersException(
        sql_command +
        "\nOs parâmetros na cláusula SELECT estão incorretos."
    )
