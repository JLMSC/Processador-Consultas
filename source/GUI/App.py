"""Representa um GUI."""

from tkinter.ttk import Style
from tkinter import Tk, PhotoImage

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
