"""Representa o rodapé de uma aplicação"""

from tkinter.font import Font
from tkinter.ttk import Frame, Label

class Footer(Frame):
    """Representa um rodapé para uma aplicação.

    Args:
        Frame (Frame): Rodapé de uma aplicação.
    """
    # O contêiner principal.
    master_container: Frame
    # Fonte usada nos textos do rodapé.
    footer_text_font: Font

    def __init__(self, master: Frame = None) -> None:
        """Inicializa o rodapé em um contêiner.

        Args:
            master (Frame, optional): O contêiner a ser
            referênciada durante a inicialização do
            rodapé.
            Valor padrão 'None'.
        """
        super().__init__(master=master, relief="sunken")
        self.master_container = master
        # Configura as fontes usadas no rodapé.
        self.__configure_footer_fonts()

    def __configure_footer_fonts(self) -> None:
        """Configura as fontes usadas no rodapé."""
        self.footer_text_font = Font(family="Callibri", size=8, weight="bold")

    def frame_grid(self, column: int, row: int, padx: int, pady: int) -> None:
        """Configura o rodapé.

        Args:
            column (int): Índice da coluna do rodapé.
            row (int): Índice da linha do rodapé.
            padx (int): Margem no eixo X, para ambos os lados.
            pady (int): Margem no eixo Y, para ambos os lados.
        """
        self.grid(column=column, row=row, padx=padx, pady=pady, sticky="WE")

    def configure_columns(self, column_id: int, weight: int) -> None:
        """Configura uma coluna do rodapé.

        Args:
            column_id (int): O índice da coluna.
            weight (int): A área da coluna (valor multiplicativo).
        """
        self.grid_columnconfigure(column_id, weight=weight)

    def draw_body(self, padx: int, pady: int) -> None:
        """Renderiza elementos ao rodapé.

        Args:
            padx (int): Margem no eixo X, para ambos os lados.
            pady (int): Margem no eixo Y, para ambos os lados.
        """
        # Texto indicando a saída do Parser.
        Label(self, text="", font=self.footer_text_font, foreground="red")\
            .grid(padx=padx, pady=pady, column=0, row=0, sticky="W")
