"""Arquivo responsável pela exceção relacionada ao
conflito de tabelas em uma condicional (tabelas iguais).
"""

class ConflictingTableException(Exception):
    """Exceção lançada quando há conflito de tabelas
    em uma condicional.
    """

def raise_conflicting_table_exception(statement: str) -> None:
    """Lança uma exceção quando há conflito de
    tabelas em uma condicional.

    Args:
        statement (str): A condicional usada em alguma
        cláusula do comando SQL fornecido.

    Raises:
        ConflictingTableException: Exceção customizada
        para alertar a existência de conflito de
        tabelas em uma condicional.
    """
    raise ConflictingTableException(
        statement +
        "\nAs tabelas, na condicional fornecida, não podem ser iguais."
    )
