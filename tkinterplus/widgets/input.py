from tkinter import Frame, Tk, StringVar, colorchooser, filedialog, Button, Entry, Spinbox, Label
import os
import re

from .. import Tooltip

class Input(Frame):
    def __init__(self, master:Tk=None,type='text',**kw):
        """A more advanced Entry widget aviable in more types."""
        Frame.__init__(self, master)

        # Textvar
        try: VALUE:StringVar = kw['textvariable']
        except: VALUE:StringVar=''
        try: self.pattern = kw['pattern']
        except: self.pattern= r'.*'
        self._call = master.register(self._callback)

        def _update(var):
            """Update the textvarable"""
            try: VALUE.set(var)
            except: pass

        def _color():
            color = colorchooser.askcolor()[1]
            if color!=None:
                COLOR['bg'] = color
                COLOR['activebackground'] = color
                COLOR['text'] = color
                _update(color)

        def _file():
            try: file = os.path.basename(VALUE.get())
            except: file=None

            try: de = kw['defaultextension']
            except: de = None
            try: ft = kw['filetypes']
            except: ft = [('Any', '*')]
            try: id = kw['initialdir']
            except: id = None
            try: ttl = kw['title']
            except: ttl = None

            path = filedialog.askopenfilename(defaultextension=de,filetypes=ft,initialdir=id,initialfile=file,title=ttl)
            if path!='':
                # print(path)
                _update(path)
                FILEL['text'] = os.path.basename(path)
                FILET.msg=path

        def _directory():
            try: me = kw['mustexist']
            except: me = None
            try: id = kw['initialdir']
            except: id = None
            try: ttl = kw['title']
            except: ttl = None

            path = filedialog.askdirectory(mustexist=me,initialdir=id,title=ttl)
            if path!='':
                _update(path)
                FILEL['text'] = os.path.basename(path)
                FILET.msg=path

        if type=='color':
            try: C = VALUE.get()
            except: C='#ffffff'
            COLOR = Button(self,text=C,bg=C,activebackground=C,command=_color)
            COLOR.pack()

        elif type=='text':
            TEXT=Entry(self,textvariable=VALUE)
            TEXT.config(validate='key', validatecommand=(self._call, '%P'))
            TEXT.pack()

        elif type=='password':
            TEXT=Entry(self,textvariable=VALUE,show='*')
            TEXT.config(validate='key', validatecommand=(self._call, '%P'))
            TEXT.pack()
            
        elif type=='number':
            try: MIN = kw['min']
            except: MIN=-1000
            try: MAX = kw['max']
            except: MAX=1000

            self.pattern = r'^[0-9]{0,}$|^-[0-9]{0,}$'
            TEXT=Spinbox(self,textvariable=VALUE,from_=MIN,to=MAX)
            TEXT.config(validate='key', validatecommand=(self._call, '%P'))
            TEXT.pack()

        elif type=='file':
            FILEB = Button(self,text='Choose File',command=_file)
            FILEB.grid(row=0,column=0)
            try:
                if VALUE.get()!='':
                    D = os.path.basename(VALUE.get())
                    T = VALUE.get()
                else:
                    D='No file chosen'
                    T='No file chosen'
            except:
                D='No file chosen'
                T='No file chosen'
            FILEL = Label(self,text=D)
            FILEL.bind('<Button-1>', lambda e: _file())
            FILEL.grid(row=0,column=1)
            FILET = Tooltip(FILEL,text=T)

        elif type=='directory':
            FILEB = Button(self,text='Choose Directory',command=_directory)
            FILEB.grid(row=0,column=0)
            try:
                if VALUE.get()!='':
                    D = os.path.basename(VALUE.get())
                    T = VALUE.get()
                else:
                    D='No directory chosen'
                    T='No directory chosen'
            except:
                D='No directory chosen'
                T='No directory chosen'
            FILEL = Label(self,text=D)
            FILEL.bind('<Button-1>', lambda e: _directory())
            FILEL.grid(row=0,column=1)
            FILET = Tooltip(FILEL,text=T)

    def _callback(self,input:str):
        """Validate entry"""
        if re.match(self.pattern, input) or input == '':
            return True
        else:
            return False
