# A widget that contains addional methods. Should be supported for all tkinterplus widgets.
import tkinter
from .. import Animation

__all__ = ["BaseWidgetPlus"]


class BaseWidgetPlus(tkinter.Misc):
    def __init__(self, master):
        # Animation.__init__(self, self)
        # self.master = master
        super().__init__()
        self.master = master
