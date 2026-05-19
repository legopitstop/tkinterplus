from typing import Callable, Self
import tkinter
from tkinter.scrolledtext import ScrolledText
import re
import enum
from .buttons import BindButton, FileButton, DirectoryButton, ColorButton
from .entries import DateEntry, TimeEntry, DateTimeEntry, WeekEntry, MonthEntry

__all__ = ["EntryTypes", "Input"]

# PLANNED
# email - Entry,pattern=r'EMAIL'
# tel - Entry,pattern='^[0-9]{3}-[0-9]{2}-[0-9]{3}$'
# url - Entry,pattern=''
# enum - OptionMenu,items=[item1, item2]
# date
# datetime-local
# month
# time
# week
# radio
# range


class EntryTypes(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk = None,
        type: str = "text",
        label: tkinter.Label = None,
        textvariable: tkinter.StringVar = None,
        command: Callable = None,
        pattern: str = None,
        from_: int = None,
        to: int = None,
        increment: int = None,
        defaultextension: str = None,
        filetypes: list = None,
        mustexist: str = None,
        width: int = None,
        height: int = None,
        items: list = None,
        state: str = None,
        **kw,
    ):
        """Construct an input widget with the parent MASTER."""
        super().__init__(master)
        self.type = type
        self.textvariable = tkinter.StringVar()

        self.pattern = None
        self.from_ = None
        self.to = None
        self.increment = None
        self.defaultextension = None
        self.filetypes = []
        self.mustexist = None
        self.label = None
        self.width = None
        self.height = None
        self.command = None
        self.state = tkinter.NORMAL  # TODO add
        self.items = []

        self._widget = None
        self._valid = master.register(self.__validate)

        # Auto type
        if self.type == "text":
            if items != None:
                type = "enum"

        match self.type:
            case "integer":
                self.textvariable = tkinter.IntVar()
                self.from_ = -100
                self.to = 100
                self.increment = 1
            case "float":
                self.textvariable = tkinter.DoubleVar()
                self.from_ = -100.0
                self.to = 100.0
                self.increment = 0.1
            case "checkbox":
                self.textvariable = tkinter.BooleanVar()

        # Add traces to variables for tkinter.Text
        self.textvariable.trace_add("write", lambda a, b, c: self.__write())
        self.textvariable.trace_add("read", lambda a, b, c: self.__read())

        self.configure(
            textvariable=textvariable,
            pattern=pattern,
            from_=from_,
            to=to,
            increment=increment,
            defaultextension=defaultextension,
            filetypes=filetypes,
            mustexist=mustexist,
            label=label,
            width=width,
            height=height,
            command=command,
            state=state,
            items=items,
            **kw,
        )
        self.draw()

    def __read(self) -> None:
        if self.type == "text":
            value = self._widget.get(0.0, tkinter.END)
            self.textvariable.set(value)

    def __write(self) -> None:
        value = self.textvariable.get()
        if self.type == "color":
            match value:  # Tkinter color names to HEX
                case "SystemButtonFace":
                    self.textvariable.set("#f8f8f8")
                case "SystemButtonText":
                    self.textvariable.set("black")
                case "SystemWindowFrame":
                    self.textvariable.set("#f8f8f8")
                case "SystemDisabledText":
                    self.textvariable.set("gray")

        elif self.type == "text":
            self._widget.delete(0.0, tkinter.END)
            self._widget.insert(0.0, value)

        if self.command != None:
            self.command()  # Call cmd when variable gets updated

    def get(self) -> str:
        if isinstance(self.items, enum.EnumMeta):
            name = self.textvariable.get()
            return self.items[name]
        return self.textvariable.get()

    def set(self, value) -> None:
        if isinstance(value, enum.Enum):
            self.textvariable.set(value._name_)
        else:
            self.textvariable.set(value)

    def focus_set(self) -> None:
        self._widget.focus_set()

    focus = focus_set

    # TODO use kw.pop() for getting all args.
    def configure(self, **kw) -> Self:
        if "textvariable" in kw and kw["textvariable"] != None:
            self.textvariable: tkinter.StringVar = kw.pop("textvariable")
            self.textvariable.trace_add("write", lambda a, b, c: self.__write())
            self.textvariable.trace_add("read", lambda a, b, c: self.__read())

        if "pattern" in kw and kw["pattern"] != None:
            self.pattern = kw.pop("pattern")
        if "from_" in kw and kw["from_"] != None:
            self.from_ = kw.pop("from_")
        if "to" in kw and kw["to"] != None:
            self.to = kw.pop("to")
        if "increment" in kw and kw["increment"] != None:
            self.increment = kw.pop("increment")
        if "defaultextension" in kw and kw["defaultextension"] != None:
            self.defaultextension = kw.pop("defaultextension")
        if "filetypes" in kw and kw["filetypes"] != None:
            self.filetypes = kw.pop("filetypes")
        if "mustexist" in kw and kw["mustexist"] != None:
            self.mustexist = kw.pop("mustexist")
        if "width" in kw and kw["width"] != None:
            self.width = kw.pop("width")
        if "height" in kw and kw["height"] != None:
            self.height = kw.pop("height")
        if "state" in kw and kw["state"] != None:
            self.state = kw.pop("state")
        if "command" in kw and kw["command"] != None:
            self.command = kw.pop("command")
        if "items" in kw and kw["items"] != None:
            self.items = kw.pop("items")
        if "label" in kw and kw["label"] != None:
            self.label: tkinter.Label = kw.pop("label")
            if isinstance(self.label, tkinter.Widget):
                self.label.bind("<Button-1>", lambda e: self.focus_set())
        return self

    config = configure

    def draw(self) -> None:
        match self.type.lower():
            case "short":
                self._widget = tkinter.Entry(
                    self,
                    textvariable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.configure(
                    validate="key", validatecommand=(self._valid, "%P")
                )
                self._widget.pack(expand=1, fill="x")

            case "checkbox":
                self._widget = tkinter.Checkbutton(
                    self,
                    variable=self.textvariable,
                    onvalue=True,
                    offvalue=False,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x")

            case "text":  # TODO add self.textvariable binding along with validation
                self._widget = ScrolledText(self, width=self.width, height=self.height)
                # self._widget.configure(validate='key', validatecommand=(self._valid, '%P'))
                self._widget.pack(expand=1, fill="x")

            case "password":
                self._widget = tkinter.Entry(
                    self,
                    textvariable=self.textvariable,
                    show="*",
                    width=self.width,
                    height=self.height,
                )
                self._widget.configure(
                    validate="key", validatecommand=(self._valid, "%P")
                )
                self._widget.pack(expand=1, fill="x")

            case "integer":  # TODO - add scrollwheel increase and decrease
                if self.pattern == None:
                    self.pattern = r"^-?[0-9]\d$"
                self._widget = tkinter.Spinbox(
                    self,
                    textvariable=self.textvariable,
                    from_=self.from_,
                    to=self.to,
                    increment=self.increment,
                    width=self.width,
                    height=self.height,
                )
                self._widget.configure(
                    validate="key", validatecommand=(self._valid, "%P")
                )
                self._widget.pack(expand=1, fill="x")

            case "float":  # TODO - add scrollwheel increase and decrease
                if self.pattern == None:
                    self.pattern = r"^-?[0-9]\d*\.\d+$"
                self._widget = tkinter.Spinbox(
                    self,
                    textvariable=self.textvariable,
                    from_=self.from_,
                    to=self.to,
                    increment=self.increment,
                    width=self.width,
                    height=self.height,
                )
                self._widget.configure(
                    validate="key", validatecommand=(self._valid, "%P")
                )
                self._widget.pack(expand=1, fill="x")

            case "color":
                self._widget = ColorButton(
                    self,
                    variable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x", side=tkinter.LEFT)

            case "file":
                self._widget = FileButton(
                    self,
                    variable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x", side=tkinter.LEFT)

            case "directory":
                self._widget = DirectoryButton(
                    self,
                    variable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x", side=tkinter.LEFT)

            case "keybind":
                self._widget = BindButton(
                    self,
                    variable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x")

            case "email":
                if self.pattern == None:
                    self.pattern = r""  # TODO Add pattern
                self._widget = tkinter.Entry(
                    self,
                    textvariable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.configure(
                    validate="key", validatecommand=(self._valid, "%P")
                )
                self._widget.pack(expand=1, fill="x")

            case "tel":
                if self.pattern == None:
                    self.pattern = r"^[0-9]{3}-[0-9]{2}-[0-9]{3}$"
                self._widget = tkinter.Entry(
                    self,
                    textvariable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.configure(
                    validate="key", validatecommand=(self._valid, "%P")
                )
                self._widget.pack(expand=1, fill="x")

            case "url":
                if self.pattern == None:
                    self.pattern = r""  # TODO Add pattern
                self._widget = tkinter.Entry(
                    self,
                    textvariable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.configure(
                    validate="key", validatecommand=(self._valid, "%P")
                )
                self._widget.pack(expand=1, fill="x")

            case "enum":
                if isinstance(self.items, enum.EnumMeta):
                    items = []
                    for i in self.items:
                        items.append(i._name_)

                elif isinstance(self.items, list):
                    items = self.items
                else:
                    items = ["unset"]

                self._widget = tkinter.OptionMenu(self, self.textvariable, *items)
                self._widget.configure(command=self.command)
                self._widget.pack(expand=1, fill="x")

            case "date":
                self._widget = DateEntry(
                    self,
                    # textvariable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x")

            case "datetime":
                self._widget = DateTimeEntry(
                    self,
                    textvariable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x")

            case "month":
                self._widget = MonthEntry(
                    self,
                    textvariable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x")

            case "time":
                self._widget = TimeEntry(
                    self,
                    textvariable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x")

            case "week":
                self._widget = WeekEntry(
                    self,
                    textvariable=self.textvariable,
                    width=self.width,
                    height=self.height,
                )
                self._widget.pack(expand=1, fill="x")

            case "radio":
                print("radio - Not added yet!")
            case "range":
                print("range - Not added yet!")

            case _:
                raise KeyError(f"Unknown entry type {self.type}")

    def __validate(self, input: str) -> bool:
        if self.pattern != None:
            if re.match(self.pattern, input) or input == "":
                return True
            else:
                self.bell()
                return False

        return True  # no validation restrictions


Input = EntryTypes
