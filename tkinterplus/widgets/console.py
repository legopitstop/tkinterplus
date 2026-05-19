from typing import Self
import tkinter
import sys

__all__ = ["ConsoleLogger", "Console", "ScrolledConsole"]


class ConsoleLogger(object):
    def __init__(self, *tags):
        self.__widgets = []
        self.tags = tags

    def write(self, text) -> None:
        sys.__stdout__.write(text)  # default console
        for w in self.__widgets:
            w.configure(state="normal")
            w.insert("end", text, *self.tags)
            w.see("end")
            w.configure(state="disabled")

    def bind(self, widget: tkinter.Text) -> None:
        """Bind widget to logger"""
        if isinstance(widget, tkinter.Text):
            self.__widgets.insert(0, widget)
        else:
            raise TypeError(
                f"Expected tkinter.Text but got {widget.__class__.__name__} instead."
            )

    def unbind(self, widget: tkinter.Text) -> None:
        """Unbind widget from logger"""
        if isinstance(widget, tkinter.Text):
            self.__widgets.remove(widget)
        else:
            raise TypeError(
                f"Expected tkinter.Text but got {widget.__class__.__name__} instead."
            )

    def flush(self) -> None:
        pass


__stdout__ = ConsoleLogger("stdout")
sys.stdout = __stdout__

__stderr__ = ConsoleLogger("stderr")
sys.stderr = __stderr__


class Console(tkinter.Frame):
    def __init__(self, master, stdout: bool = None, stderr: bool = None, **kw):
        super().__init__(master)
        self.text = tkinter.Text(self, state="disabled")
        self.text.tag_configure("stderr", foreground="red")
        self.text.pack(expand=1, fill="both")
        self.stdout = True
        self.stderr = True
        __stdout__.bind(self.text)
        __stderr__.bind(self.text)

        self.configure(stdout=stdout, stderr=stderr, **kw)

    def destroy(self) -> None:
        # Remove widget
        if self.stdout:
            __stdout__.unbind(self.text)
        if self.stderr:
            __stderr__.unbind(self.text)
        super().destroy()

    def configure(self, **kw) -> Self:
        if "stdout" in kw and kw["stdout"] != None:
            self.stdout = kw.pop("stdout")
            if self.stdout:
                __stdout__.bind(self.text)
            else:
                __stdout__.unbind(self.text)

        if "stderr" in kw and kw["stderr"] != None:
            self.stderr = kw.pop("stderr")
            if self.stderr:
                __stderr__.bind(self.text)
            else:
                __stderr__.unbind(self.text)
        self.text.configure(**kw)
        return self

    config = configure

    def yview(self, *args) -> tuple[float, float]:
        return self.text.yview(*args)

    def xview(self, *args) -> tuple[float, float]:
        return self.text.xview(*args)

    def clear(self) -> None:
        self.text.configure(state="normal")
        self.text.delete(0.0, "end")
        self.text.configure(state="disabled")


class ScrolledConsole(Console):
    def __init__(self, master=None, **kw):
        self.frame = tkinter.Frame(master)
        self.vbar = tkinter.Scrollbar(self.frame)
        self.vbar.pack(side="right", fill="y")

        kw.update({"yscrollcommand": self.vbar.set})
        Console.__init__(self, self.frame, **kw)
        self.pack(side="left", fill="both", expand=True)
        self.vbar["command"] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(Console).keys()
        methods = (
            vars(tkinter.Pack).keys()
            | vars(tkinter.Grid).keys()
            | vars(tkinter.Place).keys()
        )
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != "_" and m != "config" and m != "configure":
                setattr(self, m, getattr(self.frame, m))

    def __str__(self) -> str:
        return str(self.frame)
