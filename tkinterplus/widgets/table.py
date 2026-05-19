import tkinter

__all__ = ["Table"]


class Table(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)

    def header(self, label: str = None) -> None:
        return
