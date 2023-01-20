import tkinter
from .. import Footer

class AskEnum(tkinter.Toplevel):
    def __init__(self,master:tkinter.Tk=None,title=None,prompt=None,default=None,value:list=None,*values):
        """Construct a askenum widget with the parent MASTER."""
        tkinter.Toplevel.__init__(self,master)
        self.minsize(300,50)
        self.resizable(False,False)
        self.varable = tkinter.StringVar()

        if title!=None:
            self.title(title)
        elif master!=None:
            self.title(master.title())

        # Default value
        if default!=None:
            self.varable.set(default)
        else:
            self.varable.set(value[0])


        tkinter.Label(self,text=prompt).grid(row=0,column=0, sticky=tkinter.W)
        tkinter.OptionMenu(self,self.varable,*value).grid(row=1,column=0)

        # Footer
        foot = Footer(self)
        foot.add_button(text='Confirm',command=self._confirm)
        foot.add_button(text='Cancel',command=self._cancel)

    def _confirm(self):
        print(self.varable.get())
        self.destroy()

    def _cancel(self):
        print(False)
        self.destroy()
