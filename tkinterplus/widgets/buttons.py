from typing import Self, Callable
from tkinter import filedialog
from tkinter import colorchooser
import tkinter
import os

from . import Tooltip
from ..util import text_color

__all__ = ["FileButton", "DirectoryButton", "ColorButton", "BindButton"]


class FileButton(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        text: str = None,
        variable: tkinter.StringVar = None,
        command: Callable = None,
        **kw
    ):
        """
        Construct a file button widget with the parent MASTER.

        :param master: _description_
        :type master: tkinter.Tk
        :param text: _description_, defaults to None
        :type text: str, optional
        :param variable: _description_, defaults to None
        :type variable: tkinter.StringVar, optional
        :param command: _description_, defaults to None
        :type command: _type_, optional
        """
        super().__init__(master)
        self.variable = tkinter.StringVar()
        self.tip = tkinter.StringVar()
        self.tip.set("No file chosen")
        self.display = tkinter.StringVar()
        self.display.set("No file chosen")
        self.text = "Choose File"
        self.command = None

        self.variable.trace_add("write", self.__write)

        self.button = tkinter.Button(self, text=self.text, command=self.__callback)
        self.label = tkinter.Label(self, textvariable=self.display)
        self.label.bind("<Button-1>", lambda e: self.__callback())
        self.button.pack(expand=1, fill="x", side="left")
        self.label.pack(expand=1, fill="x", side="right")
        Tooltip(self.label, textvariable=self.tip)

        self.configure(variable=variable, command=command, text=text, **kw)

    def __callback(self) -> None:
        path = filedialog.askopenfilename(
            initialdir=os.path.dirname(self.variable.get()),
            initialfile=os.path.basename(self.variable.get()),
            parent=self,
            title=self.text,
        )
        if path != "":
            self.variable.set(path)
            if self.command != None:
                self.command()

    def __write(self, a, b, c) -> None:
        value = self.variable.get()
        self.tip.set(value)
        self.display.set(os.path.basename(value))

    def focus_set(self) -> None:
        self.button.focus_set()
        self.__callback()

    focus = focus_set

    def configure(self, **kw) -> Self:
        if "variable" in kw and kw["variable"] != None:
            self.variable: tkinter.StringVar = kw.pop("variable")
            self.variable.trace_add("write", self.__write)
        if "text" in kw and kw["text"] != None:
            self.text = kw.pop("text")
            self.button.configure(text=self.text)
        if "command" in kw and kw["command"] != None:
            self.command = kw.pop("command")

        remove = ["textvariable"]
        for k in remove:
            if k in kw:
                kw.pop(k)
        self.button.configure(**kw)
        self.label.configure(**kw)
        return self

    config = configure

    def get(self) -> str:
        return self.variable.get()

    def set(self, value: str) -> None:
        return self.variable.set(value)


