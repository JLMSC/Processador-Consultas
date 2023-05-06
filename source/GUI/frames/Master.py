"""Representa o contêiner principal de uma aplicação."""

from tkinter import Tk
from tkinter.ttk import Frame

# pylint: disable=import-error
# pylint: disable=no-name-in-module
from GUI.frames.Body import Body
from GUI.frames.Header import Header
from GUI.frames.Footer import Footer

class Master(Frame):
    """Representa o contêiner principal para uma aplicação.

    Args:
        Frame (Frame): Contêiner principal de uma aplicação.
    """
    # A aplicação principal.
    app: Tk
    # Os demais contêineres da aplicação.
    header: Header
    body: Body
    footer: Footer

    def __init__(self, master: Tk = None) -> None:
        """Inicializa o contêiner principal em uma aplicação.

        Args:
            master (Tk, optional): A aplicação a ser referenciada
            durante a inicialização do contêiner principal.
            Valor padrão: None.
        """
        super().__init__(master=master, relief="flat")
        self.app = master

    def frame_grid(self, column: int, row: int, padx: int, pady: int) -> None:
        """Configura o contêiner principal.
        Args:
            column (int): Índice da coluna do cabeçalho.
            row (int): Índice da linha do cabeçalho.
            padx (int): Margem no eixo X, para ambos os lados.
            pady (int): Margem no eixo Y, para ambos os lados.
        """
        self.grid(column=column, row=row, padx=padx, pady=pady, sticky="NSWE")

    def configure_column(self, column_id: int, weight: int) -> None:
        """Configura uma coluna do contêiner principal.
        Args:
            column_id (int): O índice da coluna.
            weight (int): A área da coluna (valor multiplicativo).
        """
        self.grid_columnconfigure(column_id, weight=weight)

    def configure_row(self, row_id: int, weight: int) -> None:
        """Configura uma linha do contêiner principal.
        Args:
            row_id (int): O índice da linha.
            weight (int): A área da linha (valor multiplicativo).
        """
        self.grid_rowconfigure(row_id, weight=weight)

    def draw_body(self, padx: int, pady: int) -> None:
        """Renderiza os demais contêineres ao contêiner principal.
        Args:
            padx (int): Margem no eixo X, para ambos os lados.
            pady (int): Margem no eixo Y, para ambos os lados.
        """
        # Inicializa o cabeçalho.
        self.header = Header(self)
        # Desenha o cabeçalho no contêiner principal.
        self.header.frame_grid(column=0, row=0, padx=padx, pady=pady)
        # Configura o grid do cabeçalho dentro do contêiner principal.
        self.header.configure_column(column_id=0, weight=0)
        self.header.configure_column(column_id=1, weight=1)
        self.header.configure_row(row_id=0, weight=0)
        self.header.configure_row(row_id=1, weight=1)
        # Renderiza os elementos contidos no cabeçalho.
        self.header.draw_body(padx=padx, pady=pady)

        # Inicializa o corpo.
        self.body = Body(self)
        # Desenha o corpo no contêiner principal.
        self.body.frame_grid(column=0, row=1, padx=padx, pady=pady)
        # Configura o grid do corpo dentro do contêiner principal.
        self.body.configure_column(column_id=0, weight=0)
        self.body.configure_column(column_id=1, weight=1)
        # Renderiza os elementos contidos no corpo.
        self.body.draw_body(padx=padx, pady=pady)

        # Inicializa o rodapé.
        self.footer = Footer(self)
        # Desenha o rodapé no contêiner principal.
        self.footer.frame_grid(column=0, row=2, padx=padx, pady=pady)
        # Renderiza os elementos contidos no rodapé.
        self.footer.draw_body(padx=padx, pady=pady)
