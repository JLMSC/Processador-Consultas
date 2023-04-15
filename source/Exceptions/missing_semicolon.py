"""Arquivo responsável pela criação de exceções customizadas,
bem como métodos responsáveis pelo lançamento de cada uma.
"""

class MissingSemiColonAtEnd(Exception):
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
    raise MissingSemiColonAtEnd(
        f"[{sql_command}]\nO comando SQL fornecido não possui ';' no final."
    )
