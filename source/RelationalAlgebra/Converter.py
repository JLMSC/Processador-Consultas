from functools import reduce
from typing import Callable, Dict, Tuple

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

    def __init__(self, parser: Parser) -> None:
        """Construtor da classe.

        Atribui valores a algumas variáveis e realiza
        a conversão de SQL para Álgebra Relaciona.

        Args:
            parser (Parser): Uma instância da classe Parser.
        """
        if isinstance(parser, Parser):
            self.parser = parser
            self.__convert()
        else:
            Exceptions.raise_invalid_parser_exception("Converter.py (__init__)")

    def __convert(self) -> str:

        # TODO: Adicionar em na árvore.
        def convert_select(clause: Tuple[str, int], params: str) -> str:
            """Converte o comando SELECT para Álgebra Relacional.

            Simplesmente retorna 'π (projeção)' junto com os
            parâmetros do SELECT.
            Caso o parâmetro seja '*', uma string vazia será retornada.

            Args:
                clause (Tuple[str, int]): Uma tupla, contendo a cláusula SELECT
                e a posição da cláusula no comando SQL.
                params (str): Os parâmetros do SELECT.

            Returns:
                str: O comando SELECT convertido em Álgebra Relacional.
            """
            #  π (projeção) seleciona colunas e não linhas!
            return "" if params == "*" else f"π {params} "

        # TODO: Adicionar em na árvore.
        def convert_from(clause: Tuple[str, int], params: str) -> str:
            """Converte o comando FROM para Álgebra Relacional.

            Simplesmente retorna uma string no formato '(tabela1 x tabela2 x ...)',
            em que as tabelas são os parâmetros do FROM.
            Caso existe somente uma tabela, '(tabela)' é retornado.

            Args:
                clause (Tuple[str, int]): Uma tupla, contendo a cláusula FROM
                e a posição da cláusula no comando SQL.
                params (str): Os parâmetros do FROM.

            Returns:
                str: O comando FROM convertido para Álgebra Relacional.
            """

            def cross_join(*tables: str) -> str:
                """Recebe duas tabelas e junta-as no formato '(tabela1 x tabela2 x ...)'.

                Args:
                    *tables (str): Os nomes das tabelas a serem unidas.

                Returns:
                    str: As tabelas unidas no formato '(tabela1 x tabela2 x ...)'.
                """
                return reduce(lambda table1, table2: f"({table1} ⨝ {table2})", tables)
            
            # ⨝ (produto cartesiano)!
            return f"{cross_join(*params.split(', '))} " if "," in params else f"({params}) "

        # FIXME: Adicionar cada um em um nó de uma árvore.
        def convert_join(clause: Tuple[str, int], params: str) -> str:
            """Converte o comando JOIN em Álgebra Relacional.

            Simplesmente retorna uma string, em que cada parâmetro extra,
            por exemplo: ON, AND, IN e NOT IN, são convertidos internamente,
            também, em Álgebra Relacional.

            Args:
                clause (Tuple[str, int]): Uma tupla, contendo a cláusula JOIN
                e a posição da cláusula no comando SQL.
                params (str): Os parâmetros do JOIN.

            Returns:
                str: O comando JOIN convertido para Álgebra Relacional.
            """

            def convert_on(params: str) -> str:
                """Converte o comando ON em Álgebra Relacional.

                Args:
                    params (str): Os parâmetros do ON.

                Returns:
                    str: O comando ON convertido para Álgebra Relacional.
                """
                # σ (seleção) seleciona linhas e não colunas!
                return f"(σ {params} "

            def convert_on_and(params: str) -> str:
                """Converte o operador AND (do JOIN ON) em Álgebra Relacional.

                Args:
                    params (str): Os parâmetros do AND.

                Returns:
                    str: O operador AND convertido para Álgebra Relacional.
                """
                # ∧ (AND)!
                return f"∧ {params} "

            def convert_on_in(params: str) -> str:
                """Converte o operador IN (do JOIN ON) em Álgebra Relacional.

                Args:
                    params (str): Os parâmetros do IN.

                Returns:
                    str: O operador IN convertido para Álgebra Relacional.
                """
                # ∈ (IN)!
                return f"∈ {params} "

            def convert_on_not_in(params: str) -> str:
                """Converte o operador NOT IN (do JOIN ON) em Álgebra Relacional.

                Args:
                    params (str): Os parâmetros do NOT IN.

                Returns:
                    str: O operador NOT IN convertido para Álgebra Relacional.
                """
                # ¬ ∈ (NOT IN)!
                return f"¬ (∈ {params}) "
            
            convert_accepted_clause: Dict[str, Callable[[str], str]] = {
                "ON": convert_on,
                "AND_ON": convert_on_and,
                "IN_ON": convert_on_in,
                "NOT IN_ON": convert_on_not_in
            }

            # Índice do comando JOIN em 'parser.sql_tokens'.
            command_index: int = self.parser.sql_tokens.index(clause) + 1
            relational_algebra: str = ""
            # Converte os parâmetros extras do JOIN em algebra relacional, se tiver um que não é do JOIN, retorna 'relational_algebra'.
            for other_clause, other_params in zip(self.parser.sql_tokens[command_index::], self.parser.sql_params[command_index::]):
                (token, _) = other_clause
                if token.upper() in convert_accepted_clause.keys():
                    relational_algebra += convert_accepted_clause[token.upper()](other_params)
                else:
                    break
            # Adiciona a tabela do JOIN ao final da expressão, adiciona também os ')' faltando.
            return f"{relational_algebra}({params}){')' * relational_algebra.count('(')} "

        # FIXME: Adicionar cada um em um nó de uma árvore.
        def convert_where(clause: Tuple[str, int], params: str) -> str:
            """Converte o comando WHERE em Álgebra Relacional.

            Simplesmente retorna uma string, em que cada parâmetro extra,
            por exemplo: AND, IN e NOT IN, são convertidos internamente,
            também, em Álgebra Relacional.

            Args:
                clause (Tuple[str, int]): Uma tupla, contendo a cláusula WHERE
                e a posição da cláusula no comando SQL.
                params (str): Os parâmetros do WHERE.

            Returns:
                str: O comando WHERE convertido para Álgebra Relacional.
            """

            def convert_where_and(params: str) -> str:
                """Converte o operador AND (do WHERE) em Álgebra Relacional.

                Args:
                    params (str): Os parâmetros do AND.

                Returns:
                    str: O operador AND convertido para Álgebra Relacional.
                """
                # ∧ (AND)!
                return f"∧ {params} "

            def convert_where_in(params: str) -> str:
                """Converte o operador IN (do WHERE) em Álgebra Relacional.

                Args:
                    params (str): Os parâmetros do IN.

                Returns:
                    str: O operador IN convertido para Álgebra Relacional.
                """
                # ∈ (IN)!
                return f"∈ {params} "

            def convert_where_not_in(params: str) -> str:
                """Converte o operador NOT IN (do WHERE) em Álgebra Relacional.

                Args:
                    params (str): Os parâmetros do NOT IN.

                Returns:
                    str: O operador NOT IN convertido para Álgebra Relacional.
                """
                # ¬ ∈ (NOT IN)!
                return f"¬ (∈ {params}) "

            convert_accepted_clause: Dict[str, Callable[[str], str]] = {
                "AND_WHERE": convert_where_and,
                "IN_WHERE": convert_where_in,
                "NOT IN_WHERE": convert_where_not_in
            }

            # Índice do comando WHERE em 'parser.sql_tokens'.
            command_index: int = self.parser.sql_tokens.index(clause) + 1
            relational_algebra: str = ""
            # Converte os parâmetros extras do WHERE em algebra relacional, se tiver um que não é do WHERE, retorna 'relational_algebra'.
            for other_clause, other_params in zip(self.parser.sql_tokens[command_index::], self.parser.sql_params[command_index::]):
                (token, _) = other_clause
                if token.upper() in convert_accepted_clause.keys():
                    relational_algebra += convert_accepted_clause[token.upper()](other_params)
                else:
                    break
            # Adiciona a tabela do WHERE ao final da expressão, adiciona também os ')' faltando.
            # Estou assumindo que 'sql_params[1]' será sempre o do FROM.
            return f"(σ {params} {relational_algebra}({self.parser.sql_params[1]}){')' * relational_algebra.count('(')}"

        convert_clause: Dict[str, Callable[[Tuple[str, int], str], str]] = {
            "SELECT": convert_select,
            "FROM": convert_from,
            "JOIN": convert_join,
            "WHERE": convert_where,
        }

        self.relational_algebra = ""
        for clause, params in zip(self.parser.sql_tokens, self.parser.sql_params):
            # Ignora cláusulas como o ON, AND, IN e NOT IN. (JOIN e WHERE já fazem isso.)
            if clause[0].upper() in convert_clause.keys():
                self.relational_algebra += convert_clause[clause[0].upper()](clause, params)
            else:
                continue
        # Retorna o comando SQL convertido para Álgebra Relacional.
        return self.relational_algebra