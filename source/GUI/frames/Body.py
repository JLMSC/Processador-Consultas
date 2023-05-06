"""Representa o corpo de uma aplicação"""

from tkinter.font import Font
from tkinter import Button, END
from tkinter.ttk import Frame, Label, Entry

# pylint: disable=import-error
# pylint: disable=no-name-in-module
import Examples

from Parser.parser import Parser
from GUI.frames.TreeCanvas import TreeCanvas
from RelationalAlgebra.Converter import Node, Converter

class Body(Frame):
    """Representa um corpo para uma aplicação.
    Args:
        Frame (Frame): Contêiner de uma aplicação.
    """
    # O contêiner principal.
    master_container: Frame
    # Fontes usadas nos textos do corpo.
    body_text_font: Font
    body_entry_font: Font
    body_button_font: Font
    # O parser.
    parser: Parser
    # O conversor.
    converter: Converter
    # O entry.
    body_entry: Entry

    def __init__(self, master: Frame = None) -> None:
        """Inicializa o corpo em um contêiner.
        Args:
            master (Frame, optional): O contêiner a ser
            referenciada durante a inicialização do
            corpo.
            Valor padrão 'None'.
        """
        super().__init__(master=master, relief="sunken")
        self.master_container = master
        # Configura as fontes usadas no corpo.
        self.__configure_body_fonts()

    def __configure_body_fonts(self) -> None:
        """Configura as fontes usadas no corpo."""
        self.body_text_font = Font(family="Callibri", size=12, weight="bold")
        self.body_entry_font = Font(family="Callibri", size=12, weight="normal")
        self.body_button_font = Font(family="Callibri", size=12, weight="bold")

    def frame_grid(self, column: int, row: int, padx: int, pady: int) -> None:
        """Configura o corpo.
        Args:
            column (int): Índice da coluna do corpo.
            row (int): Índice da linha do corpo.
            padx (int): Margem no eixo X, para ambos os lados.
            pady (int): Margem no eixo Y, para ambos os lados.
        """
        self.grid(column=column, row=row, padx=padx, pady=pady, sticky="NSWE")

    def configure_column(self, column_id: int, weight: int) -> None:
        """Configura uma coluna do corpo.
        Args:
            column_id (int): O índice da coluna.
            weight (int): A área da coluna (valor multiplicativo).
        """
        self.grid_columnconfigure(column_id, weight=weight)

    def configure_row(self, row_id: int, weight: int) -> None:
        """Configura uma linha do corpo.
        Args:
            row_id (int): O índice da linha.
            weight (int): A área da linha (valor multiplicativo).
        """
        self.grid_rowconfigure(row_id, weight=weight)

    def __draw_tree(self) -> None:
        """Limpa o Canvas do cabeçalho e desenha 
        a Árvore da Álgebra Relacional.
        """

        def dfs_drawing(canvas: TreeCanvas, node: Node, xpos: int, ypos: int, padx: int = 50, pady: int = 50) -> None:
            """Desenha uma Árvore para a Álgebra Relacional usando DFS.

            Args:
                canvas (TreeCanvas): O canvas onde será desenhado.
                node (Node): O nó inicial.
                xpos (int): A posição horizontal do nó inicial.
                ypos (int): A posição vertical do nó inicial.
                padx (int, optional): A margem de deslocamento na 
                horizontal dos nós filhos. Valor padrão: 50.
                paddy (int, optional): A margem de deslocamento na
                vertical dos nós filhos. Valor padrão: 50.
            """
            if node:
                # Desenha o círculo do Nó.
                canvas.create_oval(
                    xpos - 10, ypos - 10,
                    xpos + 10, ypos + 10,
                    fill="white", outline="black"
                )
                # Adiciona um texto acima do Nó.
                canvas.create_text(
                    xpos, ypos - 20,
                    text=f"{node.execution_order}°- {node.value}",
                    font=node_text_font
                )

                # Desenha o Nó filho esquerdo, se houver.
                if node.left_children:
                    node_text = f"{node.execution_order}°- {node.value}"
                    node_text_width = node_text_font.measure(node_text)
                    # Cria uma aresta entre os dois Nós.
                    padx = node_text_width / 2
                    canvas.create_line(xpos, ypos + 10, xpos - padx, ypos + pady - 10, fill="gray")
                    dfs_drawing(canvas, node.left_children, xpos - padx, ypos + pady, padx // 2, pady)

                # Desenha o Nó filho direito, se houver.
                if node.right_children:
                    node_text = f"{node.right_children.execution_order}°- {node.right_children.value}"
                    node_text_width = node_text_font.measure(node_text)
                    # Cria uma aresta entre os dois Nós.
                    padx = node_text_width / 2
                    canvas.create_line(xpos, ypos + 10, xpos + padx, ypos + pady + 10, fill="gray")
                    dfs_drawing(canvas, node.right_children, xpos + padx, ypos + pady + 20, padx // 2, pady)

        try:
            # Captura o Canvas do cabeçalho.
            target_canvas: TreeCanvas = self.master_container.header.canvas
            # Pega o texto do entry e passa para o parser, verificando se o
            # comando é válido.
            self.parser = Parser(self.body_entry.get())
            self.parser.check_database_compatibility(Examples.pagamento_example_db)
            # Inicializa o conversor passando o texto de 'Label' para um Parser.
            self.converter = Converter(self.parser)
            # Converte o comando SQL para Álgebra Relacional.
            self.converter.convert_in_database_context(Examples.pagamento_example_db)
            # TODO: Mostrar as Exceptions em um footer (em vermelho).
            # Limpa o Entry.
            self.body_entry.delete(0, END)
            # Limpa o Canvas do cabeçalho.
            target_canvas.delete("all")
            # Desenha a Árvore.
            node_text_font = Font(family="Callibri", size=12, weight="bold")
            dfs_drawing(target_canvas, self.converter.relational_algebra_tree, 400, 50)
        except Exception as excp:
            self.master_container.footer.children["!label"].config(text=f"({type(excp).__name__}):\n{excp}")

    def draw_body(self, padx: int, pady: int) -> None:
        """Renderiza elementos ao corpo.
        Args:
            padx (int): Margem no eixo X, para ambos os lados.
            pady (int): Margem no eixo Y, para ambos os lados.
        """
        # Texto indicando a inserção do comando SQL.
        Label(self, text="Comando SQL", font=self.body_text_font)\
            .grid(padx=padx, pady=pady, column=1, row=0, sticky="N")
        # Campo de entrada para o comando SQL.
        self.body_entry = Entry(self, font=self.body_entry_font)
        self.body_entry.grid(padx=padx, pady=pady, column=1, row=1, sticky="NSWE")
        # Botão para converter o comando SQL para Álgebra Relacional.
        Button(self, text="Converter comando SQL para Álgebra Relacional", font=self.body_button_font,
               command=self.__draw_tree)\
            .grid(padx=padx, pady=pady, column=1, row=2, sticky="N")
