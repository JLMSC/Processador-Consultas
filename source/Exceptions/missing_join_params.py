"""Arquivo responsável pela exceção relacionada a fatal
de parâmetros da cláusula JOIN."""

class MissingJoinParametersException(Exception):
    """Exceção lançada quando não há parâmetros
    na cláusula JOIN.
    """

def raise_missing_join_params_exception(sql_command: str) -> None:
    """Lança uma exceção quando não há parâmetros
    na cláusula JOIN.

    Args:
        sql_command (str): O comando SQL usado para
        verificação da existência de parâmetros na
        cláusula JOIN.

    Raises:
        MissingJoinParametersException: Exceção
        customizada para alertar a falta de parâmetros
        na cláusula JOIN.
    """
    raise MissingJoinParametersException(
        sql_command +
        "\nNão há parâmetros para a cláusula JOIN."
    )
