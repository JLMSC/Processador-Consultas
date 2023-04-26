"""Arquivo responsável pela validação e verificação de
um comando SQL, bem como as cláusulas utilizadas, a sua
estrutura e, também, os parâmetros."""

import re
from typing import List, Tuple, Dict, Callable, Set

# pylint: disable=import-error
import Exceptions

class Parser:
    """Classe responsável pela verificação e validação de um comando SQL.

    Verifica, a partir de um comando SQL fornecido, se o mesmo é válido
    e se está bem estruturado, retornando, então, uma representação, em
    árvore, do comando SQL.
    """

    # Um comando SQL qualquer.
    __sql_command: str
    # Os tokens, cláusulas SQL, de um comando qualquer.
    __sql_tokens: List[Tuple[str, int]]
    # Os parâmetros associados as cláusulas SQL, de um comando qualquer.
    __sql_params: List[str]
    # As tabelas usadas no comando SQL.
    __sql_tables: Dict[str, Set[str]]
    # As colunas usadas no comando SQL.
    __sql_columns: Dict[str, Set[str]]
    # Expressão regular para extração de palavras reservadas (cláusulas) do MySQL.
    # __sql_token_pattern: str = r'(?<!\()\b(select|from|join|on|where|and|in|not\s+in)\b|(;$)'
    __sql_token_pattern: str = r'(?<!\()\b(select|from|join|on|where|and|in|not\s+in)\b(?!([^()]*\)))|(;$)'
    # Expressão regular para a verificação do posicionamento das cláusulas do MySQL.
    __sql_command_pattern: str = r'^select\sfrom\s(?:join\son\s((and|in|not\sin)\s)*?|where\s((and|in|not\sin)\s)*?)*;$'
    # Expressão regular para validação dos parâmetros da cláusula SELECT do MySQL.
    __sql_select_params_pattern: str = r'\*|^([a-zA-Z]\w*\.)?[a-zA-Z]\w*(,[ ]*([a-zA-Z]\w*\.)?[a-zA-Z]\w*)*$'
    # Expressão regular para validação dos parâmetros da cláusula FROM do MySQL.
    __sql_from_params_pattern: str = r'^[a-zA-Z]\w*(,[ ]*[a-zA-Z]\w*)*$'
    # Expressão regular para validação dos parâmetros da cláusula JOIN do MySQL.
    __sql_join_params_pattern: str = r'^[a-zA-Z]\w*$'
    # Expressão regular para validação dos parâmetros da cláusula ON do MySQL.
    __sql_on_params_pattern: str = r'(?:(^[a-zA-Z]\w*)\.([a-zA-Z]\w*)|([a-zA-Z]\w*))\s(=|>|<|<=|>=|<>)\s(?:([a-zA-Z]\w*)\.([a-zA-Z]\w*)|([a-zA-Z]\w*)|([0-9]+)|(?:\'([a-zA-Z\d]\w*\s*)+\'))$|([a-zA-Z]\w*)$'
    # Expressão regular para validação dos parâmetros da cláusula WHERE do MySQL.
    __sql_where_params_pattern: str = r'(?:(^[a-zA-Z]\w*)\.([a-zA-Z]\w*)|([a-zA-Z]\w*))\s(=|>|<|<=|>=|<>)\s(?:([a-zA-Z]\w*)\.([a-zA-Z]\w*)|([a-zA-Z]\w*)|([0-9]+)|(?:\'([a-zA-Z\d]\w*\s*)+\'))$|([a-zA-Z]\w*)$'
    # Expressão regular para validação dos parâmetros da cláusula IN do MySQL.
    __sql_in_params_pattern: str = r"\(\s*(?:(?:'(?:\\'|[^'])*')|(?:[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)|(?:true|True|false|False)|(?:null|NULL)|(?P<subcommand1>(?:(select|SELECT)\s+.+\s+(from|FROM)\s+.+)))\s*(?:,\s*(?:(?:'(?:\\'|[^'])*')|(?:[0-9]+(?:\.[0-9]+)?(?:e[+-]?[0-9]+)?)|(?:true|True|false|False)|(?:null|NULL)|(?P<subcommand2>(?:(select|SELECT)\s+.+\s+(from|FROM)\s+.+)))\s*)*\)"

    def __init__(self, sql_command: str) -> None:
        """Construtor da classe.

        Atribui valores a algumas variáveis, separa os tokens e realiza
        a validação e verificação do comando SQL fornecido.
        
        Args:
            sql_command (str): Atribui um comando SQL a variável privada.
        """
        self.sql_command = sql_command
        self.__adapt_termination()
        self.sql_tokens = self.__tokenize()
        self.sql_params = self.__extract_params()
        self.__validate_tokens()
        self.__sql_tables = {
            key: set() 
            for key in ["SELECT", "FROM", "JOIN", "ON", "AND_ON", "IN_ON", "NOT IN_ON", "WHERE", "AND_WHERE", "IN_WHERE", "NOT IN_WHERE"]
        }
        self.__sql_columns = {
            key: set()
            for key in ["SELECT", "FROM", "JOIN", "ON", "AND_ON", "IN_ON", "NOT IN_ON", "WHERE", "AND_WHERE", "IN_WHERE", "NOT IN_WHERE"]
        }
        self.__validate_params()
        self.__validate_table_compatibility()

    @property
    def sql_command(self) -> str:
        """Extrai o conteúdo da variável privada sql_command.

        Acessa a variável privada da classe, responsável pelo
        armazenamento do comando SQL, retornando seu conteúdo.

        Returns:
            str: O conteúdo da variável privada da classe.
        """
        return self.__sql_command

    @sql_command.setter
    def sql_command(self, new_sql_command: str) -> None:
        """Altera o conteúdo da variável privada sql_command.

        Acessa a variável privada da classe, responsável pelo
        armazenamento do comando SQL, atribuindo um novo
        valor para a variável.

        Args:
            new_sql_command (str): Um novo comando SQL, em formato
            de string, a ser atribuido a variável privada sql_command.
        """
        self.__sql_command = new_sql_command

    @property
    def sql_tokens(self) -> List[Tuple[str, int]]:
        """Extrai o conteúdo da variável privada sql_tokens.

        Acessa a variável privada da classe, responsável pelo
        armazenamento das cláusulas SQL, bem como as suas
        posições.

        Returns:
            List[Tuple[str, int]]: Uma lista de tuplas, contendo
            os comandos SQL e a posição do comando.
        """
        return self.__sql_tokens

    @sql_tokens.setter
    def sql_tokens(self, new_sql_tokens: List[Tuple[str, int]]) -> None:
        """Altera o conteúdo da variável privada sql_tokens.

        Acessa a variável privada da classe, responsável pelo
        armazenamento das cláusulas SQL, bem como as suas posições,
        atribuindo um novo valor para a variável.

        Args:
            new_sql_tokens (List[Tuple[str, int]]): Uma lista de
            tuplas contendo as cláusulas SQL e suas posições no comando.
        """
        self.__sql_tokens = new_sql_tokens

    @property
    def sql_params(self) -> List[str]:
        """Extrai o conteúdo da variável privada sql_params.

        Acessa a variável privada da classe, responsável pelo
        armazenamento dos parâmetros das cláusulas SQL, retornando
        seu conteúdo.

        Returns:
            List[str]: Uma lista, contendo os parâmetros 
            associados as claúsulas SQL.
        """
        return self.__sql_params

    @sql_params.setter
    def sql_params(self, new_sql_params: List[str]) -> None:
        """Altera o conteúdo da variável privada sql_params.

        Acessa a variável privada da classe, responsável pelo
        armazenamento dos parâmetros das cláusulas SQL, atribuindo
        um novo valor para a variável.

        Args:
            new_sql_params (List[str]): Uma lista contendo os
            parâmetros associados as cláusulas SQL.
        """
        self.__sql_params = new_sql_params

    @property
    def sql_tables(self) -> Dict[str, Set[str]]:
        """Extrai o conteúdo da variável privada sql_tables.

        Acessa a variável privada da classe, responsável pelo
        armazenamento das tabelas utilizadas no comando SQL.

        Returns:
            Dict[str, Set[str]]: O conteúdo da variável privada da classe,
            ou seja, o nome das tabelas.
        """
        return self.__sql_tables

    @sql_tables.setter
    def sql_tables(self, new_sql_tables: Dict[str, Set[str]]) -> None:
        """Altera o conteúdo da variável privada sql_tables.

        Acessa a variável privada da classe, responsável pelo
        armazenamento das tabelas de um comando SQL.

        Args:
            new_sql_tables (Dict[str, Set[str]]): As tabelas utilizadas
            no comando SQL.
        """
        self.sql_tables = new_sql_tables

    @property
    def sql_columns(self) -> Dict[str, Set[str]]:
        """Extrai o conteúdo da variável privada sql_columns.

        Acessa a variável privada da classe, responsável pelo
        armazenamento das colunas utilizadas no comando SQL.

        Returns:
            Dict[str, Set[str]]: O conteúdo da variável privada da classe,
            ou seja, o nome das colunas.
        """
        return self.__sql_columns

    @sql_columns.setter
    def sql_columns(self, new_sql_columns: Dict[str, Set[str]]) -> None:
        """Altera o conteúdo da variável privada sql_columns.

        Acessa a variável privada da classe, responsável pelo
        armazenamento das colunas de um comando SQL.

        Args:
            new_sql_columns (Dict[str, Set[str]]): As colunas
            utilizadas no comando SQL.
        """
        self.sql_columns = new_sql_columns

    @property
    def sql_token_pattern(self) -> str:
        """Extrai o conteúdo da variável privada sql_token_pattern.

        Acessa a variável privada da classe, responsável pelo regex
        da seleção e captura de comandos SQL, bem como o SELECT, FROM,
        JOIN, ON e WHERE, retornando seu conteúdo.

        Returns:
            str: O conteúdo, regex, da variável privada da classe.
        """
        return self.__sql_token_pattern

    @property
    def sql_command_pattern(self) -> str:
        """Extrai o conteúdo da variável privada sql_command_pattern.

        Acessa a variável privada da classe, responsável pelo regex
        da verificação e validação da estrutura e posicionamento das
        cláusulas SQL, retornando seu conteúdo.

        Returns:
            str: O conteúdo, regex, da variável privada da classe.
        """
        return self.__sql_command_pattern

    @property
    def sql_select_params_pattern(self) -> str:
        """Extrai o conteúdo da variável privada sql_select_params_pattern.

        Acessa a variável privada da classe, responsável pelo regex
        da verificação e validação dos parâmetros da cláusula SELECT,
        retornando seu conteúdo.

        Returns:
            str: O conteúdo, regex, da variável privada da classe.
        """
        return self.__sql_select_params_pattern

    @property
    def sql_from_params_pattern(self) -> str:
        """Extrai o conteúdo da variável privada sql_from_params_pattern.

        Acessa a variável privada da classe, responsável pelo regex
        da verificação e validação dos parâmetros da cláusula FROM,
        retornando o seu conteúdo.

        Returns:
            str: O conteúdo, regex, da variável privada da classe.
        """
        return self.__sql_from_params_pattern

    @property
    def sql_join_params_pattern(self) -> str:
        """Extrai o conteúdo da variável privada sql_join_params_pattern.

        Acessa a variável privada da classe, responsável pelo regex
        da verificação e validação dos parâmetros da cláusula JOIN,
        retornando o seu conteúdo.

        Returns:
            str: O conteúdo, regex, da variável privada da classe.
        """
        return self.__sql_join_params_pattern

    @property
    def sql_on_params_pattern(self) -> str:
        """Extrai o conteúdo da variável privada sql_on_params_pattern.

        Acessa a variável privada da classe, responsável pelo regex
        da verificação e validação dos parâmetros da cláusula ON,
        retornando o seu conteúdo.

        Returns:
            str: O conteúdo, regex, da variável privada da classe.
        """
        return self.__sql_on_params_pattern

    @property
    def sql_where_params_pattern(self) -> str:
        """Extrai o conteúdo da variável privada sql_where_params_pattern.

        Acessa a variável privada da classe, responsável pelo regex
        da verificação e validação dos parâmetros da cláusula WHERE,
        retornando o seu conteúdo.

        Returns:
            str: O conteúdo, regex, da variável privada da classe.
        """
        return self.__sql_where_params_pattern

    @property
    def sql_in_params_pattern(self) -> str:
        """Extrai o conteúdo da variável privada sql_in_params_pattern.

        Acessa a variável privada da classe, responsável pelo regex
        da verificação e validação dos parâmetros da cláusula IN,
        retornando o seu conteúdo.

        Returns:
            str: O conteúdo, regex, da variável privada da classe.
        """
        return self.__sql_in_params_pattern

    def __adapt_termination(self) -> None:
        """Altera a terminação de um comando SQL.

        Remove a junção do operador ';' de algum elemento textual
        de um comando SQL qualquer.
        """
        if self.sql_command:
            if self.sql_command[-1] == ";":
                self.sql_command = self.sql_command.replace(";", " ;", 1)
            else:
                Exceptions.raise_missing_semicolon_exception(self.sql_command)
        else:
            Exceptions.raise_missing_command_exception()

    def __tokenize(self) -> List[Tuple[str, int]]:
        """Itera sobre um comando SQL (sql_command), extraindo
        os comandos SQL válidos e suas posições.

        Itera sobre cada elemento textual do comando SQL, armazenado
        na variável privada sql_command, armazenando somente os textos
        que estão de acordo com o regex sql_token_pattern, juntamente
        com a sua posição no comando.

        Returns:
            List[Tuple[str, int]]: Uma lista de tuplas, as quais contém
            o texto representando um comando SQL e sua posição no texto.
        """
        return [
            (match.group(), match.start())
            for match in re.finditer(self.sql_token_pattern, self.sql_command, re.IGNORECASE)
        ]

    def __extract_params(self) -> List[str]:
        """Extrai os parâmetros relacionados as cláusulas SQL do
        comando fornecido ao Parser.

        Itera sobre todos os tokens extraídos, pegando, então, a
        partir da posições de uma cláusula SQL para a próxima,
        qualquer elemento textual que esteja entre os tokens.

        Returns:
            List[str]: Uma lista, contendo os parâmetros
            associados as claúsulas SQL.
        """
        return [
            self.sql_command[self.sql_tokens[i - 1][1]:self.sql_tokens[i][1]]
            .replace(self.sql_tokens[i - 1][0], "")
            .strip()
            for i in range(1, len(self.sql_tokens))
        ]

    def __validate_tokens(self) -> None:
        """Verifica a validez do posicionamento das cláusulas SQL do comando fornecido.
        """

        def add_params_suffix() -> None:
            """Adiciona um sufixo aos parâmetros AND, IN e NOT IN.

            Itera sobre as cláusulas coletadas, adicionando o sufixo "_ON"
            para parâmetros do ON e o sufixo "_WHERE" para parâmetros do
            WHERE.
            """
            which_suffix: str | None = None
            for i, token in enumerate(self.sql_tokens):
                command, pos = token
                if command.upper() == "ON":
                    which_suffix = "_ON"
                if command.upper() == "WHERE":
                    which_suffix = "_WHERE"
                if command.upper() in ["AND", "IN", "NOT IN"]:
                    self.sql_tokens[i] = (f'{command}{which_suffix}', pos)

        tokens: str = ' '.join(str(token) for token, _ in self.sql_tokens)
        if re.match(self.sql_command_pattern, tokens, re.IGNORECASE) is not None:
            add_params_suffix()
        else:
            Exceptions.raise_incorrect_clause_order_exception(self.sql_command)

    def __validate_params(self) -> None:
        """Verifica a validez de todos os parâmetros coletados das cláusulas SQL.
        """

        def is_select_valid(params: str) -> None:
            """Verifica se os parâmetros da cláusula SELECT são válidos.

            Junta os parâmetros coletados do comando SQL, da cláusula SELECT,
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            todos os parâmetros.

            Args:
                params (str): Os parâmetros da cláusula SELECT.
            """
            if params:
                if re.match(self.sql_select_params_pattern, params) is not None:
                    # Separa o nome das tabelas e o nome das colunas e armazena-os.
                    # O "*" é ignorado pelo regex!
                    param_pattern: str = r'(\w+\.\w+)|(\w+|\*)'
                    matches = re.findall(param_pattern, params)
                    for match in matches:
                        if match[0]:
                            (table_name, column_name) = match[0].split(".")
                            self.sql_tables["SELECT"].add(table_name)
                            self.sql_columns["SELECT"].add(column_name)
                        else:
                            self.sql_columns["SELECT"].add(match[1])
                else:
                    Exceptions.raise_invalid_select_params_exception(self.sql_command)
            else:
                Exceptions.raise_missing_select_params_exception(self.sql_command)

        def is_from_valid(params: str) -> None:
            """Verifica se os parâmetros da cláusula FROM são válidos.

            Junta os parâmetros coletados do comando SQL, da cláusula FROM,
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            todos os parâmetros.

            Args:
                params (str): Os parâmetros da cláusula FROM.
            """
            if params:
                if re.match(self.sql_from_params_pattern, params) is not None:
                    # Captura o nome das tabelas e armazena-as.
                    param_pattern: str = r'(\w+)'
                    matches = re.findall(param_pattern, params)
                    for match in matches:
                        self.sql_tables["FROM"].add(match)
                else:
                    Exceptions.raise_invalid_from_params_exception(self.sql_command)
            else:
                Exceptions.raise_missing_from_params_exception(self.sql_command)

        def is_join_valid(params: str) -> None:
            """Verifica se os parâmetros da cláusula JOIN são válidos.

            Junta os parâmetros coletados do comando SQL, da cláusula JOIN,
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            todos os parâmetros.

            Args:
                params (str): Os parâmetros da cláusula JOIN.
            """
            if params:
                if re.match(self.sql_join_params_pattern, params) is not None:
                    # Captura o nome das tabelas e armazena-as.
                    param_pattern: str = r'(\w+)'
                    matches = re.findall(param_pattern, params)
                    for match in matches:
                        self.sql_tables["JOIN"].add(match)
                else:
                    Exceptions.raise_invalid_join_params_exception(self.sql_command)
            else:
                Exceptions.raise_missing_join_params_exception(self.sql_command)

        def is_on_valid(params: str) -> None:
            """Verifica se a condicional da cláusula ON é válida.

            Junta a condicional coletada do comando SQL, da cláusula ON,
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            a condicional.

            Args:
                params (str): A condicional da cláusula ON.
            """
            if params:
                if re.match(self.sql_on_params_pattern, params) is not None:
                    # Captura o nome das tabelas e colunas usada na condicional e armazena-as.
                    param_pattern: str = r'(\w+\.\w+)|(\w+)'
                    matches = re.findall(param_pattern, params)
                    for match in matches:
                        if match[0]:
                            (table_name, column_name) = match[0].split(".")
                            self.sql_tables["ON"].add(table_name)
                            self.sql_columns["ON"].add(column_name)
                        else:
                            self.sql_columns["ON"].add(match[1])
                else:
                    Exceptions.raise_invalid_statement_params_exception(params)
            else:
                Exceptions.raise_missing_statement_exception("ON")

        def is_and_on_valid(params: str) -> None:
            """Verifica se a condicional da cláusula AND (do ON) é válida.

            Junta a condicional coletada do comando SQL, da cláusula AND (do ON),
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            a condicional.

            Args:
                params (str): A condicional da cláusula AND (do ON).
            """
            if params:
                if re.match(self.sql_on_params_pattern, params) is not None:
                    # Captura o nome das tabelas e colunas usada na condicional e armazena-as.
                    param_pattern: str = r'(\w+\.\w+)|(\w+)'
                    matches = re.findall(param_pattern, params)
                    for match in matches:
                        if match[0]:
                            (table_name, column_name) = match[0].split(".")
                            self.sql_tables["AND_ON"].add(table_name)
                            self.sql_columns["AND_ON"].add(column_name)
                        else:
                            self.sql_columns["AND_ON"].add(match[1])
                else:
                    Exceptions.raise_invalid_statement_params_exception(params)
            else:
                Exceptions.raise_missing_statement_exception("AND (do ON)")

        def is_in_on_valid(params: str) -> None:
            """Verifica se a condicional da cláusula IN (do ON) é válida.

            Junta a condicional coletada do comando SQL, da cláusula IN (do ON),
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            a condicional.

            Args:
                params (str): A condicional da cláusula IN (do ON).
            """
            if params:
                if (matches := re.match(self.sql_in_params_pattern, params)) is not None:
                    # Verifica a subconsulta do IN (do ON).
                    if subcommand := matches.group("subcommand1") or matches.group("subcommand2"):
                        # FIXME: Separar o nome da tabela/coluna retornada pela subconsulta???
                        Parser(subcommand + ";")
                else:
                    Exceptions.raise_invalid_statement_params_exception(params)
            else:
                Exceptions.raise_missing_statement_exception("IN (do ON)")

        def is_not_in_on_valid(params: str) -> None:
            """Verifica se a condicional da cláusula NOT IN (do ON) é válida.

            Junta a condicional coletada do comando SQL, da cláusula NOT IN (do ON),
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            a condicional.

            Args:
                params (str): A condicional da cláusula NOT IN (do ON).
            """
            if params:
                if (matches := re.match(self.sql_in_params_pattern, params)) is not None:
                    # Verifica a subconsulta do NOT IN (do ON).
                    if subcommand := matches.group("subcommand1") or matches.group("subcommand2"):
                        # FIXME: Separar o nome da tabela/coluna retornada pela subconsulta???
                        Parser(subcommand + ";")
                else:
                    Exceptions.raise_invalid_statement_params_exception(params)
            else:
                Exceptions.raise_missing_statement_exception("NOT IN (do ON)")

        def is_where_valid(params: str) -> None:
            """Verifica se a condicional da cláusula WHERE é válida.

            Junta a condicional coletada do comando SQL, da cláusula WHERE,
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            a condicional.

            Args:
                params (str): A condicional da cláusula WHERE.
            """
            if params:
                if re.match(self.sql_where_params_pattern, params) is not None:
                    # Captura o nome das tabelas e colunas usada na condicional e armazena-as.
                    param_pattern: str = r'(\w+\.\w+)|(\w+)'
                    matches = re.findall(param_pattern, params)
                    for match in matches:
                        if match[0]:
                            (table_name, column_name) = match[0].split(".")
                            self.sql_tables["WHERE"].add(table_name)
                            self.sql_columns["WHERE"].add(column_name)
                        else:
                            self.sql_columns["WHERE"].add(match[1])
                else:
                    Exceptions.raise_invalid_statement_params_exception(params)
            else:
                Exceptions.raise_missing_statement_exception("WHERE")

        def is_and_where_valid(params: str) -> None:
            """Verifica se a condicional da cláusula AND (do WHERE) é válida.

            Junta a condicional coletada do comando SQL, da cláusula AND (do WHERE),
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            a condicional.

            Args:
                params (str): A condicional da cláusula AND (do WHERE).
            """
            if params:
                if re.match(self.sql_where_params_pattern, params) is not None:
                    # Captura o nome das tabeleas e colunas usada na condicional e armazena-as.
                    param_pattern: str = r'(\w+\.\w+)|(\w+)'
                    matches = re.findall(param_pattern, params)
                    for match in matches:
                        if match[0]:
                            (table_name, column_name) = match[0].split(".")
                            self.sql_tables["AND_WHERE"].add(table_name)
                            self.sql_columns["AND_WHERE"].add(column_name)
                        else:
                            self.sql_columns["AND_WHERE"].add(match[1])
                else:
                    Exceptions.raise_invalid_statement_params_exception(params)
            else:
                Exceptions.raise_missing_statement_exception("AND (do WHERE)")

        def is_in_where_valid(params: str) -> None:
            """Verifica se a condicional da cláusula IN (do WHERE) é válida.

            Junta a condicional coletada do comando SQL, da cláusula IN (do WHERE),
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            a condicional.

            Args:
                params (str): A condicional da cláusula IN (do WHERE).
            """
            if params:
                if (matches := re.match(self.sql_in_params_pattern, params)) is not None:
                    # Verifica a subconsulta do IN (do WHERE).
                    if subcommand := matches.group("subcommand1") or matches.group("subcommand2"):
                        # FIXME: Separar o nome da tabela/coluna retornada pela subconsulta???
                        Parser(subcommand + ";")
                else:
                    Exceptions.raise_invalid_statement_params_exception(params)
            else:
                Exceptions.raise_missing_statement_exception("IN (do WHERE)")

        def is_not_in_where_valid(params: str) -> None:
            """Verifica se a condicional da cláusula NOT IN (do WHERE) é válida.

            Junta a condicional coletada do comando SQL, da cláusula NOT IN (do WHERE),
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            a condicional.

            Args:
                params (str): A condicional da cláusula NOT IN (do WHERE).
            """
            if params:
                if (matches := re.match(self.sql_in_params_pattern, params)) is not None:
                    # Verifica a subconsulta do NOT IN (do WHERE).
                    if subcommand := matches.group("subcommand1") or matches.group("subcommand2"):
                        # FIXME: Separar o nome da tabela/coluna retornada pela subconsulta???
                        Parser(subcommand + ";")
                else:
                    Exceptions.raise_invalid_statement_params_exception(params)
            else:
                Exceptions.raise_missing_statement_exception("NOT IN (do WHERE)")

        # Responsável pela chamada de uma função específica para uma cláusula SQL específica.
        validator: Dict[str, Callable[[str], None]] = {
            "SELECT": is_select_valid,
            "FROM": is_from_valid,
            "JOIN": is_join_valid,
            "ON": is_on_valid,
            "AND_ON": is_and_on_valid,
            "IN_ON": is_in_on_valid,
            "NOT IN_ON": is_not_in_on_valid,
            "WHERE": is_where_valid,
            "AND_WHERE": is_and_where_valid,
            "IN_WHERE": is_in_where_valid,
            "NOT IN_WHERE": is_not_in_where_valid
        }

        # Itera sobre todos os parâmetros coletados do comando SQL, junto com as suas cláusulas.
        for i, params in enumerate(self.sql_params):
            # Chama o método de verificação de parâmetros de um determinada cláusula SQL.
            validator[self.sql_tokens[i][0].upper()](params)

    def __validate_table_compatibility(self) -> None:
        """Verifica se todas as tabelas usadas no 
        comando SQL fornecido são compatíveis.
        
        Itera sobre as tabelas de cada cláusula registrada,
        verificando se todas possuem alguma relação com as
        tabelas do FROM e JOIN.
        """

        # Separa as tabelas válidas (aquelas que são adicionadas por cláusulas).
        valid_tables: Set[str] = self.sql_tables['FROM'].union(self.sql_tables['JOIN'])
        for clause, tables in self.sql_tables.items():
            # Ignora as cláusulas do FROM e JOIN (eles adicionam tabelas).
            if clause not in ["FROM", "JOIN"]:
                if tables:
                    if tables.issubset(valid_tables):
                        continue
                    else:
                        Exceptions.raise_table_mismatch_exception(clause)
