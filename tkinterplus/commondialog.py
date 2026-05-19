from typing import Any
from abc import abstractmethod
import tkinter

__all__ = ["Dialog"]


class Dialog(tkinter.Toplevel):
    def __init__(self, master=None, **kw):
        tkinter.Toplevel.__init__(self, master)
        self.title("File Type")
        self.minsize(300, 100)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.transient(self.master)
        self.withdraw()
        self.configure(**kw)
        self.body()

    @abstractmethod
    def body(self): ...

    @abstractmethod
    def get(self) -> Any: ...

    @abstractmethod
    def set(self, value: Any) -> None: ...

    def show(self):
        self.wm_deiconify()
        self.focus_force()
        self.grab_set()
        self.master.wait_window(self)
        return self.get()
