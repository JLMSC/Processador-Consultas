"""Arquivo responsável pela exceção relacionada a
falta de um comando SQL."""

class MissingCommandException(Exception):
    """Exceção lançada quando não há um comando SQL.
    """

def raise_missing_command_exception() -> None:
    """Lança uma exceção quando nenhum comando SQL
    é fornecido.

    Raises:
        MissingCommandException: Exceção customizada
        para alertar a falta de um comando SQL.
    """
    raise MissingCommandException(
        "Nenhum comando SQL foi fornecido."
    )
