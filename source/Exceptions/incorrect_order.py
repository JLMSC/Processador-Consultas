"""Arquivo responsável pela exceção relacionada ao
posicionamento incorreto das cláusulas SQL.
"""

class IncorrectClauseOrderException(Exception):
    """Exceção lançada quando o posicionamento de
    uma ou mais cláusulas SQL estão incorretas.
    """

def raise_incorrect_clause_order_exception(sql_command: str) -> None:
    """Lança uma exceção quando o posicionamento
    de uma ou mais cláusulas SQL estão incorretos.

    Args:
        sql_command (str): O comando SQL usado para
        verificação e validação.

    Raises:
        IncorrectClauseOrderException: Exceção customizada
        para alertar o posicionamento incorreto de uma ou
        mais cláusulas SQL.
    """
    raise IncorrectClauseOrderException(
        sql_command +
        "\nAs cláusulas do comando SQL fornecido não " +
        "estão estruturados corretamente."
    )