class DirectoryButton(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        text: str = None,
        variable: tkinter.StringVar = None,
        command=None,
        **kw
    ):
        """
        Construct a directory button widget with the parent MASTER.

        :param master: _description_
        :type master: tkinter.Tk
        :param text: _description_, defaults to None
        :type text: str, optional
        :param variable: _description_, defaults to None
        :type variable: tkinter.StringVar, optional
        :param command: _description_, defaults to None
        :type command: _type_, optional
        """
        super().__init__(master)
        self.variable = tkinter.StringVar()
        self.tip = tkinter.StringVar()
        self.tip.set("No Directory chosen")
        self.display = tkinter.StringVar()
        self.display.set("No Directory chosen")
        self.text = "Choose Directory"
        self.command = None

        self.variable.trace_add("write", self.__write)

        self.button = tkinter.Button(self, text=self.text, command=self.__callback)
        self.label = tkinter.Label(self, textvariable=self.display)
        self.label.bind("<Button-1>", lambda e: self.__callback())
        self.button.pack(expand=1, fill="x", side="left")
        self.label.pack(expand=1, fill="x", side="right")
        Tooltip(self.label, textvariable=self.tip)

        self.configure(variable=variable, command=command, text=text, **kw)

    def __write(self, a, b, c) -> None:
        value = self.variable.get()
        self.tip.set(value)
        self.display.set(os.path.basename(value))

    def __callback(self) -> None:
        path = filedialog.askdirectory(
            initialdir=self.variable.get(), parent=self, title=self.text
        )
        if path != "":
            self.variable.set(path)
            if self.command != None:
                self.command()

    def configure(self, **kw) -> Self:
        if "variable" in kw and kw["variable"] != None:
            self.variable: tkinter.StringVar = kw.pop("variable")
            self.variable.trace_add("write", self.__write)
        if "text" in kw and kw["text"] != None:
            self.text = kw.pop("text")
            self.button.configure(text=self.text)
        if "command" in kw and kw["command"] != None:
            self.command = kw.pop("command")
        remove = ["textvariable"]
        for k in remove:
            if k in kw:
                kw.pop(k)
        self.button.configure(**kw)
        self.label.configure(**kw)
        return self

    config = configure

    def focus_set(self) -> None:
        self.button.focus_set()
        self.__callback()

    focus = focus_set

    def get(self) -> str:
        return self.variable.get()

    def set(self, value: str) -> None:
        return self.variable.set(value)


class ColorButton(tkinter.Frame):
    def __init__(
        self, master: tkinter.Tk, variable: tkinter.StringVar = None, command=None, **kw
    ):
        """
        Construct a color button widget with the parent MASTER.

        :param master: _description_
        :type master: tkinter.Tk
        :param variable: _description_, defaults to None
        :type variable: tkinter.StringVar, optional
        :param command: _description_, defaults to None
        :type command: _type_, optional
        """
        super().__init__(master)
        self.variable = tkinter.StringVar()
        self.variable.set("#f8f8f8")
        self.display = tkinter.StringVar()
        self.command = None

        self.variable.trace_add("write", self.__write)

        # Widget
        self.button = tkinter.Button(
            self,
            textvariable=self.variable,
            bg=self.variable.get(),
            activebackground=self.variable.get(),
            command=self.__callback,
        )
        self.button.pack(expand=1, fill=tkinter.BOTH)

        self.configure(variable=variable, command=command, **kw)

    def __callback(self) -> None:
        color = colorchooser.askcolor(parent=self)[1]
        if color != None:
            self.variable.set(color)
            if self.command != None:
                self.command()

    def __write(self, a, b, c) -> None:
        color = self.variable.get()
        if not color.startswith("#"):
            rgb = self.winfo_rgb(color)
            r, g, b = [x >> 8 for x in rgb]
            hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
            self.variable.set(hex)

        self.button.configure(bg=color, fg=text_color(color), activebackground=color)

    def configure(self, **kw) -> Self:
        if "variable" in kw and kw["variable"] != None:
            self.variable: tkinter.StringVar = kw.pop("variable")
            self.button.configure(textvariable=self.variable)
            self.variable.trace_add("write", self.__write)

        if "command" in kw and kw["command"] != None:
            self.command = kw.pop("command")

        remove = ["textvariable", "bg", "background", "fg", "foreground"]
        for k in remove:
            if k in kw:
                kw.pop(k)
        self.button.configure(**kw)

        return self

    config = configure

    def focus_set(self) -> None:
        self.button.focus_set()
        self.__callback()

    focus = focus_set

    def get(self) -> str:
        return self.variable.get()

    def set(self, value: str) -> None:
        return self.variable.set(value)


