"""Representa um GUI."""

from tkinter.ttk import Style
from tkinter import Tk, PhotoImage

# pylint: disable=import-error
# pylint: disable=no-name-in-module
from GUI.frames.Master import Master

class Application(Tk):
    """Representa uma aplicação.
    Args:
        Tk (Tk): Aplicação top-level.
    """
    # Comprimento e Largura da aplicação.
    width: int
    height: int
    # O tema da aplicação.
    theme: Style
    # Os contêineres da aplicação.
    master_container: Master

    def __init__(self, title: str, width: int = 800, height: int = 600) -> None:
        super().__init__()
        # Define o título da aplicação.
        self.title(title)
        # Define a resolução da aplicação.
        self.width = width
        self.height = height
        self.geometry(f"{self.width}x{self.height}")
        # Desabilita o redimensionamento da aplicação.
        self.resizable(False, False)
        # Define um ícone para a aplicação.
        self.iconphoto(True, PhotoImage(file="source/GUI/assets/icon.png"))
        # Define um tema para a aplicação.
        self.apply_theme("plastik")
        # Configura o contêiner principal da aplicação.
        self.__configure_master_container()
        # Faz a aplicação rodar indefinidamente.
        self.mainloop()

    def apply_theme(self, theme: str) -> None:
        """Define um tema para a aplicação.
        Args:
            theme (str): O tema a ser usado na aplicação.
        """
        self.theme = Style(self)
        self.call("source", f"source/GUI/themes/{theme}/{theme}.tcl")
        self.theme.theme_use(theme)

    def __configure_master_container(self) -> None:
        """Configura o contêiner principal da aplicação."""
        # Configura o grid da aplicação.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Inicializa o contêiner principal.
        self.master_container = Master(self)

        # Desenha o contêiner principal.
        self.master_container.frame_grid(column=0, row=0, padx=0, pady=0)

        # Configura o grid do contêiner principal dentro da aplicação.
        self.master_container.configure_column(column_id=0, weight=1)
        self.master_container.configure_row(row_id=0, weight=1)
        self.master_container.configure_row(row_id=1, weight=0)
        self.master_container.configure_row(row_id=2, weight=0)

        # Renderiza os demais contêineres da aplicação no contêiner principal.
        self.master_container.draw_body(padx=0.01 * self.width, pady=0.01 * self.height)
