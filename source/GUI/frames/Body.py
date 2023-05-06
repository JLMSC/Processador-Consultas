"""Representa o corpo de uma aplicação"""

from tkinter import Button
from tkinter.font import Font
from tkinter.ttk import Frame, Label, Entry

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
    body_output_font: Font

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
        self.body_output_font = Font(family="Callibri", size=12, weight="normal")

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
        Entry(self, font=self.body_entry_font)\
            .grid(padx=padx, pady=pady, column=1, row=1, sticky="NSWE")
        # Botão para converter o comando SQL para Álgebra Relacional.
        # TODO: Comando do botão (body)
        Button(self, text="Converter comando SQL para Álgebra Relacional", font=self.body_button_font,
               command=None)\
            .grid(padx=padx, pady=pady, column=1, row=2, sticky="N")
