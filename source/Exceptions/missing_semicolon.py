"""Arquivo responsável pela exceção relacionada a
falta de ';' no final de comandos SQL."""

class MissingSemicolonException(Exception):
    """Exceção lançada quando não há a presença
    de um ';' no final de um comando SQL.
    """

def raise_missing_semicolon_exception(sql_command: str) -> None:
    """Lança uma exceção quando não há a presença de um
    ';' no final de um comando SQL.

    Args:
        sql_command (str): O comando SQL usado para
        verificação e validação.

    Raises:
        MissingSemiColonAtEnd: Exceção customizada para
        alertar a falta de ';' no final de um comando SQL.
    """
    raise MissingSemicolonException(
        sql_command +
        "\nEstá faltando um ';' no final do comando SQL fornecido."
    )
