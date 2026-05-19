# TODO
# -
from typing import Self
import tkinter

__all__ = ["Tabview"]


# TODO figure out how it should display each tab.
class Tabview(tkinter.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master)
        self.columns = 0

        self.configure(**kw)

    def configure(self, **kw) -> Self:
        super().configure(**kw)
        return self

    config = configure
