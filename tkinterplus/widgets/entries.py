from typing import Self
from datetime import datetime
from tkcalendar import Calendar, DateEntry
import tkinter

__all__ = ["DateEntry", "TimeEntry", "DateTimeEntry", "WeekEntry", "MonthEntry"]


class DateEntry(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        textvariable: tkinter.IntVar = None,
        width: int = None,
        height: int = None,
        format: str = None,
    ):
        super().__init__(master)
        self._display = tkinter.StringVar()
        self._display.set("mm/dd/yyyy")
        self.textvariable = tkinter.DoubleVar()
        self.textvariable.trace_add("write", self.__write)
        self.width = None
        self.height = None
        self.format = "%m/%d/%Y"

        self._entry = tkinter.Entry(self, textvariable=self._display, state="readonly")
        self._entry.pack(expand=1, fill="x", side="left")
        self._button = tkinter.Button(self, text="I", command=self.tk_popup)
        self._button.pack(side="right")

        self.configure(
            textvariable=textvariable, width=width, height=height, format=format
        )

    def tk_popup(self) -> None:
        cal = Calendar(self.master, selectmode="day")
        cal.place(x=self.winfo_x(), y=self.winfo_y())

    def __write(self, a, b, c) -> None:
        timestamp = self.getdouble(self.textvariable.get())
        res = datetime.fromtimestamp(timestamp)
        dis = res.strftime(self.format)
        self._display.set(dis)

    def get(self) -> str:
        return self.textvariable.get()

    def set(self, value):
        self.textvariable.set(value)

    def configure(self, **kw) -> Self:
        if "textvariable" in kw and kw["textvariable"] != None:
            self.textvariable = kw.pop("textvariable")
            self.textvariable.trace_add("write", self.__write)
        if "width" in kw and kw["width"] != None:
            self.width = kw.pop("width")
        if "height" in kw and kw["height"] != None:
            self.height = kw.pop("height")
        if "format" in kw and kw["format"] != None:
            self.format = kw.pop("format")
        return self

    config = configure


class TimeEntry(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        textvariable: tkinter.DoubleVar = None,
        width: int = None,
        height: int = None,
        format: str = None,
    ):
        super().__init__(master)
        self._display = tkinter.StringVar()
        self._display.set("--:-- --")
        self.textvariable = tkinter.DoubleVar()
        self.textvariable.trace_add("write", self.__write)
        self.width = None
        self.height = None
        self.format = "%I:%M %p"

        self._entry = tkinter.Entry(self, textvariable=self._display, state="readonly")
        self._entry.pack(expand=1, fill="x", side="left")
        self._button = tkinter.Button(self, text="I", command=self.tk_popup)
        self._button.pack(side="right")

        self.configure(
            textvariable=textvariable, width=width, height=height, format=format
        )

    def tk_popup(self) -> None:
        pass

    def __write(self, a, b, c) -> None:
        timestamp = self.getdouble(self.textvariable.get())
        res = datetime.fromtimestamp(timestamp)
        dis = res.strftime(self.format)
        self._display.set(dis)

    def get(self) -> str:
        return self.textvariable.get()

    def set(self, value) -> None:
        self.textvariable.set(value)

    def configure(self, **kw) -> Self:
        if "textvariable" in kw and kw["textvariable"] != None:
            self.textvariable = kw.pop("textvariable")
            self.textvariable.trace_add("write", self.__write)
        if "width" in kw and kw["width"] != None:
            self.width = kw.pop("width")
        if "height" in kw and kw["height"] != None:
            self.height = kw.pop("height")
        if "format" in kw and kw["format"] != None:
            self.format = kw.pop("format")
        return self

    config = configure


