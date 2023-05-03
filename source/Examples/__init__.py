"""Arquivo responsável pela junção de todos os bancos
de dados exemplares."""

# pylint: disable=import-error
from .Pagamento.example_db import pagamento_example_db

# Indica o que, neste pacote, está disponível para uso.
__all__ = [
    'pagamento_example_db'
]