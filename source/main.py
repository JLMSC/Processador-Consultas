from Parser.parser import Parser

Parser(
    "SELECT * " +
    "FROM tabela1 " +
    "JOIN tabela5 ON id = id " +
    "JOIN tabela2 ON tabela1.id = tabela2.id AND tabela1.id = tabela2.id IN ('valor1', 'valor2') " +
    "JOIN tabela3 ON tabela2.id = tabela3.id IN (SELECT * FROM tabela1) " +
    "JOIN tabela4 ON tabela3.id = tabela4.id AND tabela1.id > 10 " +
    "WHERE tabela1.id = tabela2.id AND tabela1.id = tabela2.id " +
    "WHERE tabela2.id = tabela3.id AND tabela1.id > 30;"
)