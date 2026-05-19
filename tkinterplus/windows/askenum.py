import tkinter
from typing import Optional

from .. import Footer

__all__ = ["AskEnum", "askenum"]


class AskEnum(tkinter.Toplevel):
    def __init__(
        self,
        master: Optional[tkinter.Tk] = None,
        title: Optional[str] = None,
        prompt: Optional[str] = None,
        default: Optional[str] = None,
        value: Optional[list[str]] = None,
        *values: str
    ):
        """Construct a askenum widget with the parent MASTER."""
        tkinter.Toplevel.__init__(self, master)
        self.minsize(300, 50)
        self.resizable(False, False)
        self.VAR = tkinter.StringVar()

        if title is not None:
            self.title(title)
        elif master is not None:
            self.title(master.title())

        # Default value
        if default is not None:
            self.VAR.set(default)
        else:
            self.VAR.set(value[0])

        tkinter.Label(self, text=prompt).grid(row=0, column=0, sticky=tkinter.W)
        tkinter.OptionMenu(self, self.VAR, *value).grid(row=1, column=0)

        # Footer
        foot = Footer(self)
        foot.add_button(text="Confirm", command=self._confirm)
        foot.add_button(text="Cancel", command=self._cancel)

    def _confirm(self) -> None:
        print(self.VAR.get())
        self.destroy()

    def _cancel(self) -> None:
        print(False)
        self.destroy()


def askenum(title: str, prompt: str, default: str, value: list, *values) -> str:
    return AskEnum(
        title=title, prompt=prompt, default=default, value=value, *values
    ).VAR.get()
