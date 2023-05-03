"""Arquivo responsável pela conversão de um comando
SQL para sua expressão em Álgebra Relacional já otimizada."""

import re
from functools import reduce
from typing import Dict, List
from collections import OrderedDict

# pylint: disable=import-error
import Exceptions
from Parser.parser import Parser

class Converter:
    """Classe responsável pela conversão de um comando SQL
    para Álgebra Relacional.
    
    Após a validação e verificação, realizada pelo Parser,
    esta classe percorre cada elemento textual com o objetivo
    de transformar cada cláusula SQL em sua representação, em
    Álgebra Relacional.
    """

    # O Parser.
    __parser: Parser
    # A Álgebra Relaciona de algum comando SQL.
    __relational_algebra: str
    # Informações sobre as tabelas e colunas do comando SQL.
    __command_info: Dict[str, Dict[str, str]]

    @property
    def parser(self) -> Parser:
        """Extrai o conteúdo da variável privada parser.

        Acessa a variável privada da classe, responsável
        pela instância da classe Parser, retornando a
        instância da classe.

        Returns:
            Parser: Uma instância da classe Parser.
        """
        return self.__parser

    @parser.setter
    def parser(self, new_parser: Parser) -> None:
        """Altera o conteúdo da variável privada parser.

        Acessa a variável privada da classe, responsável
        pela instância da classe Parser, atribuindo uma
        nova instância de Parser para a variável.

        Args:
            new_parser (Parser): Uma nova instância da classe
            Parser.
        """
        self.__parser = new_parser

    @property
    def relational_algebra(self) -> str:
        """Extrai o conteúdo da variável privada relational_algebra.

        Acessa a variável privada da classe, responsável pelo
        armazenamento do comando SQL convertido em álgebra relacional,
        retornando-o seu conteúdo.

        Returns:
            str: A Álgebra Relacional de algum comando SQL.
        """
        return self.__relational_algebra

    @relational_algebra.setter
    def relational_algebra(self, new_algebra: str) -> None:
        """Altera o conteúdo da variável privada relational_algebra.

        Acessa a variável privada da classe, responsável pelo
        armazenamento do comando SQL convertido em álgebra relacional,
        atribuindo uma nova álgebra relacional para a variável.

        Args:
            new_algebra (str): Uma nova Álgebra Relacional de algum comando SQL.
        """
        self.__relational_algebra = new_algebra

    @property
    def command_info(self) -> Dict[str, Dict[str, str]]:
        """Extrai o conteúdo da variável privada command_info.

        Acessa a variável privada da classe, responsável pelo
        armazenamento de informações sobre uma determinada
        tabela de um comando SQL, otimizando-o sua representação
        em Álgebra Relacional.

        Returns:
            Dict[str, Dict[str, str]]: As tabelas usadas no comando
            SQL algumas informações otimizadas para a representação
            em Álgebra Relacional.
        """
        return self.__command_info

    @command_info.setter
    def command_info(self, new_info: Dict[str, Dict[str, str]]) -> None:
        """Altera o conteúdo da variável privada command_info.

        Acessa a variável privada da classe, responsável pelo
        armazenamento de informações sobre uma determinada tabela
        de um comando SQL, atribuindo novas informações para a
        variável.

        Args:
            new_info (Dict[str, str]): Um novo dicionário com
            novas informações para a variável.
        """
        self.__command_info = new_info

    def __init__(self, parser: Parser | type) -> None:
        """Construtor da classe.

        Atribui valores a algumas variáveis e realiza
        a conversão de SQL para Álgebra Relaciona.

        Args:
            parser (Parser | type): Uma instância da classe Parser.
        """
        if isinstance(parser, Parser):
            self.parser = parser
            self.command_info = OrderedDict()
        else:
            Exceptions.raise_invalid_parser_exception("Converter.py (__init__)")

    def convert_in_database_context(self, database: Dict[str, List[str]]) -> str:
        """Converte um comando SQL (relacionado ao Banco de Dados Exemplar) para
        a sua representação em Álgebra Relacional.

        Itera sobre nome de tabelas e colunas, separando conforme necessário,
        para que, durante a criação da Álgebra Relacional, o mesmo já esteja
        otimizado.
        Etapas da otimização:
        a. Aplicar primeiro as operações que reduzem o tamanho dos resultados
        intermediários. i. Operações de seleção; ii. Operações de projeção.
        b. Aplicar primeiro as operações de seleção e de junção mais restritivas.
        i. Reordenar os nós folha da árvore de consulta; ii. Evitar a operação
        de produto cartesiano; iii. Ajustar o restante da árvore de forma apropriada.

        Args:
            database (Dict[str, List[str]]): Um dicionário contendo o nome
            das tabelas (chaves) e uma lista com as colunas da tabela (valor).

        Veja '/source/Examples' para mais detalhes sobre a estrutura de 'database'.

        Returns:
            str: A Álgebra Relacional do comando SQL.
        """

        def make_projection() -> None:
            """Identifica as tabelas de cada coluna usada no comando SQL,
            adicionando-a à tabela correspondente em 'command_info'.
            """
            for token, columns in self.parser.sql_columns.items():
                if token in ["SELECT", "ON", "WHERE"]:
                    for column_name in columns:
                        if column_name != "*":
                            column_name = column_name.lower()
                            target_table: str | None = search_table_in_database(column_name)
                            if target_table is not None:
                                if column_name not in self.command_info[target_table]['projection']:
                                    self.command_info[target_table]['projection'] += f"{column_name} "
                            else:
                                Exceptions.raise_column_mismatch_in_example_exception(column_name)

        def convert_on2ra() -> None:
            """Converte os parâmetros do ON, do JOIN, para Álgebra Relacional.
            """
            table_index: int = -1
            for token_info, params in zip(self.parser.sql_tokens, self.parser.sql_params):
                (token, _) = token_info
                token = token.upper()

                if token == "JOIN":
                    table_index += 1
                elif token == "ON":
                    self.command_info[sql_context_tables[table_index]]['junction'] += f"{params} "
                elif token.endswith("_ON"):
                    self.command_info[sql_context_tables[table_index]]['junction'] += f"{token.replace('_ON', '', 1)} {params} "

        def convert_where2ra() -> None:
            """Converte os parâmetros do WHERE para Álgebra Relacional.
            """
            for token_info, params in zip(self.parser.sql_tokens, self.parser.sql_params):
                (token, _) = token_info
                token = token.upper()

                # Converte somente os tokens que possuem o sufixo "WHERE",
                # usando regex para identificar os parâmetros do 'WHERE' que
                # possuem, explicitamente, o nome de uma tabela ou não.
                if token.endswith("WHERE"):
                    regex_where = r'\b(?<![\'"])([a-zA-Z]\w+\.[a-zA-Z]\w+)(?![\'"])\b|\b(?<![\'"])([a-zA-Z]\w+)(?![\'"])\b'
                    if (matches := re.match(regex_where, params, re.IGNORECASE)) is not None:
                        match = matches.groups()
                        # Verifica se o nome da tabela está explicito.
                        if match[0]:
                            self.command_info[match[0].split(".")[0]]['restriction'] += f"{params} "
                        # Procura pela tabela.
                        else:
                            column_name: str = match[1].lower()
                            if column_name != "*":
                                target_table: str = search_table_in_database(column_name)
                                # Ignora duplicatas.
                                if column_name not in self.command_info[target_table]['restriction']:
                                    if token.endswith("_WHERE"):
                                        self.command_info[target_table]['restriction'] += f"{token.replace('_WHERE', '', 1)} {params} "
                                    else:
                                        self.command_info[target_table]['restriction'] += f"{params} "

        def search_table_in_database(target_column: str) -> str:
            """Procura pelo nome da tabela correspondente de uma coluna.

            Itera sobre todas as tabelas de 'database' e verifica se a
            coluna a qual não possui o nome da tabela explicita, está
            incluída na lista.

            'database' é a mesma variável usada em 'convert_in_database_context'.

            Args:
                target_column (str): A coluna pela qual se deseja saber
                o nome da tabela correspondente.

            Returns:
                str: Retorna o nome da tabela, caso seja encontrada.
            
            Raises:
                ColumnMismatchException: Exceção customizada
                para alertar a utilização de colunas icompatíveis
                em uma cláusula SQL.
            """
            # Itera sobre as tabelas e colunas do banco de dados exemplar.
            for example_table, example_columns in database.items():
                # Procura somente nas tabelas que foram usadas pelo comando SQL.
                if example_table in self.command_info.keys():
                    # Retorna o nome da tabela, caso encontre a coluna correspondente..
                    if target_column in example_columns:
                        return example_table
            Exceptions.raise_column_mismatch_in_example_exception(target_column)

        def mount_ra() -> str:
            """Monta a Álgebra Relacional.

            Pega as informações convertidas e armazenadas em 'command_info'
            e monta a Álgebra Relacional na ordem esperada.

            Returns:
                str: A Álgebra Relacional montada.
            """

            def cross_join(*expressions: str) -> str:
                """Recebe qualquer quantia de expressões, de uma Álgebra Relacional,
                e junta-as no formato '((exp1exp2) ... exp3) ...', basicamente
                adiciona um parênteses extra em duas expressões.

                Returns:
                    str: As expressões com um novo conjunto de parênteses.
                """
                return reduce(lambda exp1, exp2: f"({exp1.strip()}{exp2.strip()})", expressions)

            relational_algebra: str = ''
            for table in sql_context_tables:
                # Extrai as variáveis de 'command_info'.
                table_projection: str = self.command_info[table]['projection'].strip()
                table_restriction: str = self.command_info[table]['restriction'].strip()
                table_junction: str = self.command_info[table]['junction'].strip()

                # Reorganiza as variáveis para Álgebra Relacional.
                table_projection = f"(π {table_projection.replace(' ', ', ')} " if bool(table_projection) else ""
                table_restriction = f"(σ {table_restriction.replace('AND', '', 1).strip()} " if bool(table_restriction) else ""
                table_junction = f"@jn |x| {table_junction}" if bool(table_junction) else ""

                # Junta tudo, organizando a qntd. de parênteses.
                converted2ra: str = f"{table_projection}{table_restriction}({table}"
                relational_algebra += f"{converted2ra}{')' * converted2ra.count('(')} {table_junction} "

            # Tira os espaços em brancos incorretos.
            relational_algebra = relational_algebra.strip()

            # Arruma os parênteses usando o reduce.
            if '@jn' in relational_algebra: # '@jn' é um placeholder.
                relational_algebra = f"{cross_join(*relational_algebra.split('@jn')).replace('|x|', ' |x|')}"

            return relational_algebra

        # Cria um dicionário para a Álgebra Relacional do comando SQL, 
        # incluindo informações já otimizadas conforme descrito previamente.
        sql_context_tables: List[str] = self.parser.sql_tables["FROM"] + self.parser.sql_tables["JOIN"]
        for table in sql_context_tables:
            self.command_info.update({
                table: {
                    "projection": "",
                    "restriction": "",
                    "junction": ""
                }
            })

        # Cria a projeção para as tabelas.
        make_projection()

        # Cria a junção para as tabelas.
        convert_on2ra()

        # Cria a restrição para as tabelas.
        convert_where2ra()

        # Estrutura a Álgebra Relacional.
        select_params: str = self.parser.sql_params[0]
        select2ra: str = f"π {select_params}" if select_params != '*' else ""
        self.relational_algebra = f"{select2ra} {mount_ra()}".strip()

        # TODO: Montar uma árvore com base em 'self.command_info'

        return self.relational_algebra