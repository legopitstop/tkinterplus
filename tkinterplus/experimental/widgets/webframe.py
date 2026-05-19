# TODO
# -
from typing import Self
from tkinter.scrolledtext import ScrolledText
from typing import Union
import tkinter
import requests

__all__ = ["WebFrame"]


# from tkinterweb import HtmlFrame
class WebFrame(tkinter.Frame):
    def __init__(
        self,
        master=None,
        src: str = None,
        srcdoc: str = None,
        width: int = None,
        height: int = None,
        allowfullscreen: bool = None,
        sandbox: str = None,
        cache: Union[str, bool] = None,
        context_menu: bool = True,
        **kw
    ):
        super().__init__(master)
        self.src = None
        self.srcdoc = None
        self.allowfullscreen = False
        self.sandbox = ""
        self.cache = True
        self.context_menu = True
        self.__elements = ""
        self.__dev_tools = None
        self.__page_source = None

        self.canvas = tkinter.Canvas(self, bg="red")
        self.canvas.pack(expand=1, fill="both")

        # Context menu
        self.__menu = tkinter.Menu(self, tearoff=False)
        self.__menu.add_command(label="Reload (Ctrl-R)", command=self.reload)
        self.__menu.add_separator()
        self.__menu.add_command(label="Save as... (Ctrl-S)", command=self.save)
        self.__menu.add_command(label="Print... (Ctrl-P)", command=self.print)
        self.__menu.add_separator()
        self.__menu.add_command(
            label="View Page Source (Ctrl-U)", command=self.view_page_source
        )
        self.__menu.add_command(label="Inspect", command=self.developer_tools)

        # Binds
        self.canvas.bind("<Control-r>", lambda e: self.reload())
        self.canvas.bind("<Control-s>", lambda e: self.save())
        self.canvas.bind("<Control-p>", lambda e: self.print())
        self.canvas.bind("<Control-u>", lambda e: self.view_page_source())
        self.canvas.bind("<Control-C>", lambda e: self.developer_tools())

        self.configure(
            src=src,
            srcdoc=srcdoc,
            width=width,
            height=height,
            allowfullscreen=allowfullscreen,
            sandbox=sandbox,
            cache=cache,
            context_menu=context_menu,
            **kw
        )

    # unique methods

    def developer_tools(self) -> Self:
        """Open developer tools window"""

        def destroy():
            self.__dev_tools.destroy()
            self.__dev_tools = None

        if self.__dev_tools == None:
            pass
        # TODO
        # self.__dev_tools = DeveloperTools(self.master)
        # self.__dev_tools.protocol('WM_DELETE_WINDOW', destroy)

        else:
            destroy()
        return self

    def view_page_source(self) -> Self:
        """Open view page source window"""
        WRAP = tkinter.StringVar()
        WRAP.set("word")

        def destroy():
            self.__page_source.destroy()
            self.__page_source = None

        def wrap():
            source.configure(wrap=WRAP.get())

        if self.__page_source == None:
            self.__page_source = tkinter.Toplevel(self.master)
            self.__page_source.protocol("WM_DELETE_WINDOW", destroy)
            self.__page_source.title("View Page Source")
            self.__page_source.attributes("-topmost", True, "-toolwindow", True)

            checkbox = tkinter.Checkbutton(
                self.__page_source,
                text="Word Wrap",
                variable=WRAP,
                onvalue="word",
                offvalue="none",
                command=wrap,
            )
            checkbox.pack(anchor=tkinter.W)

            source = ScrolledText(self.__page_source, wrap="word")
            source.pack(expand=1, fill="both")
            source.insert(0.0, self.srcdoc)
            source.configure(state=tkinter.DISABLED)

        else:
            destroy()
        return self

    def render(self) -> Self:
        """Render the page"""
        if self.srcdoc != None:
            self.canvas.create_line(0, 0, 100, 100)

        else:
            raise ValueError(
                "Cannot render doc as SRCDOC is not defined! You must define a SRC or the SRCDOC in html"
            )
        return self

    def reload(self) -> Self:
        """Reload this page"""
        print("reload")
        self.canvas.delete("all")
        self.render()
        return self

    def save(self) -> Self:
        """Save page as"""
        print("save page")
        return self

    def print(self) -> Self:
        """Print page"""
        print("print page")
        return self

    def open_menu(self, e: tkinter.Event) -> Self:
        self.__menu.tk_popup(e.x, e.y)
        self.__menu.grab_release()
        return self

    # default widget methods

    def configure(self, **kw) -> Self:
        if "src" in kw and kw["src"] != None:
            self.src = kw.pop("src")
            html = requests.get(self.src, allow_redirects=True)
            self.srcdoc = html.content

        if "srcdoc" in kw and kw["srcdoc"] != None:
            self.srcdoc = kw.pop("srcdoc")

        if "allowfullscreen" in kw and kw["allowfullscreen"] != None:
            self.allowfullscreen = kw.pop("allowfullscreen")
        if "sandbox" in kw and kw["sandbox"] != None:
            self.sandbox = kw.pop("sandbox")
        if "cache" in kw and kw["cache"] != None:
            self.cache = kw.pop("cache")
        if "context_menu" in kw and kw["context_menu"] != None:
            self.context_menu = kw.pop("context_menu")
            if self.context_menu:
                self.canvas.bind("<Button-3>", self.open_menu)
            else:
                self.canvas.unbind("<Button-3>")

        if "width" in kw and kw["width"] != None:
            super().configure(width=kw.pop("width"))
        if "height" in kw and kw["height"] != None:
            super().configure(height=kw.pop("height"))
        return self

    def grid_configure(self, cnf={}, **kw) -> None:
        self.render()
        super().grid_configure(cnf, **kw)

    grid = grid_configure

    def pack_configure(self, cnf={}, **kw) -> None:
        self.render()
        super().pack_configure(cnf, **kw)

    pack = pack_configure

    def place_configure(self, cnf={}, **kw) -> None:
        self.render()
        super().place_configure(cnf, **kw)

    place = place_configure

    config = configure
