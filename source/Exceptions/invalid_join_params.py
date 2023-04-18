"""Arquivo responsável pela exceção relacionada a
existência de parâmetros incorretos na cláusula JOIN"""

class InvalidJoinParametersException(Exception):
    """Exceção lançada quando há parâmetros incorretos
    na cláusula JOIN.
    """

def raise_invalid_join_params_exception(sql_command: str) -> None:
    """Lança uma exceção quando há parâmetros incorretos
    na cláusula JOIN.

    Args:
        sql_command (str): O comando SQL usado para
        validação dos parâmetros na cláusula JOIN.

    Raises:
        InvalidJoinParametersException: Exceção
        customizada para alertar a existência de
        parâmetros incorretos na cláusula JOIN.
    """
    raise InvalidJoinParametersException(
        sql_command +
        "\nOs parâmetros na cláusula JOIN estão incorretos."
    )
