# TODO
# -
from typing import Self
import tkinter
import emoji

from .. import emojichooser
from ... import Icon, Picturebox

__all__ = ["EmojiButton", "IconButton"]


class EmojiButton(tkinter.Frame):
    def __init__(
        self, master: tkinter.Tk, variable: tkinter.StringVar = None, command=None, **kw
    ):
        super().__init__(master)
        self.variable = tkinter.StringVar()
        self.command = None
        self.display = tkinter.StringVar()

        self.variable.trace_add("write", self.__write)

        # Widget
        self.button = tkinter.Button(
            self, textvariable=self.display, command=self.__callback
        )
        self.button.pack(expand=1, fill=tkinter.BOTH)

        self.configure(variable=variable, command=command, **kw)

    def __callback(self) -> None:
        print("callback")
        emoji = emojichooser.askemoji(parent=self)[1]
        if emoji != None:
            # self.variable.set(emoji)
            if self.command != None:
                self.command()

    def __write(self, a, b, c) -> None:
        value = self.variable.get()
        e = emoji.emojize(value, language="alias")
        self.display.set(e)

    def configure(self, **kw) -> Self:
        if "variable" in kw and kw["variable"] != None:
            self.variable: tkinter.StringVar = kw.pop("variable")
            self.variable.trace_add("write", self.__write)
        if "command" in kw and kw["command"] != None:
            self.command = kw.pop("command")
        return self

    config = configure

    def focus_set(self) -> None:
        self.button.focus_set()
        self.__callback()

    focus = focus_set


# TODO This could just be a tkinterplus.Picture but has a command bind.
class IconButton(Picturebox):
    def __init__(
        self,
        master: tkinter.Tk = None,
        icon: Icon = None,
        command=None,
        state: str = None,
        **kw
    ):
        super().__init__(master)
        self.icon = None
        self.command = None
        self.state = "normal"
        self.textvariable = tkinter.StringVar()

        self.bind("<Button-1>", self._callback)

        self.configure(icon=icon, command=command, state=state, **kw)

    def _callback(self, e: tkinter.Event) -> None:
        if self.command != None and self.state == "normal":
            self.command()

    def configure(self, **kw) -> Self:
        if "image" in kw:
            kw.pop("image")
        if "icon" in kw and kw["icon"] != None:
            self.icon = kw.pop("icon")
            super().configure(image=self.icon.image)
        if "command" in kw and kw["command"] != None:
            self.command = kw.pop("command")
        if "state" in kw and kw["state"] != None:
            self.state = kw.pop("state")

        super().configure(**kw)
        return self

    config = configure
