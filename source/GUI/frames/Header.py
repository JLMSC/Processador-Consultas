"""Representa o cabeçalho de uma aplicação."""

from tkinter import Canvas
from tkinter.font import Font
from tkinter.ttk import Frame, Label

# pylint: disable=import-error
# pylint: disable=no-name-in-module
from GUI.frames.TreeCanvas import TreeCanvas

class Header(Frame):
    """Representa um cabeçalho para uma aplicação.

    Args:
        Frame (Frame): Contêiner de uma aplicação.
    """
    # O contêiner principal.
    master_container: Frame
    # O canvas.
    canvas: Canvas
    # Fontes usadas nos textos do cabeçalho.
    header_text_font: Font

    def __init__(self, master: Frame = None) -> None:
        """Inicializa o cabeçalho em um contêiner.

        Args:
            master (Frame, optional): O contêiner a ser
            referenciado durante a inicialização do
            cabeçalho.
            Valor padrão: 'None'.
        """
        super().__init__(master=master, relief="sunken")
        self.master_container = master
        # Configura as fontes usadas no cabeçalho.
        self.__configure_header_fonts()

    def __configure_header_fonts(self) -> None:
        """Configura as fontes usadas no cabeçalho."""
        self.header_text_font = Font(family="Callibri", size=12, weight="bold")

    def frame_grid(self, column: int, row: int, padx: int, pady: int) -> None:
        """Configura o cabeçalho.

        Args:
            column (int): Índice da coluna do cabeçalho.
            row (int): Índice da linha do cabeçalho.
            padx (int): Margem no eixo X, para ambos os lados.
            pady (int): Margem no eixo Y, para ambos os lados.
        """
        self.grid(column=column, row=row, padx=padx, pady=pady, sticky="NSWE")

    def configure_column(self, column_id: int, weight: int) -> None:
        """Configura uma coluna do cabeçalho.

        Args:
            column_id (int): O índice da coluna.
            weight (int): A área da coluna (valor multiplicativo).
        """
        self.grid_columnconfigure(column_id, weight=weight)

    def configure_row(self, row_id: int, weight: int) -> None:
        """Configura uma linha do cabeçalho.

        Args:
            row_id (int): O índice da linha.
            weight (int): A área da linha (valor multiplicativo).
        """
        self.grid_rowconfigure(row_id, weight=weight)

    def draw_body(self, padx: int, pady: int) -> None:
        """Renderiza elementos ao cabeçalho.

        Args:
            padx (int): Margem no eixo X, para ambos os lados.
            pady (int): Margem no eixo Y, para ambos os lados.
        """
        # Texto indicando que é a Árvore da Álgebra Relacional.
        Label(self, text="Árvore da Álgebra Relacional", font=self.header_text_font)\
            .grid(padx=padx, pady=pady, column=1, row=0, sticky="N")
        # Canvas onde será mostrado o desenho da Árvore da Álgebra Relacional.
        self.canvas = TreeCanvas(self)
        self.canvas.grid(padx=padx, pady=pady, column=1, row=1, sticky="NSWE")
