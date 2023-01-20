from tkinter import ACTIVE, BOTH, NE, NORMAL, NW, X, Y, Tk, StringVar, Frame, Label, _get_temp_root

class Notification():
    def __init__(self, master:Tk=None, text:str=None, textvariable:StringVar=None, state:str=None, anchor:str=None, bg:str=None, fg:str=None):
        if master is None: master = _get_temp_root()

        # Arguments
        self.master = master
        self.textvariable = StringVar()
        self.state = NORMAL
        self.anchor = NW
        self.bg = 'black'
        self.fg = 'white'
        self.x0 = -100
        self.y0 = -100
        self.x1 = -8
        self.y1 = -8

        self.frame = Frame(self.master, bg=self.bg, cursor='hand2')
        self._text = Label(self.frame, textvariable=self.textvariable, bg=self.bg, fg=self.fg, padx=10, pady=10)
        self._text.pack(expand=True, fill=BOTH)

        self.configure(
            text=text,
            textvariable=textvariable,
            state=state,
            anchor=anchor,
            bg=bg,
            fg=fg
        )
        
        # Arguments for tk
        self.children = self.frame.children
        self.tk = self.frame.tk
        self._w = self.frame._w
    
    def _slide(self, start:int, stop:int, cord:str, time:int):
        frames = list(range(start, stop))
        if cord == X: self.frame.place(x=start)
        elif cord == Y: self.frame.place(y=start)

        ms = time / len(frames)
        t = 0
        for f in frames:
            if cord == X: self.frame.after(int(t), lambda frame=f: self.frame.place(x=frame))
            elif cord == Y: self.frame.after(int(t), lambda frame=f: self.frame.place(y=frame))
            t += ms

        # self.frame.place(x=0, y=0)
        return self

    def show(self, ms:int=500, hide_after:int=None):
        """Show the notification"""
        if self.state==NORMAL:
            self.configure(state=ACTIVE)

            print(self.x0, self.x1)
            print(self.y0, self.y1)
            self.frame.place(y=self.y0)
            if ms > 0: self._slide(self.x0, self.x1, X, ms)
            else: self.frame.place(x=self.x1, y=self.y1)

            if hide_after!=None: self.frame.after(hide_after, lambda ms: self.hide(ms))
        return self
    
    def hide(self, ms:int=500):
        """hide the notification"""
        if self.state == ACTIVE:
            self.configure(state=NORMAL)
            # self._slide(-100, 1, X, ms)
            self.frame.place_forget()
        return self

    def configure(self, **kw):
        if 'text' in kw and kw['text']!=None: self.textvariable.set(kw['text'])
        if 'textvariable' in kw and kw['textvariable']!=None:
            self.textvariable = kw['textvariable']
            self._text.configure(textvariable=self.textvariable)

        if 'state' in kw and kw['state']!=None: self.state = kw['state']

        if 'bg' in kw and kw['bg']!=None:
            self.bg = kw['bg']
            self.frame.configure(bg=self.bg)
            self._text.configure(bg=self.bg)

        if 'fg' in kw and kw['fg']!=None:
            self.fg = kw['fg']
            self._text.configure(fg=self.fg)

        if 'anchor' in kw and kw['anchor']!=None:
            values = ['n','e','s','w', 'ne', 'nw', 'se', 'sw', 'center']
            if kw['anchor'] in values:
                self.anchor = kw['anchor']
                if self.anchor == 'center':
                    self.x = 0
                    self.y = 0
                else:
                    self.master.update()
                    for k in self.anchor:
                        if k == 'n': 
                            self.y0 = -100
                            self.y1 = -8
                        elif k == 's':
                            self.y0 = -100
                            self.y1 = self.master.winfo_height() - 100

                        elif k == 'e':
                            self.x0 = -100
                            self.x1 = self.master.winfo_width() - 100
                        elif k == 'w':
                            self.x0 = -100
                            self.x1 = -8
            else: KeyError('Expected %s'%values)
        return self
    config = configure