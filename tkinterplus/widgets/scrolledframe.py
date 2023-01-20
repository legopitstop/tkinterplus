import tkinter
from .. import BaseWidgetPlus

class ScrolledFrame(BaseWidgetPlus):
    def __init__(self, container, bg_color:str=None, **kw):
        """Construct a scrolledframe widget with the parent MASTER."""
        self.bg_color = '#f0f0f0'

        self._container = tkinter.Frame(container)

        self._canvas = tkinter.Canvas(self._container, bd=0, highlightthickness=0, bg=self.bg_color)
        self._canvas.bind('<Enter>', self._on_enter)
        self._canvas.bind('<Leave>', self._on_leave)

        self._scrollbar = tkinter.Scrollbar(self._container, orient="vertical", command=self._canvas.yview)
        self.frame = tkinter.Frame(self._canvas, bg=self.bg_color)
        self.frame.bind("<Configure>",lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self._scrollbar.pack(side=tkinter.RIGHT, fill='y')

        self.configure(bg_color=bg_color)

        # Arguments for tk
        self.children = self.frame.children
        self.tk = self.frame.tk
        self._w = self.frame._w
        super().__init__(self)

    def _on_mouse_wheel(self, e:tkinter.Event): self._canvas.yview_scroll( int(-1*(e.delta/120)) , "units")
    def _on_enter(self, e:tkinter.Event): self._canvas.bind_all('<MouseWheel>', self._on_mouse_wheel)
    def _on_leave(self, e:tkinter.Event): self._canvas.unbind_all('<MouseWheel>')

    # NOT ADDED

    def configure(self, **kw):
        """ScrolledText"""
        if 'bg_color' in kw:
            self.bg_color = kw['bg_color']
            self.frame.configure(bg=self.bg_color)
            self._canvas.configure(bg=self.bg_color)
    config = configure

    # Default Tk
    def pack_configure(self, **kw):
        """Pack a widget in the parent widget."""
        self._container.pack_configure(**kw)
    pack = pack_configure

    def grid_configure(self, **kw):
        """osition a widget in the parent widget in a grid."""
        self._container.grid_configure(**kw)
    grid = grid_configure

    def place_configure(self, **kw):
        """Place a widget in the parent widget."""
        self._container.place_configure(**kw)
    place = place_configure

    def destroy(self):
        """Destroy this and all descendants widgets."""
        self._container.destroy()

    def bind_all(self, sequence:str, func, add:bool=None):
        """Bind to all widgets at an event SEQUENCE a call to function FUNC."""
        self.frame.bind_all(sequence, func, add)
        self._canvas.bind_all(sequence, func, add)
        
    def unbind_all(self, sequence:str):
        """Unbind for all widgets for event SEQUENCE all functions."""
        self.frame.unbind_all(sequence)
        self._canvas.unbind_all(sequence)

    def bind(self, sequence:str, func, add:bool=None):
        """Bind to this widget at event SEQUENCE a call to function FUNC."""
        self.frame.bind(sequence, func, add)
        self._canvas.bind(sequence, func, add)

    def unbind(self, sequence:str, funcid:str=None):
        """Unbind for this widget for event SEQUENCE the function identified with FUNCID."""
        self.frame.unbind(sequence, funcid)
        self._canvas.unbind(sequence, funcid)

    config = configure
