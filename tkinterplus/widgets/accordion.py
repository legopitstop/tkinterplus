from tkinter import E, EW, LEFT, W, NORMAL, Tk, Misc, Frame, Label, StringVar, _get_temp_root

from .. import Icon, EXPAND_MORE, EXPAND_LESS

class Accordion(Misc):
    def __init__(self, master:Tk, text:str=None, textvariable:StringVar=None, bg_color:str=None, bg_header_color:str=None, disabled_fg_header_color:str=None, active_bg_header_color:str=None, active_fg_header_color:str=None, fg_header_color:str=None, show_icon:str=None, hide_icon:str=None, name:str=None, variable:StringVar=None, state:str=None):
       
        if master is None: master = _get_temp_root()

        # Other Args
        self.visable = False
        self.textvariable = StringVar()
        self.text = None
        self.bg_color = '#f0f0f0'
        self.bg_header_color = 'white'
        self.fg_header_color = 'black'
        self.disabled_fg_header_color = 'red'
        self.active_bg_header_color = 'white'
        self.active_fg_header_color = 'black'
        self.show_icon = EXPAND_LESS
        self.hide_icon = EXPAND_MORE
        self.width = 100
        self.height = 100
        self.variable = StringVar()
        self.state = NORMAL # NORMAL, DISABLED, ACTIVE
        # TODO remove self.visable and use self.state instead

        # Widgets
        self.SHOW_ICON = Icon(self.show_icon, color=self.fg_header_color)
        self.HIDE_ICON = Icon(self.hide_icon, color=self.fg_header_color)

        self._container = Frame(master)
        self._header = Frame(self._container)
        self._label = Label(self._header, textvariable=self.textvariable, bg=self.bg_header_color, fg=fg_header_color, anchor=W)
        self._label.grid(row=0,column=0, sticky=EW, ipadx=2, ipady=2)

        self._icon = Label(self._header, image=self.SHOW_ICON, width=23, height=23, bg=self.bg_header_color)
        self._icon.grid(row=0,column=1, sticky=E)

        self._header.grid(row=0,column=0, sticky=EW)
        self.content = Frame(self._container, bg=self.bg_color, width=self.width, height=self.height)

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
            bg_color=bg_color,
            bg_header_color=bg_header_color,
            fg_header_color=fg_header_color,
            textvariable=textvariable,
            show_icon=show_icon,
            hide_icon=hide_icon,
            state=state,
            disabled_fg_header_color=disabled_fg_header_color,
            active_bg_header_color=active_bg_header_color,
            active_fg_header_color=active_fg_header_color
        )


    def configure(self, **kw):
        if 'text' in kw and kw['text']!=None:
            self.text = kw['text']
            self.textvariable.set(self.text)
        if 'textvariable' in kw and kw['textvariable']!=None: self.textvariable = kw['textvariable']
        if 'disabled_fg_header_color' in kw and kw['disabled_fg_header_color']!=None: self.disabled_fg_header_color = kw['disabled_fg_header_color']
        if 'active_bg_header_color' in kw and kw['active_bg_header_color']!=None: self.active_bg_header_color = kw['active_bg_header_color']
        if 'active_fg_header_color' in kw and kw['active_fg_header_color']!=None: self.active_fg_header_color = kw['active_fg_header_color']
        if 'name' in kw and kw['name']!=None: self.name = kw['name']
        if 'variable' in kw and kw['variable']!=None: self.variable = kw['variable']
        if 'state' in kw and kw['state']!=None: self.state = kw['state']

        if 'width' in kw and kw['width']!=None:
            self.width = kw['width']
            self.content.configure(width=self.width)

        if 'height' in kw and kw['height']!=None:
            self.height = kw['height']
            self.content.configure(height=self.height)

        if 'bg_color' in kw and kw['bg_color']!=None:
            self.bg_color = kw['bg_color']
            self.content.configure(bg=self.bg_color)

        if 'bg_header_color' in kw and kw['bg_header_color']!=None:
            self.bg_header_color = kw['bg_header_color']
            self._label.configure(bg=self.bg_header_color)
            self._icon.configure(bg=self.bg_header_color)

        if 'fg_header_color' in kw and kw['fg_header_color']!=None:
            self.fg_header_color = kw['fg_header_color']
            self._label.configure(fg=self.fg_header_color)
            self.SHOW_ICON.configure(color=self.fg_header_color)
            self.HIDE_ICON.configure(color=self.fg_header_color)
            

        if 'show_icon' in kw and kw['show_icon']!=None:
            self.show_icon = kw['show_icon']
            self.SHOW_ICON.configure(name=self.show_icon, color=self.fg_header_color)

        if 'hide_icon' in kw and kw['hide_icon']!=None:
            self.hide_icon = kw['hide_icon']
            self.HIDE_ICON.configure(name=self.hide_icon, color=self.fg_header_color)
        
        self.update()

    config = configure

    def update(self):
        """updates the icons"""
        # Update the icons with the new color
        if self.visable: self._icon.configure(bg=self.bg_header_color, image=self.SHOW_ICON)
        else: self._icon.configure(bg=self.bg_header_color, image=self.HIDE_ICON)
        
        # Update widget state
        self._label.unbind('<Button-1>')
        self._icon.unbind('<Button-1>')
        self._label.configure(fg=self.disabled_fg_header_color)
        if self.state==NORMAL:
            self._label.bind('<Button-1>', lambda e: self._toggle())
            self._icon.bind('<Button-1>', lambda e: self._toggle())
            self._label.configure(fg=self.fg_header_color)

            self.variable.trace_add('write', self._variable_update)

    def _variable_update(self, a, b, c):
        v = self.variable.get()
        if v!=self.name and v!='': self.hide()

    def _toggle(self):
        if self.visable: self.hide()
        else: self.show()

    def show(self):
        """Expand the accordion"""
        if self.visable==False:
            self.visable=True
            self.content.grid(row=1,column=0, sticky='nesw')

            # Update color
            self.SHOW_ICON.configure(color=self.active_fg_header_color)
            self.HIDE_ICON.configure(color=self.active_fg_header_color)
            self._label.configure(bg=self.active_bg_header_color, fg=self.active_fg_header_color)
            self._icon.configure(bg=self.active_bg_header_color, fg=self.active_fg_header_color, image=self.SHOW_ICON)
            self.variable.set(self.name)

    def hide(self):
        """Shrink the accordion"""
        if self.visable==True:
            self.visable=False
            self.content.grid_forget()
            
            # Update color
            self.SHOW_ICON.configure(color=self.fg_header_color)
            self.HIDE_ICON.configure(color=self.fg_header_color)
            self._label.configure(bg=self.bg_header_color, fg=self.fg_header_color)
            self._icon.configure(bg=self.bg_header_color, fg=self.fg_header_color, image=self.HIDE_ICON)

            if self.variable.get() == self.name: self.variable.set('')

    def grid_configure(self, **kw): self._container.grid_configure(**kw)
    grid = grid_configure
    
    def place_configure(self, **kw): self._container.place_configure(**kw)
    place = place_configure
    
    def pack_configure(self, **kw): self._container.pack_configure(**kw)
    pack = pack_configure