class BindButton(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        variable: tkinter.StringVar = None,
        seperator: str = None,
        command=None,
        bindcommand=None,
        bind_all: bool = False,
        **kw
    ):
        """
        Construct a bind button widget with the parent MASTER.

        :param master: _description_
        :type master: tkinter.Tk
        :param variable: _description_, defaults to None
        :type variable: tkinter.StringVar, optional
        :param seperator: _description_, defaults to None
        :type seperator: str, optional
        :param command: _description_, defaults to None
        :type command: _type_, optional
        :param bindcommand: _description_, defaults to None
        :type bindcommand: _type_, optional
        :param bind_all: _description_, defaults to False
        :type bind_all: bool, optional
        """
        super().__init__(master)
        self.variable = tkinter.StringVar()
        self.command = None
        self._button_variable = tkinter.StringVar()
        self.seperator = "+"
        self.bindcommand = None
        self._bind_all = False

        # Widget
        self.button = tkinter.Button(
            self,
            textvariable=self._button_variable,
            disabledforeground="black",
            command=self.listen,
        )
        self.button.pack(expand=1, fill=tkinter.BOTH)

        self.configure(
            variable=variable,
            command=command,
            seperator=seperator,
            bindcommand=bindcommand,
            bind_all=bind_all,
            **kw
        )

    def _seq(self, e: tkinter.Event) -> str:
        # 0x0001 Shift
        # 0x0002 caps Lock
        # 0x0004 Control
        # 0x0008 left alt
        # 0x0010 num lock
        # 0x0080 right alt
        # 0x0100 mouse 1
        # 0x0200 mouse 2
        # 0x0400 mouse 3
        seq = []
        if (e.state & 0x0004) > 0:
            seq.append("Control")
        if e.keysym == "Control_L" or e.keysym == "Control_R":
            return "<" + e.keysym + ">"
        else:
            seq.append(e.keysym)
        return "<" + "-".join(seq) + ">"

    def _display(self, seq: str) -> str:
        keys = seq.replace("<", "").replace(">", "").split("-")
        res = []
        for k in keys:
            if len(k) == 1 and k.isupper():
                res.append("Shift")
                res.append(k.lower())
            else:
                res.append(k)
        return self.seperator.join(res)

    def callback(self, e: tkinter.Event) -> None:
        old = self.variable.get()
        new = self._seq(e)
        self.variable.set(new)
        self.button.configure(state=tkinter.NORMAL)
        self.master.unbind_all("<KeyRelease>")

        if self.bindcommand is not None:
            if self._bind_all:
                self.master.unbind_all(old)
                self.master.bind_all(new, self.bindcommand)
            else:
                self.master.unbind(old)
                self.master.bind(new, self.bindcommand)

        if self.command != None:
            self.command()

    def listen(self) -> None:
        self.button.configure(state=tkinter.DISABLED)
        self._button_variable.set("> <")
        res = self.master.bind_all("<KeyRelease>", self.callback)
        print(res)

    def configure(self, **kw) -> Self:
        if "variable" in kw and kw["variable"] is not None:
            self.variable: tkinter.StringVar = kw.pop("variable")
            self.variable.trace_add(
                "write",
                lambda a, b, c: self._button_variable.set(
                    self._display(self.variable.get())
                ),
            )  # update btn text
            self._button_variable.set(self._display(self.variable.get()))
        if "bind_all" in kw and kw["bind_all"] is not None:
            self._bind_all = kw.pop("bind_all")
        if "bindcommand" in kw and kw["bindcommand"] is not None:
            self.bindcommand = kw.pop("bindcommand")
        if "command" in kw and kw["command"] is not None:
            self.command = kw.pop("command")
        if "seperator" in kw and kw["seperator"] is not None:
            self.seperator = kw.pop("seperator")

        remove = ["textvariable"]
        for k in remove:
            if k in kw:
                kw.pop(k)
        self.button.configure(**kw)
        return self

    config = configure

    def focus_set(self) -> None:
        self.button.focus_set()
        self.listen()

    focus = focus_set

    def get(self) -> str:
        return self.variable.get()

    def set(self, value: str) -> None:
        return self.variable.set(value)
