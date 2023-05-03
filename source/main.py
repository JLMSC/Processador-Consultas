"""Arquivo principal.
"""
import Examples

# pylint: disable=import-error
from Parser.parser import Parser
from RelationalAlgebra.Converter import Converter

ph = Parser(
    "SELECT nome, datanascimento, descricao, saldoinicial " +
    "FROM usuario " +
    "JOIN contas ON usuario.idusuario = contas.usuario_idusuario " +
    "WHERE saldoinicial >= 235 AND uf = 'ce' AND cep <> '62930000' " +
    "JOIN movimentacao ON usuario.idUsuario = movimentacao.idmovimentacao;"
)
ph.check_database_compatibility(database=Examples.pagamento_example_db)

cnv = Converter(ph)
print(cnv.convert_in_database_context(Examples.pagamento_example_db))
