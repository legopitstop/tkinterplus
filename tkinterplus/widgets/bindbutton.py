import tkinter

class BindButton(tkinter.Frame):
    def __init__(self, master:tkinter.Tk, variable:tkinter.StringVar=None, seperator:str=None, command=None, **kw):
        super().__init__(master)
        self.variable = tkinter.StringVar()
        self.command = None
        self._button_variable = tkinter.StringVar()
        self.seperator = '+'

        # Widget
        self.button = tkinter.Button(self, textvariable=self._button_variable, disabledforeground='black', command=self.listen)
        self.button.pack(expand=1, fill=tkinter.BOTH)

        self.configure(
            variable=variable,
            command=command,
            seperator=seperator,
            **kw
        )

    def _seq(self, e:tkinter.Event):
        # 0x0001 Shift
        # 0x0002 caps Lock
        # 0x0004 Control
        # 0x0008 left alt
        # 0x0010 num lock
        # 0x0080 right alt
        # 0x0100 mouse 1
        # 0x0200 mouse 2
        # 0x0400 mouse 3
        seq = []
        if (e.state & 0x0004) > 0: seq.append('Control')
        if e.keysym == 'Control_L' or e.keysym=='Control_R': return '<'+e.keysym+'>'
        else: seq.append(e.keysym)
        return '<'+'-'.join(seq)+'>'
        
    def _display(self, seq:str):
        keys = seq.replace('<','').replace('>','').split('-')
        res = []
        for k in keys:
            if len(k)==1 and k.isupper():
                res.append('Shift')
                res.append(k.lower())
            else: res.append(k)
        return self.seperator.join(res)

    def callback(self, e:tkinter.Event):
        seq = self._seq(e)
        self.variable.set(seq)
        self.button.configure(state=tkinter.NORMAL)
        self.master.unbind_all('<KeyRelease>')
        if self.command!=None: self.command()

    def listen(self):
        self.button.configure(state=tkinter.DISABLED)
        self._button_variable.set('> <')
        self.master.bind_all('<KeyRelease>', self.callback)

    def get(self): return self.variable.get()
    def set(self, value:str): return self.variable.set(value)

    def configure(self, **kw):
        if 'variable' in kw and kw['variable']!=None:
            self.variable:tkinter.StringVar = kw.pop('variable')
            self.variable.trace_add('write', lambda a,b,c: self._button_variable.set(self._display(self.variable.get()))) # update btn text
            self._button_variable.set(self._display(self.variable.get()))

        if 'command' in kw and kw['command']!=None: self.command = kw.pop('command')
        if 'seperator' in kw and kw['seperator']!=None: self.seperator = kw.pop('seperator')

        # Remove
        remove = ['textvariable']
        for r in remove:
            if r in kw: del kw[r]
        self.button.configure(**kw)

    config = configure