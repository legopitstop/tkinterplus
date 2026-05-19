import tkinter
import tktooltip

__all__ = ["Tooltip"]


class Tooltip(tktooltip.ToolTip):
    def __init__(
        self,
        master: tkinter.Tk,
        msg: str = None,
        textvariable: tkinter.StringVar = None,
        **kw
    ):
        super().__init__(master, "", **kw)
        self._var = tkinter.StringVar(value=msg)
        self._var.trace_add("write", self._callback)
        self.configure(textvariable=textvariable)

    def _callback(self, a, b, c) -> None:
        self.msg = self.textvariable.get()

    def configure(self, **kw) -> None:
        if "textvariable" in kw:
            if kw["textvariable"] is None:
                kw.pop("textvariable")
            else:
                self.textvariable = kw.pop("textvariable")
                self.textvariable.trace_add("write", self._callback)
        super().configure(**kw)

    config = configure
