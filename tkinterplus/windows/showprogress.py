from tkinter import W, EW, Toplevel, Tk, IntVar, Label
from tkinter.ttk import Progressbar

from .. import Footer

class ShowProgress(Toplevel):
    def __init__(self,master:Tk=None,title:str=None,label:str=None,value:float=None,max:float=None,completecommand=None):
        """Creates a progress window"""
        Toplevel.__init__(self,master)
        self.minsize(300,50)
        self.resizable(False,False)

        if title!=None:
            self.title(title)
        elif master!=None:
            self.title(master.title())
        
        # Value
        self.label=label
        self.value=value
        self.max=max
        self._complete=completecommand

        self._varable=IntVar()
        if value!=None:
            self._varable.set(self.value)

        # Label
        if self.label!=None:
            self._label = Label(self,text=self.label)
            self._label.grid(row=0,column=0,padx=10,sticky=W)

        # Progressbar
        self._bar = Progressbar(self,mode='determinate',variable=self._varable,maximum=max)
        self._bar.grid(row=1,column=0,padx=10,sticky=EW)

        # Footer
        self._foot = Footer(self)
        self._foot.add_button(text='Cancel',command=self.destroy)

        self.iconify()

    def config(self,master:Tk=None,label:str=None,value:float=None,max:float=None):
        """Update the progressbar"""
        if label:
            self._label['text'] = label

        if value:
            self._varable.set(value)
            if value>=self.max:
                if value==self.max:
                    self._foot.config_button(0,'Close')
                    self._complete()
        if max:
            self._bar['maximum'] = max

    def step(self,amount:float=None):
        """Increments the value option by amount."""
        n = self.get()
        if amount!=None:
            self.config(value=n+amount)
        else:
            self.config(value=n+1)

    def get(self):
        """Returns the currrent value"""
        return self._varable.get()
