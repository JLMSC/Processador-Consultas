"""Arquivo responsável pela exceção relacionada a fatal
de parâmetros da cláusula FROM."""

class MissingFromParametersException(Exception):
    """Exceção lançada quando não há parâmetros
    na cláusula FROM.
    """

def raise_missing_from_params_exception(sql_command: str) -> None:
    """Lança uma exceção quando não há parâmetros
    na cláusula FROM.

    Args:
        sql_command (str): O comando SQL usado para
        verificação da existência de parâmetros na
        cláusula FROM.

    Raises:
        MissingFromParametersException: Exceção
        customizada para alertar a falta de parâmetros
        na cláusula FROM.
    """
    raise MissingFromParametersException(
        sql_command +
        "\nNão há parâmetros para a cláusula FROM."
    )
