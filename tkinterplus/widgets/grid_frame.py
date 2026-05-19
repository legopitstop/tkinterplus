from typing import Self
import tkinter
import math

from ..util import EventHelper

__all__ = ["GridFrame", "ScrolledGridFrame"]


class GridFrame(tkinter.Frame):
    def __init__(self, master=None, columns: int = None, bg: str = None, **kw):
        super().__init__(master)
        self.columns = 0
        self._row = 0
        self._column = 0

        self._master_width = self.master.winfo_width()

        self.configure(columns=columns, bg=bg, **kw)
        EventHelper.on_resize(self.master, lambda e: self.on_resized(e))

    def clear(self):
        for c in self.winfo_children():
            c.destroy()
        self._row = 0
        self._column = 0

    def configure(self, **kw) -> Self:
        if "columns" in kw and kw["columns"] != None:
            self.columns = kw.pop("columns")
        super().configure(**kw)
        return self

    config = configure

    def _show(self, columns) -> None:
        self._row = 0
        self._column = 0
        for widget in self.winfo_children():
            widget.grid(row=self._row, column=self._column)
            self._column += 1
            if self._column >= columns:
                self._column = 0
                self._row += 1

    def _calc_columns(self) -> int:
        self.master.update_idletasks()
        width = max([widget.winfo_reqwidth() for widget in self.winfo_children()])
        return math.floor(self.master.winfo_width() / width)

    def on_resized(self, e) -> None:
        if self.columns <= 0:
            self._show(self._calc_columns())
        else:
            self._show(self.columns)


class ScrolledGridFrame(tkinter.Frame):
    def __init__(self, master, columns: int = 0, bg=None):
        """Construct a scrolledframe widget with the parent MASTER."""
        self.master = master
        self._container = tkinter.Frame(master)

        self._canvas = tkinter.Canvas(
            self._container, bd=0, highlightthickness=0, bg=bg
        )
        self._canvas.bind("<Enter>", self._on_enter)
        self._canvas.bind("<Leave>", self._on_leave)

        self._scrollbar = tkinter.Scrollbar(
            self._container, orient="vertical", command=self._canvas.yview
        )
        self.frame = GridFrame(self._canvas, columns=columns, bg=bg)
        self.frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )
        self._canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self._scrollbar.pack(side=tkinter.RIGHT, fill="y")

        # Arguments for tk
        self.children = self.frame.children
        self.tk = self.frame.tk
        self._w = self.frame._w
        self._last_child_ids = self.frame._last_child_ids

        self._container.bind("<Configure>", lambda e: self.update())

    def _on_mouse_wheel(self, e: tkinter.Event) -> None:
        self._canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def _on_enter(self, e: tkinter.Event) -> None:
        self._canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _on_leave(self, e: tkinter.Event) -> None:
        self._canvas.unbind_all("<MouseWheel>")

    # Default Tk
    def pack_configure(self, **kw) -> None:
        """Pack a widget in the parent widget."""
        self._container.pack_configure(**kw)

    pack = pack_configure

    def grid_configure(self, **kw) -> None:
        """osition a widget in the parent widget in a grid."""
        self._container.grid_configure(**kw)

    grid = grid_configure

    def place_configure(self, **kw) -> None:
        """Place a widget in the parent widget."""
        self._container.place_configure(**kw)

    place = place_configure

    def destroy(self) -> None:
        """Destroy this and all descendants widgets."""
        self._container.destroy()

    def bind_all(self, sequence: str, func, add: bool = None) -> None:
        """Bind to all widgets at an event SEQUENCE a call to function FUNC."""
        self.frame.bind_all(sequence, func, add)
        self._canvas.bind_all(sequence, func, add)

    def unbind_all(self, sequence: str) -> None:
        """Unbind for all widgets for event SEQUENCE all functions."""
        self.frame.unbind_all(sequence)
        self._canvas.unbind_all(sequence)

    def bind(self, sequence: str, func, add: bool = None) -> None:
        """Bind to this widget at event SEQUENCE a call to function FUNC."""
        self.frame.bind(sequence, func, add)
        self._canvas.bind(sequence, func, add)

    def unbind(self, sequence: str, funcid: str = None) -> None:
        """Unbind for this widget for event SEQUENCE the function identified with FUNCID."""
        self.frame.unbind(sequence, funcid)
        self._canvas.unbind(sequence, funcid)

    def update(self) -> None:
        self.frame.configure(width=self._container.winfo_width())
        self.frame.configure(height=self._container.winfo_height())
        return super().update()
