"""Arquivo responsável pela exceção relacionada a
existencia da utilização de colunas incompatíveis em
uma cláusula SQL.
"""

class ColumnMismatchException(Exception):
    """Exceção lançada quando existe a
    utilização de colunas incompatíveis em
    uma cláusula SQL.
    """

def raise_column_mismatch_in_example_exception(column: str) -> None:
    """Lança uma exceção quando existe a
    utilização de colunas incompatíveis em
    uma cláusula SQL no contexto de um exemplo
    já existente.

    Args:
        column (str): O nome da coluna incompatível.

    Raises:
        ColumnMismatchException: Exceção customizada
        para alertar a utilização de colunas icompatíveis
        em uma cláusula SQL.
    """
    raise ColumnMismatchException(
        f"A coluna {column} não existe no contexto do banco de dados exemplar fornecido."
    )