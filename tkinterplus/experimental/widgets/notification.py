# TODO
# - Implement animations

from typing import Self
from tkinter import (
    ACTIVE,
    BOTH,
    NORMAL,
    NW,
    Tk,
    StringVar,
    Frame,
    Label,
    _get_temp_root,
)

__all__ = ["Notification"]


class Notification:
    def __init__(
        self,
        master: Tk = None,
        text: str = None,
        textvariable: StringVar = None,
        state: str = None,
        anchor: str = None,
        bg: str = None,
        fg: str = None,
        **kw,
    ):
        if master is None:
            master = _get_temp_root()

        # Arguments
        self.master = master
        self.textvariable = StringVar()
        self.state = NORMAL
        self.anchor = NW
        self.bg = "black"
        self.fg = "white"
        self.x = 0
        self.y = 0

        # Subwidgets
        self.frame = Frame(self.master, bg=self.bg, cursor="hand2")
        self._text = Label(
            self.frame,
            textvariable=self.textvariable,
            bg=self.bg,
            fg=self.fg,
            padx=10,
            pady=10,
        )
        self._text.pack(expand=True, fill=BOTH)

        self.configure(
            text=text,
            textvariable=textvariable,
            state=state,
            anchor=anchor,
            bg=bg,
            fg=fg,
            **kw,
        )

        # Arguments for tk
        self.children = self.frame.children
        self.tk = self.frame.tk
        self._w = self.frame._w

    def show(self, anchor: str = None, ms: int = 500, hide_after: int = None) -> Self:
        """
        Show the notification

        :param anchor: The position to show the notification, defaults to None
        :type anchor: str, optional
        :param ms: Duration of the animation, defaults to 500
        :type ms: int, optional
        :param hide_after: The time (in miliseconds) to hide the notification, defaults to None
        :type hide_after: int, optional
        :rtype: Notification
        """
        if self.state == NORMAL:
            pos = [x for x in anchor]
            self.configure(state=ACTIVE)
            self.frame.place(x=0, y=0)
            self.frame.update_idletasks()
            for c in pos:
                match c:
                    case "n":
                        self.y = -10
                    case "s":
                        self.y = (
                            self.master.winfo_height() - self.frame.winfo_height()
                        ) - 10
                    case "e":
                        self.x = (
                            self.master.winfo_width() - self.frame.winfo_width()
                        ) - 10
                    case "w":
                        self.x = -10
            self.frame.place(x=self.x, y=self.y)
            if hide_after != None:
                self.frame.after(hide_after, lambda: self.hide(ms))
        return self

    def hide(self, ms: int = 500) -> Self:
        """
        Hide the notification

        :param ms: Duration of the animation, defaults to 500
        :type ms: int, optional
        :rtype: Notification
        """
        if self.state == ACTIVE:
            self.configure(state=NORMAL)
            # self._slide(-100, 1, X, ms)
            self.frame.place_forget()
        return self

    def configure(self, **kw) -> Self:
        if "text" in kw and kw["text"] != None:
            self.textvariable.set(kw.pop("text"))
        if "textvariable" in kw and kw["textvariable"] != None:
            self.textvariable = kw.pop("textvariable")
            self._text.configure(textvariable=self.textvariable)

        if "state" in kw and kw["state"] != None:
            self.state = kw.pop("state")

        if "bg" in kw and kw["bg"] != None:
            self.bg = kw.pop("bg")
            self.frame.configure(bg=self.bg)
            self._text.configure(bg=self.bg)

        if "fg" in kw and kw["fg"] != None:
            self.fg = kw.pop("fg")
            self._text.configure(fg=self.fg)

        if "anchor" in kw and kw["anchor"] != None:
            anchor = kw.pop("anchor")
            values = ["n", "e", "s", "w", "ne", "nw", "se", "sw", "center"]
            if anchor in values:
                self.anchor = anchor
                if self.anchor == "center":
                    self.x = 0
                    self.y = 0
                else:
                    self.master.update()
                    for k in self.anchor:
                        if k == "n":
                            self.y0 = -100
                            self.y1 = -8
                        elif k == "s":
                            self.y0 = -100
                            self.y1 = self.master.winfo_height() - 100

                        elif k == "e":
                            self.x0 = -100
                            self.x1 = self.master.winfo_width() - 100
                        elif k == "w":
                            self.x0 = -100
                            self.x1 = -8
            else:
                KeyError("Expected %s" % values)
        return self

    config = configure
