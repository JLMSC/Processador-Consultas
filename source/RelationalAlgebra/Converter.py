"""Arquivo responsável pela conversão de um comando
SQL para sua expressão em Álgebra Relacional já otimizada."""

import re
from typing import Dict, List, Set

from Parser.parser import Parser

# pylint: disable=import-error
import Exceptions

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
            self.command_info = {}
            self.__convert_from_example()
        else:
            Exceptions.raise_invalid_parser_exception("Converter.py (__init__)")

    def __convert_from_example(self) -> str:
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

        Returns:
            str: A Álgebra Relacional do comando SQL.
        """

        # TODO: Doc
        def search_table_in_example_db(target_column: str) -> str | None:
            # Itera sobre as tabelas e colunas do banco de dados exemplar.
            for example_table, example_columns in example.items():
                # Verifica se a tabela existe no contexto do comando SQL fornecido.
                if example_table in self.command_info.keys():
                    # Retorna o nome da tabela, caso encontre.
                    if target_column in example_columns:
                        return target_column
            return None

        # TODO: variável da classe? ou botar no parser?
        # O banco de dados exemplo utilizado está em "/examples_db/example_01.png"
        example: Dict[str, List[str]] = {
            "usuario": [
                "idusuario", "nome", "logradouro", "número",
                "bairro", "cep", "uf", "datanascimento"
            ],
            "contas": [
                "idconta", "descricao", "tipoconta_idtipoconta",
                "usuario_idusuario", "saldoinicial"
            ],
            "movimentacao": [
                "idmovimentacao", "datamovimentacao", "descricao",
                "tipomovimento_idtipomovimento", "categoria_idcategoria",
                "contas_idconta", "valor"
            ],
            "tipomovimentacao": [
                "idtipomovimentacao", "descmovimentacao"
            ],
            "categoria": [
                "idcategoria", "desccategoria"
            ],
            "tipoconta": [
                "idtipoconta", "descrição"
            ]
        }

        # Cria um dicionário para a Álgebra Relacional do comando SQL,
        # incluindo informações já otimizadas conforme descrito previamente.
        sql_context_tables: Set[str] = self.parser.sql_tables['FROM'].union(self.parser.sql_tables['JOIN'])
        for table in sql_context_tables:
            self.command_info.update({
                table: {
                    "projection": "",
                    "restriction": "",
                    "junction": ""
                }
            })

        # Itera sobre os tokens do comando SQL e as colunas usadas no comando.
        for token, columns in self.parser.sql_columns.items():
            # Adiciona as colunas à 'Projeção' da Álgebra Relacional do comando SQL.
            if token in ["SELECT", "ON", "WHERE"]:
                for column_name in columns:
                    # Suporte para '[a-zA-Z]'
                    column_name = column_name.lower()
                    # Pega o nome da tabela correspondente a cada coluna, iterada, do comando SQL.
                    target_table = search_table_in_example_db(column_name)
                    # Verifica se a tabela foi encontrada.
                    if target_table is not None:
                        # Ignora duplicatas.
                        if column_name not in self.command_info[target_table]['projection']:
                            self.command_info[target_table]['projection'] += f"{column_name} "
                            break

        # FIXME: Refatorar
        # Itera sobre as cláusulas do comando SQL e seus parâmetros.
        for token_info, params in zip(self.parser.sql_tokens, self.parser.sql_params):
            # Extrai o nóme da cláusula, ignorando a posição e suportano '[a-zA-Z]'.
            (token, _) = token_info
            token = token.upper()
            # FIXME: Refatorar os IF/ELSE token.endswith(...)
            # Adiciona as restrições da 'Junção' entre duas tabelas da Álgebra Relacional do comando SQL.
            if token.endswith('ON'):
                # Usa regex para identificar os parâmetros do 'ON' que possuem
                # o nome da tabela explicito ou não.
                if (matches := re.match(r'(\w+\.\w+)|(\w+|\*)', params, re.IGNORECASE)) is not None:
                    match = matches.groups()
                    if match[0]:
                        self.command_info[match[0].split(".")[0]]['junction'] += f"{params} "
                    # Procura pela tabela correspondente.
                    else:
                        for example_table, example_columns in example.items():
                            if example_table in self.command_info.keys():
                                if match[1] not in self.command_info[example_table]['junction']:
                                    if match[1] in example_columns:
                                        self.command_info[example_table]['junction'] += f"{params} "
                                        break
            # Adiciona as restirções da 'Seleção' na Álgebra Relacional do comando SQL.
            elif token.endswith('WHERE'):
                # Usa regex para identificar os parâmetros do 'WHERE' que possuem
                # o nome da tabela explicito ou não.
                regex_where = r'\b(?<![\'"])([a-zA-Z]\w+\.[a-zA-Z]\w+)(?![\'"])\b|\b(?<![\'"])([a-zA-Z]\w+)(?![\'"])\b'
                if (matches := re.match(regex_where, params, re.IGNORECASE)) is not None:
                    match = matches.groups()
                    if match[0]:
                        self.command_info[match[0].split(".")[0]]['restriction'] += f"{params} "
                    # Procura pela tabela correspondente.
                    else:
                        for example_table, example_columns in example.items():
                            if example_table in self.command_info.keys():
                                if match[1] not in self.command_info[example_table]['restriction']:
                                    if match[1] in example_columns:
                                        self.command_info[example_table]['restriction'] += f"{token.replace('_WHERE', '')} {params} " if token.endswith("_WHERE") else f"{params} "
                                        break

        # TODO: Montar a Álgebra Relacional.
        # TODO: Montar uma árvore com base em 'self.command_info'
        # TODO: Retornar a Álgebra Relacional.

        self.relational_algebra = ""
        return self.relational_algebra