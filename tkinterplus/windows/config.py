import tkinter
from .. import Footer, Input

class Config(tkinter.Toplevel):
    def __init__(self,master:tkinter.Tk=None,title=None,prompt=None,confirmcommand=None,icon=None,theme=None):
        """Construct a config widget with the parent MASTER."""
        tkinter.Toplevel.__init__(self,master)
        self.minsize(300,50)
        self.resizable(False,False)

        if icon!=None: self.iconbitmap(icon)
        if title!=None: self.title(title)
        elif master!=None:
            self.title(master.title())

        self.option = tkinter.Frame(self)
        self.option.grid(row=0,column=0)

        # Footer
        foot = Footer(self)
        foot.add_button('Confirm',self._confirm)
        foot.add_button('Cancel',self.destroy)

        self._row=0
        self._column=0
        self._cmd=confirmcommand
        self._config={}

        if theme!=None:
            pass
            # self.theme = TkThemeLoader(self)
            # self.theme.loadStyleSheet(theme)
        else:
            self.theme=None

    def _confirm(self):
        print('confirmed')
        self._cmd(self.get())
        self.destroy()

    def get(self):
        """Returnss an object containing the new config."""
        out = {}
        for n in self._config:
            out[n] = self._config[n].get()
        return out

    def add_string(self,name,label=None,required=False):
        """Add a string option to the config"""
        VAR = tkinter.StringVar()
        tkinter.Label(self.option,text=label).grid(row=self._row,column=0,sticky=tkinter.E)
        tkinter.Entry(self.option,textvariable=VAR).grid(row=self._row,column=1,sticky=tkinter.W)
        if self.theme!=None: self.theme.reloadStyleSheet()
        self._config[name] = VAR
        self._row+=1

    def add_boolean(self,name,label=None,required=False):
        """Add a boolean (checkbox) option to the config"""
        VAR = tkinter.BooleanVar()
        tkinter.Label(self.option,text=label).grid(row=self._row,column=0,sticky=tkinter.E)
        tkinter.Checkbutton(self.option,variable=VAR,onvalue=True,offvalue=False).grid(row=self._row,column=1,sticky=tkinter.W)
        if self.theme!=None: self.theme.reloadStyleSheet()
        self._config[name] = VAR
        self._row+=1

    def add_integer(self,name,label=None,min=None,max=None,required=False):
        """Add an integer option to the config"""
        VAR = tkinter.IntVar()
        tkinter.Label(self.option,text=label).grid(row=self._row,column=0,sticky=tkinter.E)
        tkinter.Spinbox(self.option,textvariable=VAR,from_=min,to=max,increment=1).grid(row=self._row,column=1,sticky=tkinter.W)
        if self.theme!=None: self.theme.reloadStyleSheet()
        self._config[name] = VAR
        self._row+=1

    def add_float(self,name,label=None,min=None,max=None,required=False):
        """Add a float option to the config"""
        tkinter.Label(self.option,text=label).grid(row=self._row,column=0,sticky=tkinter.E)
        VAR = tkinter.Spinbox(self.option,from_=min,to=max,increment=0.1)
        VAR.grid(row=self._row,column=1,sticky=tkinter.W)
        if self.theme!=None: self.theme.reloadStyleSheet()
        self._config[name] = VAR
        self._row+=1

    def add_enum(self,name,label=None,required=False):
        """Add an enum option to the config"""
        values=['item1','item2']
        VAR = tkinter.StringVar()
        VAR.set(values[0])
        tkinter.Label(self.option,text=label).grid(row=self._row,column=0,sticky=tkinter.E)
        tkinter.OptionMenu(self.option,VAR,*values).grid(row=self._row,column=1,sticky=tkinter.W)
        if self.theme!=None: self.theme.reloadStyleSheet()
        self._config[name] = VAR
        self._row+=1

    def add_filename(self,name,label=None,required=False):
        """Add a file option to the config"""
        VAR = tkinter.StringVar()
        tkinter.Label(self.option,text=label).grid(row=self._row,column=0,sticky=tkinter.E)
        Input(self.option,'file',textvarable=VAR).grid(row=self._row,column=1,sticky=tkinter.W)
        if self.theme!=None: self.theme.reloadStyleSheet()
        self._config[name] = VAR
        self._row+=1

    def add_directory(self,name,label=None,required=False):
        """Add a directory option to the config"""
        VAR = tkinter.StringVar()
        tkinter.Label(self.option,text=label).grid(row=self._row,column=0,sticky=tkinter.E)
        Input(self.option,'directory',textvarable=VAR).grid(row=self._row,column=1,sticky=tkinter.W)
        if self.theme!=None: self.theme.reloadStyleSheet()
        self._config[name] = VAR
        self._row+=1

    def add_color(self,name,label=None,required=False):
        """Add a color option to the config"""
        tkinter.Label(self.option,text=label).grid(row=self._row,column=0,sticky=tkinter.E)
        Input(self.option,'color').grid(row=self._row,column=1,sticky=tkinter.W)
        if self.theme!=None: self.theme.reloadStyleSheet()
        self._row+=1

    def add_object(self,name,label=None,required=False):
        if label!=None:
            tkinter.LabelFrame(self.option).grid(row=self._row,column=0)
            print(label)
        else:
            print('frame')
