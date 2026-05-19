from typing import Dict, List, Optional
import tkinter
import mimetypes

from ..commondialog import Dialog
from ..widgets.grid_frame import GridFrame

__all__ = ["MimeChooser", "ask_mime"]


class MimeChooser(Dialog):
    def __init__(
        self,
        master: tkinter.Tk = None,
        types_map: Dict[str, str] = None,
        categories: Dict[str, List[str]] = None,
        **kw
    ):
        """Construct a mime picker window with the parent MASTER."""
        self.types_map = mimetypes.types_map.copy()
        self.categories = {
            "Archive": ["application/*"],
            "Audio": ["audio/*"],
            "Document": ["text/*"],
            "Image": ["image/*"],
            "Video": ["video/*"],
        }
        self.VAR = tkinter.StringVar()
        self.CATEGORY = tkinter.StringVar()
        self.SEARCH = tkinter.StringVar()
        Dialog.__init__(self, master, types_map=types_map, categories=categories, **kw)

        # TEMP
        self.minsize(400, 300)
        self.resizable(True, True)
        self.redraw()

    def get(self) -> Optional[str]:
        return None if self.VAR.get() == "" else self.VAR.get()

    def set(self, value: str) -> None:
        self.VAR.set(value)

    def configure(self, **kw) -> None:
        if "types_map" in kw and kw["types_map"] is not None:
            self.types_map = kw.pop("types_map")

        if "categories" in kw and kw["categories"] is not None:
            self.categories = kw.pop("categories")

        if "initialmime" in kw and kw["initialmime"] is not None:
            self.VAR.set(kw.pop("initialmime"))
        Dialog.configure(self, **kw)

    def body(self):
        self.search_icn = tkinter.Label(self, text="search")
        self.search_entry = tkinter.Entry(self, textvariable=self.SEARCH)
        self.search_entry.bind("<KeyRelease>", lambda e: self.redraw())
        self.cat_lst = tkinter.Listbox(self)
        self.cat_lst.bind("<<ListboxSelect>>", self._select)
        self.mime_frm = GridFrame(self, background="green", width=100)

        self.search_icn.grid(row=0, column=0, sticky="w")
        self.search_entry.grid(row=0, column=1, sticky="we")
        self.cat_lst.grid(row=1, column=0, sticky="ns")
        self.mime_frm.grid(row=1, column=1, sticky="nesw")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Add categories
        for cat in self.categories.keys():
            self.cat_lst.insert("end", cat)

    def redraw(self) -> None:
        self.mime_frm.clear()

        items = self.types_map.keys()
        if self.SEARCH.get() != "":
            print("SEARCH", self.SEARCH.get())
            self.cat_lst.grid_forget()
            return
        if self.CATEGORY.get() != "":
            items = []
            types = self.categories.get(self.CATEGORY.get(), [])
            for t in types:
                if t.endswith("/*"):
                    t = t[:-1]
                    for ext, mime in self.types_map.items():
                        if mime.startswith(t):
                            items.append(ext)
                    continue
                items.append(mimetypes.guess_all_extensions(t))

        for ext in items:
            tkinter.Label(self.mime_frm, text=ext[1:].upper())

        self.cat_lst.grid(row=1, column=0, sticky="ns")

    def _select(self, e):
        sel = self.cat_lst.curselection()
        if sel:
            self.CATEGORY.set(self.cat_lst.get(sel[0]))
        self.redraw()


def ask_mime(mimetype=None, **options) -> Optional[str]:
    if mimetype:
        options["initialmime"] = mimetype
    return MimeChooser(**options).show()
