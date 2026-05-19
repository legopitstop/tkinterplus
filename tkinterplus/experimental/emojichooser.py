from typing import Self
from tkinter.simpledialog import _setup_dialog, _place_window
import tkinter
import emoji

from .. import setWinStyle
from ..widgets.grid_frame import ScrolledGridFrame

__all__ = ["Dialog", "Chooser", "askemoji"]


class Dialog(tkinter.Toplevel):
    def __init__(self, parent: tkinter.Tk, title: str):
        """
        Initialize a dialog.

        :param parent: A parent window (the application window)
        :type parent: tkinter.Tk
        :param title: The dialog title
        :type title: str
        """
        tkinter.Toplevel.__init__(self, parent)
        setWinStyle(self)

        self.withdraw()  # remain invisible for now
        # If the parent is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent is not None and parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        _setup_dialog(self)

        self.parent = parent

        self.result = None

        body = tkinter.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if self.initial_focus is None:
            self.initial_focus = self

        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        _place_window(self, parent)

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def destroy(self) -> None:
        """Destroy the window"""
        self.initial_focus = None
        super().destroy()
        tkinter._destroy_temp_root(self.master)

    def body(self, master) -> None:
        """create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        """
        pass

    def buttonbox(self) -> None:
        """add standard button box.

        override if you do not want the standard buttons
        """

        box = tkinter.Frame(self)

        w = tkinter.Button(box, text="OK", width=10, command=self.ok, default="active")
        w.pack(side="left", padx=5, pady=5)
        w = tkinter.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None) -> None:

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self, event=None) -> None:
        self.destroy()

    #
    # command hooks

    def validate(self) -> int:
        """validate the data

        This method is called automatically to validate the data before the
        dialog is destroyed. By default, it always validates OK.
        """

        return 1  # override

    def apply(self) -> None:
        """process the data

        This method is called automatically to process the data, *after*
        the dialog is destroyed. By default, it does nothing.
        """

        pass  # override


# Using canvas and the cached emojis from Windows render it.
# C:\Windows\SystemApps\MicrosoftWindows.Client.CBS_cw5n1h2txyewy\InputApp\Assets\Fonts
# Emoji Panel
# https://github.com/microsoft/fluentui-emoji
class EmojiChooser(Dialog):
    def __init__(self, parent, **options):
        self._query = tkinter.StringVar()
        super().__init__(parent, "Emoji")

    def body(self, master) -> None:
        search = tkinter.Entry(master, textvariable=self._query)
        search.bind("<KeyRelease>", lambda e: self.render())
        search.pack(expand=1, fill="x")

        # self._emojis = ScrolledGridFrame(master)
        # self._emojis.pack(expand=1, fill="both")

        self._emojis = tkinter.Canvas(master)
        self.render()
        self._emojis.pack(expand=1, fill="both")

    def render(self) -> None:
        for c in self._emojis.winfo_children():
            c.destroy()
        res = self.get_emojis()
        if not res:
            tkinter.Label(self._emojis, text="No search results")
            return

        c = 10
        for k in res:
            # tkinter.Label(self._emojis, text=str(k))
            self._emojis.create_text(10, c, text=k, fill="black", font=("Helvetica"))
            c += 10

    def get_emojis(self) -> list[str]:
        def search(v: dict):
            return v["status"] == 2 and query in v["en"]

        query = self._query.get()
        all = [k for k, v in emoji.EMOJI_DATA.items() if search(v)]
        return all

    def _fixresult(self) -> str:
        return emoji.emojize(str(self.result), language="alias"), str(self.result)


def askemoji(emoji=None, **options) -> str:
    """Display dialog window for selection of an emoji.

    Convenience wrapper for the Chooser class.  Displays the emoji
    chooser dialog with emoji as the initial value.

    Returns
    ---
    (emoji, name)
    """
    if "parent" not in options:
        options["parent"] = tkinter._get_temp_root()

    if emoji:
        options = options.copy()
        options["initialemoji"] = emoji

    return EmojiChooser(**options)._fixresult()
