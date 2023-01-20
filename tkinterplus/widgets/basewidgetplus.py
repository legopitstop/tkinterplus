# A widget that contains addional methods. Should be supported for all tkinterplus widgets.
import tkinter
from .. import Animation

class BaseWidgetPlus(Animation, tkinter.Misc):
    def __init__(self, master):
        Animation.__init__(self, self)
        tkinter.Misc.__init__(self)