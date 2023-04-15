"""Arquivo responsável pela validação e verificação de
um comando SQL, bem como as cláusulas utilizadas, a sua
estrutura e, também, os parâmetros."""

import re

from typing import List, Tuple, Dict, Callable

# pylint: disable=import-error
from Exceptions.missing_semicolon import raise_missing_semicolon_exception

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
    __sql_params: Dict[Tuple[str, int], List[str]]
    # FIXME: Posso assumir que todo comando MySQL DEVE terminar com ; ?
    # Expressão regular para extração de palavras reservadas (cláusulas) do MySQL.
    __sql_command_pattern: str = r'\b(select|from|join|on|where)\b|(;$)'
    # Expressão regular para validação dos parâmetros da cláusula SELECT do MySQL.
    __sql_select_params_pattern: str = r'\*|^[a-zA-Z]+[a-zA-Z0-9_]*(,\s*[a-zA-Z]+[a-zA-Z0-9_]*)*$|^[a-zA-Z]+[a-zA-Z0-9_]*\.[a-zA-Z]+[a-zA-Z0-9_]*(,\s*[a-zA-Z]+[a-zA-Z0-9_]*\.[a-zA-Z]+[a-zA-Z0-9_]*)*$'

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
    def sql_params(self) -> Dict[Tuple[str, int], List[str]]:
        """Extrai o conteúdo da variável privada sql_params.

        Acessa a variável privada da classe, responsável pelo
        armazenamento dos parâmetros das cláusulas SQL, retornando
        seu conteúdo.

        Returns:
            Dict[Tuple[str, int], List[str]]: Um dicionário,
            contendo as cláusulas SQL, suas posições e os 
            parâmetros associados as claúsulas SQL.
        """
        return self.__sql_params

    @sql_params.setter
    def sql_params(self, new_sql_params: Dict[Tuple[str, int], List[str]]) -> None:
        """Altera o conteúdo da variável privada sql_params.

        Acessa a variável privada da classe, responsável pelo
        armazenamento dos parâmetros das cláusulas SQL, atribuindo
        um novo valor para a variável.

        Args:
            new_sql_params (Dict[Tuple[str, int], List[str]]): Um
            dicionário, contendo as cláusulas SQL, suas posições e
            os parâmetros associados as cláusulas SQL.
        """
        self.__sql_params = new_sql_params

    @property
    def sql_command_pattern(self) -> str:
        """Extrai o conteúdo da variável privada sql_command_pattern

        Acessa a variável privada da classe, responsável pelo regex
        da seleção e captura de comandos SQL, bem como o SELECT, FROM,
        JOIN, ON e WHERE, retornando seu conteúdo.

        Returns:
            str: O conteúdo, regex, da variável privada da classe.
        """
        return self.__sql_command_pattern

    def __adapt_termination(self) -> None:
        """Altera a terminação de um comando SQL.

        Remove a junção do operador ';' de algum elemento textual
        de um comando SQL qualquer.
        """
        if self.sql_command[-1] == ";":
            self.sql_command = self.sql_command.replace(";", " ;", 1)
        else:
            raise_missing_semicolon_exception(self.sql_command)

    def __tokenize(self) -> List[Tuple[str, int]]:
        """Itera sobre um comando SQL (sql_command), extraindo
        os comandos SQL válidos e suas posições.

        Itera sobre cada elemento textual do comando SQL, armazenado
        na variável privada sql_command, armazenando somente os textos
        que estão de acordo com o regex sql_command_pattern, juntamente
        com a sua posição no comando.

        Returns:
            List[Tuple[str, int]]: Uma lista de tuplas, as quais contém
            o texto representando um comando SQL e sua posição no texto.
        """
        return [
            (token, i)
            for i, token in enumerate(self.sql_command.strip().split())
            if re.match(self.sql_command_pattern, token, re.IGNORECASE)
        ]

    def __extract_params(self) -> Dict[Tuple[str, int], List[str]]:
        """Extrai os parâmetros relacionados as cláusulas SQL do
        comando fornecido ao Parser.

        Itera sobre todos os tokens extraídos, pegando, então, a
        partir da posições de uma cláusula SQL para a próxima,
        qualquer elemento textual que esteja entre os tokens.

        Returns:
            Dict[Tuple[str, int], List[str]]: Um dicionário,
            contendo as cláusulas SQL, suas posições e os 
            parâmetros associados as claúsulas SQL.
        """
        commands: List[str] = self.sql_command.strip().split()
        return {
            (self.sql_tokens[i-1]): list(commands[self.sql_tokens[i-1][1]+1:self.sql_tokens[i][1]])
            for i in range(1, len(self.sql_tokens))
        }

    def __validate_params(self) -> None:
        """Verifica a validez de todos os parâmetros coletados das cláusulas SQL.
        """

        def is_select_valid(params: List[str]) -> bool:
            """Verifica se os parâmetros da cláusula SELECT são válidos.

            Junta os parâmetros coletados do comando SQL, da cláusula SELECT,
            e aplica um regex no mesmo, verificando se existe algum 'match' com
            todos os parâmetros.

            Args:
                params (List[str]): Os parâmetros da cláusula SELECT.

            Returns:
                bool: Se os parâmetros são válidos ou não.
            """
            params_str: str = ' '.join(str(p) for p in params)
            return re.match(self.__sql_select_params_pattern, params_str) is not None

        def is_from_valid(params: List[str]) -> bool:
            # TODO: Implementar isso aqui.
            # TODO: Verificar se as colunas do FROM ta de acordo com os alias do SELECT.
            pass

        def is_join_valid(params: List[str]) -> bool:
            # TODO: Implementar isso aqui.
            pass

        def is_on_valid(params: List[str]) -> bool:
            # TODO: Implementar isso aqui.
            pass

        def is_where_valid(params: List[str]) -> bool:
            # TODO: Implementar isso aqui.
            pass

        # Responsável pela chamada de uma função específica para uma cláusula SQL específica.
        validator: Dict[str, Callable[[List[str]], bool]] = {
            "SELECT": is_select_valid,
            "FROM": is_from_valid,
            "JOIN": is_join_valid,
            "ON": is_on_valid,
            "WHERE": is_where_valid
        }

        # TODO: Separar os parâmetros válidos em uma lista ou sei lá, tem que ver se o nome das tabelas e alias tão de acordo.
        # Itera sobre todos os parâmetros coletados do comando SQL, junto com as suas cláusulas.
        params_are_valid: bool = True
        for key, value in self.sql_params.items():
            params_are_valid = all([validator[key[0]](value), params_are_valid])
        return params_are_valid
