from typing import List

from source.Parser.parser import Parser


class Node:
    valor:str
    left = None
    right = None
    level=0;

    def __init__(self, vl, left, right):
        self.valor = vl
        self.left = left
        self.right = right

class Convert:
    __parser:Parser
    __raiz:Node

    tabelas_atributos: dict[str: List[str]] = {
        "Usuario": ["idUsuario", "Nome", "Logradouro", "Numero",  "Bairro", "CEP", "UF", "DataNascimento"],
        "Contas": ["idConta", "Descricao", "TipoConta_idTipoCota", "Usuario_idUsuario", "SaldoInicial"],
        "Movimentacao": ["idMovimentacao", "DataMovimentacao", "Descricao",
                         "TipoMovimento_idTipoMovimento", "Categoria_idCategoria", "Contas_idConta", "Valor"],
        "TipoConta": ["idTipoConta", "Descricao"],
        "TipoMovimento": ["idTipoMovimento", "DescMovimentacao"],
        "Categoria": ["idCategoria", "DescCategoria"]
    }

    #funcoes = {"SELECT": __projecao, "WHERE"}


    def __init__(self, parser:Parser):
        self.__parser = parser

    def convertendo(self):
        aux, resultado = self.__parser.sql_command.strip().split("FROM"), ""
        percorrer_tabela = aux[1].split()
        nome_tabela = self.__inserir_parenteses(percorrer_tabela[0])
        id_principal, id_where, id_join = aux[1].find(";"), aux[1].find("WHERE"), aux[1].find("JOIN")

        if " * " not in aux[0]:
            resultado += self.__projecao(aux[0])

        if id_where > -1:
            resultado += self.__selecao(aux[1][id_where:id_principal])

        elif id_where == -1 and " * " in aux[0]:
            resultado += "σ "

        if id_where > -1 and id_join > -1:
            resultado += self.__juncao(aux[1][id_join:id_where - 1])
            nome_tabela = ""

        elif id_where == -1 and id_join > -1:
            resultado += self.__juncao(aux[1][id_join:id_principal])
            nome_tabela = ""

        resultado += nome_tabela
        print(resultado)
        return resultado.replace(";", " ")

    @staticmethod
    def __projecao(string:str):
        return string.replace("SELECT","π")

    @staticmethod
    def __selecao(string: str) -> str:
        return string[string.index("WHERE"):].replace("WHERE", "σ").replace(" AND ", " ^ ").replace(" OR ", " v ")

    def __verificar_classe(self, metodo: str) -> str:
        if "." in metodo:
            return str(metodo.split(".")[0].title())
        else:

            for x in self.tabelas_atributos.keys():
                tb = [y.lower() for y in self.tabelas_atributos[x]]
                if metodo.lower() in tb:
                    return x
        return ""

    def __juncao(self, string: str):
        aux = string.split("JOIN")
        condicionais = [x.split("ON")[1].strip() for x in aux if x != '']
        final = ""

        for x in range(len(condicionais)):
            if x == 0:
                final += self.__inserir_parenteses(self.__juncao_simples(condicionais[x], True))
            else:
                final += self.__juncao_simples(condicionais[x], False)
                final = self.__inserir_parenteses(final)

        return final

    def __juncao_simples(self, consulta: str, primeiro:bool):
        consulta = consulta.replace("(","").replace(")","").replace(";","")
        aux = consulta.split(" = ")

        if primeiro:
            tabela = self.__verificar_classe(aux[0]) + "|X| "
            tabela += consulta
            consulta = tabela

        tabela = self.__verificar_classe(aux[1])
        consulta += self.__inserir_parenteses(tabela)

        return consulta

    @staticmethod
    def __inserir_parenteses(string: str) -> str:
        return "(" + string.strip() + ")"