class DateTimeEntry(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        textvariable: tkinter.DoubleVar = None,
        width: int = None,
        height: int = None,
        format: str = None,
    ):
        super().__init__(master)
        self._display = tkinter.StringVar()
        self._display.set("mm/dd/yyyy --:-- --")
        self.textvariable = tkinter.DoubleVar()
        self.textvariable.trace_add("write", self.__write)
        self.width = None
        self.height = None
        self.format = "%m/%d/%Y %I:%M %p"

        self._entry = tkinter.Entry(self, textvariable=self._display, state="readonly")
        self._entry.pack(expand=1, fill="x", side="left")
        self._button = tkinter.Button(self, text="I")
        self._button.pack(side="right")

        self.configure(
            textvariable=textvariable, width=width, height=height, format=format
        )

    def __write(self, a, b, c) -> None:
        timestamp = self.getdouble(self.textvariable.get())
        res = datetime.fromtimestamp(timestamp)
        dis = res.strftime(self.format)
        self._display.set(dis)

    def get(self) -> str:
        return self.textvariable.get()

    def set(self, value) -> None:
        self.textvariable.set(value)

    def configure(self, **kw) -> Self:
        if "textvariable" in kw and kw["textvariable"] != None:
            self.textvariable = kw.pop("textvariable")
            self.textvariable.trace_add("write", self.__write)
        if "width" in kw and kw["width"] != None:
            self.width = kw.pop("width")
        if "height" in kw and kw["height"] != None:
            self.height = kw.pop("height")
        if "format" in kw and kw["format"] != None:
            self.format = kw.pop("format")
        return self

    config = configure


class WeekEntry(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        textvariable: tkinter.DoubleVar = None,
        width: int = None,
        height: int = None,
        format: str = None,
    ):
        super().__init__(master)
        self._display = tkinter.StringVar()
        self._display.set("Week --, ----")
        self.textvariable = tkinter.DoubleVar()
        self.textvariable.trace_add("write", self.__write)
        self.width = None
        self.height = None
        self.format = "Week %U, %Y"

        self._entry = tkinter.Entry(self, textvariable=self._display, state="readonly")
        self._entry.pack(expand=1, fill="x", side="left")
        self._button = tkinter.Button(self, text="I")
        self._button.pack(side="right")

        self.configure(
            textvariable=textvariable, width=width, height=height, format=format
        )

    def __write(self, a, b, c) -> None:
        timestamp = self.getdouble(self.textvariable.get())
        res = datetime.fromtimestamp(timestamp)
        dis = res.strftime(self.format)
        self._display.set(dis)

    def get(self) -> str:
        return self.textvariable.get()

    def set(self, value) -> None:
        self.textvariable.set(value)

    def configure(self, **kw) -> Self:
        if "textvariable" in kw and kw["textvariable"] != None:
            self.textvariable = kw.pop("textvariable")
            self.textvariable.trace_add("write", self.__write)
        if "width" in kw and kw["width"] != None:
            self.width = kw.pop("width")
        if "height" in kw and kw["height"] != None:
            self.height = kw.pop("height")
        if "format" in kw and kw["format"] != None:
            self.format = kw.pop("format")
        return self

    config = configure


class MonthEntry(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        textvariable: tkinter.DoubleVar = None,
        width: int = None,
        height: int = None,
        format: str = None,
    ):
        super().__init__(master)
        self._display = tkinter.StringVar()
        self._display.set("-------- ----")
        self.textvariable = tkinter.DoubleVar()
        self.textvariable.trace_add("write", self.__write)
        self.width = None
        self.height = None
        self.format = "%B %Y"

        self._entry = tkinter.Entry(self, textvariable=self._display, state="readonly")
        self._entry.pack(expand=1, fill="x", side="left")
        self._button = tkinter.Button(self, text="I")
        self._button.pack(side="right")

        self.configure(
            textvariable=textvariable, width=width, height=height, format=format
        )

    def __write(self, a, b, c) -> None:
        timestamp = self.getdouble(self.textvariable.get())
        res = datetime.fromtimestamp(timestamp)
        dis = res.strftime(self.format)
        self._display.set(dis)

    def get(self) -> str:
        return self.textvariable.get()

    def set(self, value) -> None:
        self.textvariable.set(value)

    def configure(self, **kw) -> Self:
        if "textvariable" in kw and kw["textvariable"] != None:
            self.textvariable = kw.pop("textvariable")
            self.textvariable.trace_add("write", self.__write)
        if "width" in kw and kw["width"] != None:
            self.width = kw.pop("width")
        if "height" in kw and kw["height"] != None:
            self.height = kw.pop("height")
        if "format" in kw and kw["format"] != None:
            self.format = kw.pop("format")
        return self

    config = configure
