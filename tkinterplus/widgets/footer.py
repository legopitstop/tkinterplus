from tkinter import SOLID, E, Frame, Tk, Button

class Footer(Frame):
    def __init__(self, master:Tk, bg_color:str=None, **kw):
        """Adds a frame at the bottom of the window that is the full width of the window."""
        # Parameters
        self.bg_color = '#f0f0f0'

        # get the grid geo of the window.
        slaves = master.grid_slaves()
        self._row = slaves[0].grid_info()['row']+1
        self._column = slaves[0].grid_info()['column']

        # varables
        self.col=1
        self.master = master
        self.buttons=[]
        self._btn_count=0

        # frame that holds all widgets.
        Frame.__init__(self, self.master,bg=self.bg_color)

        # Apply the auto grid
        self.grid(row=self._row,column=0, columnspan=self._column+1,sticky='ews')

        # Button Container
        self.container = Frame(self,bg=self.bg_color)
        self.container.grid(row=0,column=1)

        # Create spacer
        self.spacer = Frame(self,bg=self.bg_color,width=0)
        self.spacer.grid(row=0,column=0)

        self.grid_columnconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.master.grid_rowconfigure(self._row,weight=1)

        self.configure(bg_color=bg_color)

    def add_button(self,text:str=None,command=None, padx:int=10, pady:int=5, ipadx:int=None, ipady:int=None):
        """Add a button to the footer"""
        btnbg='#e1e1e1'
        btnbd='#adadad'
        btn = Button(self.container,text=text,command=command,padx=20,relief=SOLID,activebackground=btnbg,bg=btnbg,highlightbackground=btnbd,highlightthickness=1,bd=1)
        btn.grid(row=0,column=self.col,sticky=E, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        self.buttons.append(btn)
        self.container.update()
        self._btn_count+=1
        self.col+=1

    def remove_button(self,index):
        """Delete a button from the footer"""
        self.buttons[index].destroy()

    def config_button(self,index,text:str=None,command=None):
        """Update the buttons properties"""
        btn = self.buttons[index]
        if text!=None:
            btn['text'] = text

        if command!=None:
            btn['command'] = command

    def configure(self, **kw):
        if 'bg_color' in kw:
            self.bg_color = kw['bg_color']
            super().configure(bg=self.bg_color)
            self.container.configure(bg=self.bg_color)
            self.spacer.configure(bg=self.bg_color)
