import tkinter
from customtkinter import CTkLabel, CTkToplevel, CTkCheckBox, CTkRadioButton

# test = tkinter.Menu()
# test.add_command()

__all__ = ["CTkMenuItem"]


class CTkMenuItem:
    def __init__(self, itemType: str, id: int, label: str = None, menu=None, **kw):
        self.id = id
        self.itemType = itemType
        self.label = "CTkMenuItem"
        self.menu = None
        self.command = None

        self.configure(label=label, menu=menu, **kw)

    def configure(self, **kw):
        if "label" in kw and kw["label"] != None:
            self.label = kw.pop("label")
        if "menu" in kw and kw["menu"] != None:
            self.menu = kw.pop("menu")
        if "command" in kw and kw["command"] != None:
            self.command = kw.pop("command")
        return self

    config = configure


class CTkMenu:
    def __init__(self, master=None):
        self.master = master
        self.__children = []
        self.__toplevel = CTkToplevel(fg_color="black")
        self.__toplevel.overrideredirect(True)
        # self.__toplevel.bind('<FocusOut>', lambda e: self.unpost())
        self.unpost()

    def add(self, itemType, kw):
        """Internal function."""
        item = CTkMenuItem(itemType, len(self.__children) + 1, **kw)
        self.__children.append(item)
        return item.id

    def add_cascade(self, **kw):
        return self.add("cascade", kw)

    def add_checkbutton(self, **kw):
        return self.add("checkbutton", kw)

    def add_command(self, **kw):
        return self.add("command", kw)

    def add_radiobutton(self, **kw):
        return self.add("radiobutton", kw)

    def add_separator(self, **kw):
        return self.add("separator", kw)

    def tk_popup(self, x: int, y: int, entry: str = ""):
        self.post(x, y)

    # TODO

    def insert(self, index, itemType, cnf={}, **kw):
        """Internal function."""
        pass

    def insert_cascade(self, index, **kw):
        """Add hierarchical menu item at INDEX."""
        self.insert(index, "cascade", kw)

    def insert_checkbutton(self, index, **kw):
        """Add checkbutton menu item at INDEX."""
        self.insert(index, "checkbutton", kw)

    def insert_command(self, index, **kw):
        """Add command menu item at INDEX."""
        self.insert(index, "command", kw)

    def insert_radiobutton(self, index, **kw):
        """Add radio menu item at INDEX."""
        self.insert(index, "radiobutton", kw)

    def insert_separator(self, index, **kw):
        """Add separator at INDEX."""
        self.insert(index, "separator", kw)

    def delete(self, index1, index2=None):
        """Delete menu items between INDEX1 and INDEX2 (included)."""
        pass

    def entrycget(self, index, option):
        """Return the resource value of a menu item for OPTION at INDEX."""
        return

    def entryconfigure(self, index, cnf=None, **kw):
        """Configure a menu item at INDEX."""
        return

    entryconfig = entryconfigure

    def grab_release(self):
        pass

    def index(self, index):
        """Return the index of a menu item identified by INDEX."""
        return

    def invoke(self, index):
        """Invoke a menu item identified by INDEX and execute
        the associated command."""
        return

    def post(self, x, y):
        """Display a menu at position X,Y."""

        def click(itemType, value):
            match itemType:
                case "command":
                    value()
                    self.unpost()

        def on_enter(value):
            x = self.__toplevel.winfo_x() + self.__toplevel.winfo_width()
            y = self.__toplevel.winfo_y()
            value.tk_popup(x, y)

        for c in self.__toplevel.winfo_children():
            c.destroy()
        for i in self.__children:
            match i.itemType:
                case "command":
                    item = CTkLabel(self.__toplevel, text=i.label)
                    if i.command != None:
                        item.bind(
                            "<Button-1>", lambda e, c=i.command: click("command", c)
                        )
                    item.pack(expand=1, fill="x", padx=20)

                case "cascade":
                    item = CTkLabel(self.__toplevel, text=i.label)
                    if i.menu != None:
                        item.bind("<Enter>", lambda e, m=i.menu: on_enter(m))
                    item.pack(expand=1, fill="x", padx=20)

                case "checkbutton":
                    item = CTkCheckBox(self.__toplevel, text=i.label)
                    if i.menu != None:
                        item.bind("<Button-1>", lambda e, m=i.menu: click("cascade", m))
                    item.pack(expand=1, fill="x", padx=20)

                case "radiobutton":
                    item = CTkRadioButton(self.__toplevel, text=i.label)
                    if i.menu != None:
                        item.bind("<Button-1>", lambda e, m=i.menu: click("cascade", m))
                    item.pack(expand=1, fill="x", padx=20)

        self.__toplevel.geometry(f"+{x}+{y}")
        self.__toplevel.deiconify()

    def type(self, index):
        """Return the type of the menu item at INDEX."""
        return

    def unpost(self):
        """Unmap a menu."""
        if isinstance(self.master, CTkMenu):
            self.master.unpost()
        self.__toplevel.withdraw()

    def xposition(self, index):
        """Return the x-position of the leftmost pixel of the menu item
        at INDEX."""
        return

    def yposition(self, index):
        """Return the y-position of the topmost pixel of the menu item at INDEX."""
        return
