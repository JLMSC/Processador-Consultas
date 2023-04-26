"""Arquivo responsável pela exceção relacionada a
invalidez de uma instância da classe Parser.
"""

class InvalidParserException(Exception):
    """Exceção lançada quando a instância da
    classe Parser é inválida (não foi inicializada).
    """

def raise_invalid_parser_exception(where: str) -> None:
    """Lança uma exceção quando a instância da
    classe Parser é inválida (não foi inicializada.)

    Args:
        where (str): Onde, o local em que a classe
        Parser não foi inicializada corretamente.

    Raises:
        InvalidParserException: Exceção customizada
        para alertar a invalidez de uma instância da
        classe Parser.
    """
    raise InvalidParserException(
        f"A classe Parser não foi inicializada em '{where}'"
    )