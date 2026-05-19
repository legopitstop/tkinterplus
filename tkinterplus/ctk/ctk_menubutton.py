import customtkinter
from .ctk_menu import CTkMenu

__all__ = ["CTkMenubutton"]


class CTkMenubutton(customtkinter.CTkButton):
    def __init__(self, master, text: str = None, menu: CTkMenu = None):
        super().__init__(master, text="CTkMenubutton", command=self.popup)
        self.menu = None
        self.configure(menu=menu, text=text)

    def popup(self):
        if self.menu != None:
            x = self.master.winfo_x() + self.winfo_x()
            y = self.master.winfo_y() + self.winfo_y()
            self.menu.tk_popup(x, y)

    def configure(self, **kw):
        if "menu" in kw and kw["menu"] != None:
            self.menu = kw["menu"]
        if "text" in kw and kw["text"] != None:
            self.configure(text=kw["text"])

    config = configure
