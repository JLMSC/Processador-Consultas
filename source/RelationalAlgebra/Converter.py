from functools import reduce
from typing import Callable, Dict, List

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

        def convert_select(params: str) -> str:
            """Converte o comando SELECT para Álgebra Relacional.

            Simplesmente retorna 'π (projeção)' junto com os
            parâmetros do SELECT.
            Caso o parâmetro seja '*', uma string vazia será retornada.

            Args:
                params (str): Os parâmetros do SELECT.

            Returns:
                str: O comando SELECT convertido em Álgebra Relacional.
            """
            # TODO: Adicionar em um nó na árvore.
            #  π (projeção) seleciona colunas e não linhas!
            return "" if params == "*" else f"π {params} "

        def convert_from(params: str) -> str:
            """Converte o comando FROM para Álgebra Relacional.

            Simplesmente retorna uma string no formato '(tabela1 x tabela2 x ...)',
            em que as tabelas são os parâmetros do FROM.
            Caso existe somente uma tabela, '(tabela)' é retornado.

            Args:
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
            
            # TODO: Adicionar em na árvore.
            # ⨝ (produto cartesiano)!
            return cross_join(*params.split(", ")) if "," in params else f"({params})"

        def convert_join(params: str) -> str:
            # TODO: Adicionar em na árvore.
            # FIXME: Pegar o sql_command, já tem a posição do JOIN atual, e só criar uma algebra relacional em cima disso com os parâmetros extras (AND, IN, NOT IN)
            return f"({params}) "

        # def convert_on(params: str) -> str:
        #     return f"σ {params} "

        # def convert_on_and(params: str) -> str:
        #     return f"∧ {params} "

        # def convert_on_in(params: str) -> str:
        #     return f"∈ {params} "

        # def convert_on_not_in(params: str) -> str:
        #     return f"¬ (∈ {params}) "

        def convert_where(params: str) -> str:
            # TODO: Adicionar em na árvore.
            # FIXME: Pegar o sql_command, já tem a posição do JOIN atual, e só criar uma algebra relacional em cima disso com os parâmetros extras (AND, IN, NOT IN)
            return f"σ {params} "

        # def convert_where_and(params: str) -> str:
        #     return f"∧ {params} "

        # def convert_where_in(params: str) -> str:
        #     return f"∈ {params} "

        # def convert_where_not_in(params: str) -> str:
        #     return f"¬ (∈ {params}) "


        convert_clause: Dict[str, Callable[[str], str]] = {
            "SELECT": convert_select,
            "FROM": convert_from,
            "JOIN": convert_join,
            # "ON": convert_on,
            # "AND_ON": convert_on_and,
            # "IN_ON": convert_on_in,
            # "NOT IN_ON": convert_on_not_in,
            "WHERE": convert_where,
            # "AND_WHERE": convert_where_and,
            # "IN_WHERE": convert_where_in,
            # "NOT IN_WHERE": convert_where_not_in
        }

        # TODO: AND, IN, NOT IN -> DEPOIS DA SELEÇÃO.
        # TODO: ON, WHERE <- ANTES DO NOME DA TABELA.

        relational_algebra: str = ""
        for clause, params in zip(self.parser.sql_tokens, self.parser.sql_params):
            (token, _) = clause
            if token.upper() in convert_clause.keys():
                # FIXME: Adicionar 'clause' nos parâmetros do 'convert_clause'. (Preciso da posição do comando.)
                relational_algebra += convert_clause[token.upper()](params)
            else:
                continue
        pass

# class Convert:
#     __parser:Parser

#     tabelas_atributos: dict[str: List[str]] = {
#         "Usuario": ["idUsuario", "Nome", "Logradouro", "Numero",  "Bairro", "CEP", "UF", "DataNascimento"],
#         "Contas": ["idConta", "Descricao", "TipoConta_idTipoCota", "Usuario_idUsuario", "SaldoInicial"],
#         "Movimentacao": ["idMovimentacao", "DataMovimentacao", "Descricao",
#                          "TipoMovimento_idTipoMovimento", "Categoria_idCategoria", "Contas_idConta", "Valor"],
#         "TipoConta": ["idTipoConta", "Descricao"],
#         "TipoMovimento": ["idTipoMovimento", "DescMovimentacao"],
#         "Categoria": ["idCategoria", "DescCategoria"]
#     }

#     # funcoes = {"SELECT": __projecao, "WHERE"}


#     def __init__(self, parser:Parser):
#         self.__parser = parser

#     def convertendo(self):
#         aux, resultado = self.__parser.sql_command.strip().split("FROM"), ""
#         percorrer_tabela = aux[1].split()
#         nome_tabela = self.__inserir_parenteses(percorrer_tabela[0])
#         id_principal, id_where, id_join = aux[1].find(";"), aux[1].find("WHERE"), aux[1].find("JOIN")

#         if " * " not in aux[0]:
#             resultado += self.__projecao(aux[0])

#         if id_where > -1:
#             resultado += self.__selecao(aux[1][id_where:id_principal])

#         elif id_where == -1 and " * " in aux[0]:
#             resultado += "σ "

#         if id_where > -1 and id_join > -1:
#             resultado += self.__juncao(aux[1][id_join:id_where - 1])
#             nome_tabela = ""

#         elif id_where == -1 and id_join > -1:
#             resultado += self.__juncao(aux[1][id_join:id_principal])
#             nome_tabela = ""

#         resultado += nome_tabela
#         print(resultado)
#         return resultado.replace(";", " ")

#     @staticmethod
#     def __projecao(string:str):
#         return string.replace("SELECT","π")

#     @staticmethod
#     def __selecao(string: str) -> str:
#         return string[string.index("WHERE"):].replace("WHERE", "σ").replace(" AND ", " ^ ").replace(" OR ", " v ")

#     def __verificar_classe(self, metodo: str) -> str:
#         if "." in metodo:
#             return str(metodo.split(".")[0].title())
#         else:

#             for x in self.tabelas_atributos.keys():
#                 tb = [y.lower() for y in self.tabelas_atributos[x]]
#                 if metodo.lower() in tb:
#                     return x
#         return ""

#     def __juncao(self, string: str):
#         aux = string.split("JOIN")
#         condicionais = [x.split("ON")[1].strip() for x in aux if x != '']
#         final = ""

#         for x in range(len(condicionais)):
#             if x == 0:
#                 final += self.__inserir_parenteses(self.__juncao_simples(condicionais[x], True))
#             else:
#                 final += self.__juncao_simples(condicionais[x], False)
#                 final = self.__inserir_parenteses(final)

#         return final

#     def __juncao_simples(self, consulta: str, primeiro:bool):
#         consulta = consulta.replace("(","").replace(")","").replace(";","")
#         aux = consulta.split(" = ")

#         if primeiro:
#             tabela = self.__verificar_classe(aux[0]) + "|X| "
#             tabela += consulta
#             consulta = tabela

#         tabela = self.__verificar_classe(aux[1])
#         consulta += self.__inserir_parenteses(tabela)

#         return consulta

#     @staticmethod
#     def __inserir_parenteses(string: str) -> str:
#         return "(" + string.strip() + ")"


