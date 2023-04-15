from Parser.parser import Parser

# TODO: Inserir mais casos de teste. (Botar em um Loop)
Parser(
    "SELECT * " +
    "FROM tabela1 " +
    "JOIN tabela2 ON tabela1.id = tabela2.id " +
    "JOIN tabela3 ON tabela2.id = tabela3.id " +
    "JOIN tabela4 ON tabela3.id = tabela4.id;"
)