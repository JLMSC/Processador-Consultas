"""Um canvas customizado, com a possibilidade de
movimentação vertical e horizontal."""

from tkinter import Tk
from tkinter.ttk import Frame
from tkinter import Canvas, Scrollbar

class TreeCanvas(Canvas):
    """Representa um Canvas.

    Args:
        Canvas (Canvas): Um Canvas.
    """

    # O contêiner principal.
    master_container: Frame
    # Os 'scrollbars' vertical e horizontal.
    vscrollbar: Scrollbar
    hscrollbar: Scrollbar

    def __init__(self, master: Tk = None):
        """Inicializa um Canvas em um Frame.

        Args:
            master (Tk, optional): O contêiner a ser
            referenciado durante a inicialização do
            Canvas.
            Valor padrão: 'None'.
        """
        super().__init__(master=master)
        self.master_container = master
        # Adiciona dois 'scrollbars' um vertical e um horizontal.
        self.__configure_scrolls()
        # Adiciona 'binds' a funções de movimentação dos 'scrollbars'.
        self.bind("<ButtonPress-1>", self.scroll_start)
        self.bind("<B1-Motion>", self.scroll_move)

    def __configure_scrolls(self) -> None:
        """Configura dois 'scrollbars' no Canvas, um vertical e um horizontal.
        """
        # Cria os 'scrollbars'.
        self.vscrollbar = Scrollbar(self.master_container, orient="vertical", command=self.yview)
        self.hscrollbar = Scrollbar(self.master_container, orient="horizontal", command=self.xview)
        self.config(xscrollcommand=self.hscrollbar.set, yscrollcommand=self.vscrollbar.set)
        # Deixa os 'scrollbars' invisíveis.
        self.vscrollbar.config(highlightthickness=0, bg=self["bg"])
        self.hscrollbar.config(highlightthickness=0, bg=self["bg"])

    def scroll_start(self, event):
        """Marca a posição atual do Mouse quando 'ButtonPress-1' é acionado.

        Args:
            event (event): Evento relacionado ao Mouse.
        """
        self.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        """Move o Canvas, de acordo com a movimentação do Mouse, 
        sempre que o Mouse for movimentado enquanto 'ButtonPress-1' 
        enquanto acionado.

        Args:
            event (event): Evento relacionado ao Mouse.
        """
        self.scan_dragto(event.x, event.y, gain=1)
