from tkinter import Tk, Canvas

from ...windows.modal import Modal

class CanvasPlus(Canvas):
    def __init__(self, master:Tk, **kw):
        """Canvas widget to display graphical elements like lines or text."""
        super().__init__(master, **kw)

    def create_window(self, __x:float, __y:float, window=None, *args, **kw):
        if isinstance(window, Modal): window = window._container
        super().create_window(__x, __y, window=window, *args, **kw)