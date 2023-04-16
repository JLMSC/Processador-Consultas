"""Arquivo responsável pela exceção relacionada a falta
de parâmetros na cláusula SELECT."""

class MissingSelectParametersException(Exception):
    """Exceção lançada quando não há parâmetros
    na cláusula SELECT.
    """

def raise_missing_select_params_exception(sql_command: str) -> None:
    """Lança uma exceção quando não há parâmetros
    na cláusula SELECT.

    Args:
        sql_command (str): O comando SQL usado para
        verificação da existência de parâmetros na
        cláusula SELECT.

    Raises:
        MissingSelectParametersException: Exceção 
        customizada para alertar a falta de parâmetros
        na cláusula SELECT.
    """
    raise MissingSelectParametersException(
        sql_command +
        "\nNão há parâmetros para a cláusula SELECT."
    )
