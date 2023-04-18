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
    __sql_token_pattern: str = r'\b(select|from|join|on|where)\b|(;$)'
    # Expressão regular para a verificação do posicionamento das cláusulas do MySQL.
    __sql_command_pattern: str = r'^select\sfrom\s(?:join\son\s|where\s)*;$'
    # Expressão regular para validação dos parâmetros da cláusula SELECT do MySQL.
    __sql_select_params_pattern: str = r'\*|^([a-zA-Z][a-zA-Z0-9_]*\.)?[a-zA-Z][a-zA-Z0-9_]*(,[ ]*([a-zA-Z][a-zA-Z0-9_]*\.)?[a-zA-Z][a-zA-Z0-9_]*)*$'
    # Expressão regular para validação dos parâmetros da cláusula FROM do MySQL.
    __sql_from_params_pattern: str = r'^[a-zA-Z][a-zA-Z0-9_]*(,[ ]*[a-zA-Z][a-zA-Z0-9_]*)*$'

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
        self.__validate_tokens()
        self.sql_params = self.__extract_params()
        self.__sql_tables = {"SELECT": set(), "FROM": set(), "JOIN": set(), "ON": set(), "WHERE": set()}
        self.__sql_columns = {"SELECT": set(), "FROM": set(), "JOIN": set(), "ON": set(), "WHERE": set()}
        self.__validate_params()

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
            (token, i)
            for i, token in enumerate(self.sql_command.strip().split())
            if re.match(self.sql_token_pattern, token, re.IGNORECASE)
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
        commands: List[str] = self.sql_command.strip().split()
        return [
            commands[self.sql_tokens[i-1][1]+1:self.sql_tokens[i][1]]
            for i in range(1, len(self.sql_tokens))
        ]

    def __validate_tokens(self) -> None:
        """Verifica a validez do posicionamento das cláusulas SQL do comando fornecido.
        """
        tokens: str = ' '.join(str(token) for token, _ in self.sql_tokens)
        if re.match(self.sql_command_pattern, tokens, re.IGNORECASE) is None:
            Exceptions.raise_incorrect_clause_order_exception(self.sql_command)

    def __validate_params(self) -> None:
        """Verifica a validez de todos os parâmetros coletados das cláusulas SQL.
        """

        def is_select_valid(params: str) -> bool:
            """Verifica se os parâmetros da cláusula SELECT são válidos.

            Junta os parâmetros coletados do comando SQL, da cláusula SELECT,
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            todos os parâmetros.

            Args:
                params (str): Os parâmetros da cláusula SELECT.

            Returns:
                bool: Se os parâmetros são válidos ou não.
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
                    # Indica que os parâmetros do SELECT são válidos.
                    return True
                Exceptions.raise_invalid_select_params_exception(self.sql_command)
            Exceptions.raise_missing_select_params_exception(self.sql_command)

        def is_from_valid(params: str) -> bool:
            """Verifica se os parâmetros da cláusula FROM são válidos.

            Junta os parâmetros coletados do comando SQL, da cláusula SELECT,
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            todos os parâmetros.

            Args:
                params (str): Os parâmetros da cláusula FROM.

            Returns:
                bool: Se os parâmetros são válidos ou não.
            """
            if params:
                if re.match(self.sql_from_params_pattern, params) is not None:
                    # Captura o nome das tabelas e armazena-as.
                    param_pattern: str = r'(\w+)'
                    matches = re.findall(param_pattern, params)
                    for match in matches:
                        self.sql_tables["FROM"].add(match)
                    # Indica que os parâmetros do FROM são válidos.
                    return True
                Exceptions.raise_invalid_from_params_exception(self.sql_command)
            Exceptions.raise_missing_from_params_exception(self.sql_command)

        def is_join_valid(params: str) -> bool:
            # TODO: Implementar isso aqui.
            # TODO: Botar uma exceção aqui em um simples IF.
            pass

        def is_on_valid(params: str) -> bool:
            # TODO: Implementar isso aqui.
            # TODO: Botar uma exceção aqui em um simples IF.
            pass

        def is_where_valid(params: str) -> bool:
            # TODO: Implementar isso aqui.
            # TODO: Botar uma exceção aqui em um simples IF.
            pass

        # Responsável pela chamada de uma função específica para uma cláusula SQL específica.
        validator: Dict[str, Callable[[str], bool]] = {
            "SELECT": is_select_valid,
            "FROM": is_from_valid,
            "JOIN": is_join_valid,
            "ON": is_on_valid,
            "WHERE": is_where_valid
        }

        # Itera sobre todos os parâmetros coletados do comando SQL, junto com as suas cláusulas.
        params_are_valid: bool = True
        for i, params in enumerate(self.sql_params):
            # Junta os parâmetros de uma cláusula em uma string única.
            params_str: str = ' '.join(str(p) for p in params)
            # Chama o método de verificação de parâmetros de um determinada cláusula SQL.
            params_are_valid = all([validator[self.sql_tokens[i][0]](params_str), params_are_valid])
        # FIXME: Antes de retornar "params_are_valid", verificar se o nome das colunas e tabelas são compatíveis.
        return params_are_valid
