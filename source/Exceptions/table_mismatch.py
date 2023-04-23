"""Arquivo responsável pela exceção relacionada a
existencia da utilização de tabelas incompatíveis em
uma cláusula SQL.
"""

class TableMismatchException(Exception):
    """Exceção lançada quando existe a
    utilização de tabelas incompatíveis em
    uma cláusula SQL.
    """

def raise_table_mismatch_exception(clause: str) -> None:
    """Lança uma exceção quando existe a
    utilização de tabelas incompatíveis em
    uma cláusula SQL.

    Args:
        clause (str): O nome da cláusula que contém
        a utilização de tabelas incompatíveis.

    Raises:
        TableMismatchException: Exceção customizada
        para alertar a utilização de tabelas icompatíveis
        em uma cláusula SQL.
    """
    raise TableMismatchException(
        f"Alguma tabela usada em '{clause}' não existe no contexto do comando SQL fornecido."
    )
