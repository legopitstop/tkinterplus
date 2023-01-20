from tkinter import ACTIVE, BOTH, DISABLED, NORMAL, Tk, Event, Frame, Message, StringVar, Misc, _get_temp_root
import _tkinter

#NOTE This widget is still being worked on. Expect issues for missing features!
class Tooltip(Misc):
    def __init__(self, parent:Tk, text:str=None, textvariable:StringVar=None, bg:str=None, fg:str=None, ipadx:int=None, ipady:int=None, state:str=None, anchor:str=None, x:int=None, y:int=None, borderwidth:int=None, width:int=None, height=None, bordercolor:str=None, delay:int=None, follow:bool=None):
        """Construct a tooltip widget with the parent MASTER."""
        self.__root = _get_temp_root()
        self.parent = parent
        self.master = parent.master
        self.visable = False
        self.has_message = False
        # Arguments
        self.state = NORMAL
        self.text = None
        self.textvariable = StringVar()
        self.bg_color = 'white'
        self.fg_color = 'black'
        self.delay = 0
        self.ipadx=5
        self.ipady=5
        self.anchor = 'nw'
        self.x = 10
        self.y = 10
        self.bordercolor='black'
        self.borderwidth = 1
        self.delay = 0
        self.follow = True
        self.waiting = None
        self.width = 128
        self.height = 128
        
        self._container = Frame(self.master, bg=self.bg_color, padx=self.ipadx, pady=self.ipady, highlightthickness=self.borderwidth, highlightbackground=self.bordercolor, width=self.width, height=self.height)

        # Arguments for tk
        self.children = self._container.children
        self.tk = self._container.tk
        self._w = self._container._w
        self.configure(
            text=text,
            textvariable=textvariable,
            bg=bg,
            fg=fg,
            ipadx=ipadx,
            ipady=ipady,
            state=state,
            anchor=anchor,
            x=x,
            y=y,
            bordercolor=bordercolor,
            borderwidth=borderwidth,
            delay = delay,
            follow=follow
        )

    def _on_motion(self, e:Event): self.moveto(e.x, e.y)
    def _on_enter(self, e:Event): self.show(e.x, e.y)
    def _on_leave(self, e:Event): self.hide()

    def update(self):
        self._remove_binds()
        if self.state!=DISABLED:
            self.parent.bind('<Enter>', self._on_enter, add=True)
            self.parent.bind('<Leave>', self._on_leave, add=True)
            if self.follow==False:
                self._container.bind('<Enter>', self._on_enter, add=True)
                # self._container.bind('<Leave>', self._on_leave, add=True)

    def _remove_message(self):
        for child in self._container.winfo_children(): child.destroy()
        self.has_message = False

    def _remove_binds(self):
        self.parent.unbind('<Enter>')
        self.parent.unbind('<Leave>')
        self.unbind('<Enter>')
        self.unbind('<Leave>')

    def _create_message(self):
        self._remove_message()
        self._message = Message(self._container, textvariable=self.textvariable, width=self.width, bg=self.bg_color, fg=self.fg_color)
        self._message.pack(expand=True, fill=BOTH)
        self.has_message = True

    def _best_fit(self):
        """Get the best fit"""
        width = self.__root.winfo_width()
        height = self.__root.winfo_height()
        
        anchor = [None, None]
        i = 0
        for c in self.anchor:
            anchor[i] = c
            i+=1

        if height <= self.winfo_height() + self.winfo_y(): anchor[0] = 'n' # s
        if self.winfo_y() <= 0: anchor[0] = 's' # n

        if width <= self.winfo_width() + self.winfo_x(): anchor[1] = 'w' # e
        if self.winfo_x() <= 0: anchor[1] = 'e' # w

        result = ''
        for c in anchor: result+=c
        return result

    def moveto(self, x:int, y:int):
        if self.state!=DISABLED:
            self._container.tkraise()
            x0 = 0
            y0 = 0
            anchor = self._best_fit()
            if anchor=='center':
                x0 = (self.parent.winfo_x() +x + self.winfo_height()) / 2
                y0 = (self.parent.winfo_y() +y + self.winfo_width()) / 2
            else:
                for a in anchor:
                    if a == 'n': y0 = self.parent.winfo_y() + y + self.y
                    elif a == 's': y0 = self.parent.winfo_y() + y - self.y - self.winfo_height()
                    elif a == 'w': x0 = self.parent.winfo_x() + x + self.x
                    elif a == 'e': x0 = self.parent.winfo_x() + x - self.x - self.winfo_width()
            self._container.place_configure(x=x0, y=y0)
        
    def show(self, x:int, y:int):
        """Show the tooltip"""
        def confirm():
            self.waiting = None
            self.state = ACTIVE
            if self.follow:
                self.moveto(x, y)
                self.parent.bind('<Motion>', self._on_motion, add=True)
            else:
                self.moveto(self.x, self.y)

        if self.state==NORMAL and self.waiting==None: self.waiting = self.after(self.delay, confirm)

    def hide(self):
        """Hide the tooltip"""
        if self.state!=DISABLED:
            self.state = NORMAL
            self._container.lower()
            self._container.place_forget()
            self.parent.unbind('<Motion>')

            if self.waiting!=None: self.after_cancel(self.waiting)

    def configure(self, **kw):
        if 'state' in kw and kw['state']!=None: self.state = kw['state']
        if 'text' in kw and kw['text']!=None:
            self.textvariable.set(kw['text'])
            self._create_message()

        if 'textvariable' in kw and kw['textvariable']!=None:
            self.textvariable = kw['textvariable']
            self._create_message()
 
        if 'delay' in kw and kw['delay']!=None: self.delay = kw['delay']
        if 'x' in kw and kw['x']!=None: self.x = kw['x']
        if 'y' in kw and kw['y']!=None: self.y = kw['y']
        if 'follow' in kw and kw['follow']!=None: self.follow = kw['follow']

        if 'width' in kw and kw['width']!=None:
            self.width = kw['width']
            self._container.configure(width=self.width)
            if self.has_message: self._message.configure(width=self.width)

        if 'height' in kw and kw['height']!=None:
            self.height = kw['height']
            self._container.configure(height=self.height)
        
        if 'bordercolor' in kw and kw['bordercolor']!=None:
            self.bordercolor = kw['bordercolor']
            self._container.configure(highlightbackground=self.bordercolor)
        if 'borderwidth' in kw and kw['borderwidth']!=None:
            self.borderwidth = kw['borderwidth']
            self._container.configure(highlightthickness=self.borderwidth)

        if 'anchor' in kw and kw['anchor']!=None:
            if kw['anchor'] in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center']:
                self.anchor = kw['anchor']
            else: raise _tkinter.TclError('bad anchor "%s": must be n, ne, e, se, s, sw, w, nw, or center'%(kw['anchor']))
        
        if 'ipadx' in kw and kw['ipadx']!=None:
            self.ipadx = kw['ipadx']
            self._container.configure(padx=self.ipadx)

        if 'ipady' in kw and kw['ipady']!=None:
            self.ipady = kw['ipady']
            self._container.configure(pady=self.ipady)

        if 'bg' in kw and kw['bg']!=None:
            self.bg = kw['bg']
            self._container.configure(bg=self.bg)
            if self.has_message: self._message.configure(bg=self.bg)

        if 'fg' in kw and kw['fg']!=None:
            self.fg = kw['fg']
            if self.has_message: self._message.configure(fg=self.fg)
        
        self.update()
    config = configure

    def destroy(self):
        self._remove_binds()
        self._container.destroy()
        super().destroy()