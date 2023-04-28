"""Arquivo responsável pela exceção relacionada a
existencia da utilização de colunas incompatíveis em
uma cláusula SQL.
"""

class ColumnMismatchException(Exception):
    """Exceção lançada quando existe a
    utilização de colunas incompatíveis em
    uma cláusula SQL.
    """

def raise_column_mismatch_in_example_exception(clause: str) -> None:
    """Lança uma exceção quando existe a
    utilização de colunas incompatíveis em
    uma cláusula SQL no contexto de um exemplo
    já existente.

    Args:
        clause (str): O nome da cláusula que contém
        a utilização de colunas incompatíveis.

    Raises:
        ColumnMismatchException: Exceção customizada
        para alertar a utilização de colunas icompatíveis
        em uma cláusula SQL.
    """
    raise ColumnMismatchException(
        f"Alguma coluna usada em '{clause}' no comando SQL fornecido não existe no contexto do banco de dados exemplar."
    )