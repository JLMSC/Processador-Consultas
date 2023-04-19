"""Arquivo responsável pela exceção relacionada a
falta de uma condicional em alguma cláusula do
comando SQL fornecido.."""

class MissingStatementException(Exception):
    """Exceção lançada quando não há uma condicional
    em alguma cláusula do comando SQL fornecido..
    """

def raise_missing_statement_exception(clause: str) -> None:
    """Lança uma exceção quando nenhuma condicional
    é fornecida para alguma cláusula do comando SQL
    fornecido.

    Args:
        clause (str) - A cláusula SQL que não possui
        uma condicional.

    Raises:
        MissingCommandException: Exceção customizada
        para alertar a falta de um comando SQL.
    """
    raise MissingStatementException(
        f"Nenhum condicional foi informada na cláusula '{clause}'."
    )
