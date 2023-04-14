import re

from typing import List, Tuple, Dict

# TODO: Botar as exceções, e os métodos também, em um arquivo separado.

class InvalidSQLCommand(Exception):
    """Exceção lançada quando um comando SQL é classificado
    como inválido.
    """

def raise_invalid_sql_command_exception(sql_command: str) -> None:
    """Lança uma exceção quando um comando SQL fornecido é
    classificado como inválido.

    Args:
        sql_command (str): O comando SQL usado para verificação
        e validação.

    Raises:
        InvalidSQLCommand: Exceção customizada para alertar
        que um comando SQL foi classificado como inválido.
    """
    raise InvalidSQLCommand(
        f"[{sql_command}]\nO comando SQL fornecido é inválido."
    )

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
    # Expressão regular para extração de palavras reservadas do MySQL.
    __sql_command_pattern: str = r'\b(select|from|join|on|where)\b|(;$)'

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
            raise_invalid_sql_command_exception(self.sql_command)

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


# TODO: Inserir mais casos de teste. (Botar em um Loop)
Parser(
    "SELECT * " +
    "FROM tabela1 " +
    "JOIN tabela2 ON tabela1.id = tabela2.id " +
    "JOIN tabela3 ON tabela2.id = tabela3.id " +
    "JOIN tabela4 ON tabela3.id = tabela4.id;"
)
