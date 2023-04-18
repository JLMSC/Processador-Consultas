"""Arquivo responsável pela exceção relacionada ao
uso de uma ou mais tabelas incompatíveis no comando SQL.
"""

class TableMismatchException(Exception):
    """Exceção lançada quando existe uma ou 
    mais tabelas incompatíveis no comando SQL.
    """

def raise_table_mismatch_exception() -> None:
    """Lança uma exceção quando existe uma ou
    mais tabelas incompatíveis no comando SQL.

    Raises:
        TableMismatchException: Exceção customizada
        para alertar a existência de uma ou mais
        tabelas incompatíveis no comando SQL.
    """
    raise TableMismatchException(
        "Existe uma ou mais tabelas incompatíveis no comando SQL fornecido."
    )
