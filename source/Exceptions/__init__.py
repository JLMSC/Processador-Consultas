"""Arquivo responsável pela junção de todas as exceções
customizadas e, também, a utilização das exceções."""

# pylint: disable=import-error
from .invalid_parser import raise_invalid_parser_exception
from .missing_command import raise_missing_command_exception
from .missing_semicolon import raise_missing_semicolon_exception
from .incorrect_order import raise_incorrect_clause_order_exception
from .missing_from_params import raise_missing_from_params_exception
from .invalid_from_params import raise_invalid_from_params_exception
from .invalid_join_params import raise_invalid_join_params_exception
from .missing_join_params import raise_missing_join_params_exception
from .missing_condition_params import raise_missing_statement_exception
from .column_mismatch import raise_column_mismatch_in_example_exception
from .invalid_select_params import raise_invalid_select_params_exception
from .missing_select_params import raise_missing_select_params_exception
from .invalid_condition_params import raise_invalid_statement_params_exception
from .table_mismatch import raise_table_mismatch_exception, raise_table_mismatch_in_example_exception

# Indica o que, neste pacote, está disponível para uso.
__all__ = [
    'raise_invalid_parser_exception',
    'raise_table_mismatch_exception',
    'raise_missing_command_exception',
    'raise_missing_statement_exception',
    'raise_missing_semicolon_exception',
    'raise_missing_join_params_exception',
    'raise_invalid_join_params_exception',
    'raise_invalid_from_params_exception',
    'raise_missing_from_params_exception',
    'raise_invalid_select_params_exception',
    'raise_missing_select_params_exception',
    'raise_incorrect_clause_order_exception',
    'raise_invalid_statement_params_exception',
    'raise_table_mismatch_in_example_exception',
    'raise_column_mismatch_in_example_exception'
]
