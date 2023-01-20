import tkinter
from .. import MaterialIcon

class Accordion(tkinter.Misc):
    def __init__(self, master:tkinter.Tk, text:str=None, image:str=None, textvariable:tkinter.StringVar=None, bg:str=None, background_header:str=None, disabled_foreground_header:str=None, active_background_header:str=None, active_foreground_header:str=None, foreground_header:str=None, show_icon:str=None, hide_icon:str=None, name:str=None, variable:tkinter.StringVar=None, state:str=None, font=None):
        """Construct an accordion widget with the parent MASTER."""
        if master is None: master = tkinter._get_temp_root()

        # Other Args
        self.visable = False
        self.textvariable = tkinter.StringVar()
        self.textvariable.set('Accordion')
        self.text = None
        self.bg = '#f0f0f0'
        self.background_header = 'white'
        self.foreground_header = 'black'
        self.disabled_foreground_header = 'red'
        self.active_background_header = 'white'
        self.active_foreground_header = 'black'
        self.show_icon = 'expand_more'
        self.hide_icon = 'expand_less'
        self.width = 100
        self.height = 100
        self.variable = tkinter.StringVar()
        self.image = None
        self.state = tkinter.NORMAL # NORMAL, DISABLED, ACTIVE
        # TODO remove self.visable and use self.state instead

        # Widgets
        self.SHOW_ICON = MaterialIcon(self.show_icon, color=self.foreground_header, size=(30, 30))
        self.HIDE_ICON = MaterialIcon(self.hide_icon, color=self.foreground_header, size=(30, 30))

        self._container = tkinter.Frame(master)
        self._header = tkinter.Frame(self._container, bg=self.background_header, cursor='hand2')
        self._label = tkinter.Label(self._header, textvariable=self.textvariable, compound=tkinter.LEFT, image=self.image, bg=self.background_header, fg=foreground_header, anchor=tkinter.W)
        self._label.grid(row=0,column=0, sticky=tkinter.EW, ipadx=5, ipady=2)

        self._icon = tkinter.Label(self._header, image=self.SHOW_ICON, width=23, height=23, bg=self.background_header)
        self._icon.grid(row=0,column=1, sticky=tkinter.E)

        self._header.grid(row=0,column=0, ipadx=10, ipady=2, sticky=tkinter.EW)
        self.content = tkinter.Frame(self._container, bg=self.bg, width=self.width, height=self.height)

        # Arguments for tk
        self.master = master
        self.children = self.content.children
        self.tk = self.content.tk
        self._w = self.content._w
        self.name = self.winfo_name()

        # Responsive
        self._header.grid_columnconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)
        self._container.grid_rowconfigure(1, weight=1)

        self.configure(
            name=name,
            variable=variable,
            text=text,
            image=image,
            bg=bg,
            background_header=background_header,
            foreground_header=foreground_header,
            textvariable=textvariable,
            show_icon=show_icon,
            hide_icon=hide_icon,
            state=state,
            disabled_foreground_header=disabled_foreground_header,
            active_foreground_header=active_foreground_header,
            active_background_header=active_background_header
        )

    def configure(self, **kw):
        if 'text' in kw and kw['text']!=None:
            self.text = kw['text']
            self.textvariable.set(self.text)

        if 'image' in kw and kw['image']!=None:
            self.image = kw['image']
            self._label.configure(image=self.image)
        
        if 'textvariable' in kw and kw['textvariable']!=None: self.textvariable = kw['textvariable']
        if 'disabled_foreground_header' in kw and kw['disabled_foreground_header']!=None: self.disabled_foreground_header = kw['disabled_foreground_header']
        if 'active_background_header' in kw and kw['active_background_header']!=None: self.active_background_header = kw['active_background_header']
        if 'active_foreground_header' in kw and kw['active_foreground_header']!=None: self.active_foreground_header = kw['active_foreground_header']
        if 'name' in kw and kw['name']!=None: self.name = kw['name']
        if 'variable' in kw and kw['variable']!=None: self.variable = kw['variable']

        if 'width' in kw and kw['width']!=None:
            self.width = kw['width']
            self.content.configure(width=self.width)

        if 'height' in kw and kw['height']!=None:
            self.height = kw['height']
            self.content.configure(height=self.height)

        if 'bg' in kw and kw['bg']!=None:
            self.bg = kw['bg']
            self.content.configure(bg=self.bg)

        if 'background_header' in kw and kw['background_header']!=None:
            self.background_header = kw['background_header']
            self._label.configure(bg=self.background_header)
            self._icon.configure(bg=self.background_header)
            self._header.configure(bg=self.background_header)

        if 'foreground_header' in kw and kw['foreground_header']!=None:
            self.foreground_header = kw['foreground_header']
            self._label.configure(fg=self.foreground_header)
            self.SHOW_ICON.configure(color=self.foreground_header)
            self.HIDE_ICON.configure(color=self.foreground_header)

        if 'show_icon' in kw and kw['show_icon']!=None:
            self.show_icon = kw['show_icon']
            self.SHOW_ICON.configure(name=self.show_icon, color=self.foreground_header)

        if 'hide_icon' in kw and kw['hide_icon']!=None:
            self.hide_icon = kw['hide_icon']
            self.HIDE_ICON.configure(name=self.hide_icon, color=self.foreground_header)

        if 'state' in kw and kw['state']!=None:
            self.state = kw['state']
            if self.state == tkinter.DISABLED:
                self.SHOW_ICON.configure(color=self.disabled_foreground_header)
                self.HIDE_ICON.configure(color=self.disabled_foreground_header)
                self._label.configure(fg=self.disabled_foreground_header)
                self._icon.configure(fg=self.disabled_foreground_header)
                self._header.configure(cursor=None)

            elif self.state == tkinter.ACTIVE:
                self.SHOW_ICON.configure(color=self.active_foreground_header)
                self.HIDE_ICON.configure(color=self.active_foreground_header)
                self._icon.configure(bg=self.active_background_header, image=self.HIDE_ICON)
                self._label.configure(bg=self.active_background_header, fg=self.active_foreground_header)
                self._header.configure(bg=self.active_background_header)
            else:
                self.SHOW_ICON.configure(color=self.foreground_header)
                self.HIDE_ICON.configure(color=self.foreground_header)
                self._label.configure(bg=self.background_header, fg=self.foreground_header)
                self._icon.configure(bg=self.background_header, fg=self.foreground_header, image=self.SHOW_ICON)
                self._header.configure(bg=self.background_header)
        
        self.update()
    config = configure

    def update(self):
        """updates the icons"""
        # Update widget state
        self._label.unbind('<Button-1>')
        self._icon.unbind('<Button-1>')
        if self.state!=tkinter.DISABLED:
            self._label.bind('<Button-1>', lambda e: self._toggle())
            self._icon.bind('<Button-1>', lambda e: self._toggle())
            self.variable.trace_add('write', self._variable_update)

    def _variable_update(self, a, b, c):
        v = self.variable.get()
        if v!=self.name and v!='': self.hide()

    def _toggle(self):
        if self.state==tkinter.ACTIVE: self.hide()
        else: self.show()

    def show(self):
        """Expand the accordion"""
        if self.state==tkinter.NORMAL:
            self.configure(state=tkinter.ACTIVE)
            self.content.grid(row=1,column=0, sticky='nesw')
            self.variable.set(self.name)

    def hide(self):
        """Shrink the accordion"""
        if self.state == tkinter.ACTIVE:
            self.configure(state=tkinter.NORMAL)
            self.content.grid_forget()
            if self.variable.get() == self.name: self.variable.set('')

    def grid_configure(self, **kw): self._container.grid_configure(**kw)
    grid = grid_configure
    
    def place_configure(self, **kw): self._container.place_configure(**kw)
    place = place_configure
    
    def pack_configure(self, **kw): self._container.pack_configure(**kw)
    pack = pack_configure