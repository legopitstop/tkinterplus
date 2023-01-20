import tkinter
from tkinter import ttk
from .. import GRID, util

class Footer():
    def __init__(self, master:tkinter.Tk=None, bg:str=None):
        """Construct a footer widget with the parent MASTER."""
        if master is None: master = tkinter._get_temp_root()

        # Arguments
        self.bg = '#f0f0f0'

        # varables
        self.manager = util.winfo_geometry_manager(master)
        self.col=1
        self.master = master
        self.buttons=[]
        self._btn_count=0

        # frame that holds all widgets.
        self._container = tkinter.Frame(self.master,bg=self.bg)
        self._content = tkinter.Frame(self._container,bg=self.bg,width=0, padx=10)
        self._content.grid(row=0,column=0, sticky=tkinter.EW)

        self.configure(
            bg=bg
        )

        # Arguments for tk
        self.children = self._content.children
        self.tk = self._content.tk
        self._w = self._content._w
        self._last_child_ids = self._content._last_child_ids
        self._geo()
    
    def _geo(self):
        """Place the footer using the suggested geometry method"""
        self._container.grid_columnconfigure(0,weight=1)

        if self.manager == GRID:
            # get the grid geo of the window.
            slaves = self.master.grid_slaves()
            self._row = slaves[0].grid_info()['row']+1
            self._column = slaves[0].grid_info()['column']
            # Apply the auto grid
            self._container.grid(row=self._row,column=0, columnspan=self._column+1,sticky='ews')

            self.master.grid_columnconfigure(0,weight=1)
            self.master.grid_rowconfigure(self._row,weight=1)
            # self._container.grid_columnconfigure(0,weight=1)
        
        else:
            self._container.pack(expand=True, fill=tkinter.X, anchor=tkinter.S)

    def add_button(self,text:str=None, **kw):
        """Add a button to the footer"""
        btnbg='#e1e1e1'
        btnbd='#adadad'
        btn = ttk.Button(self._container,text='FooterButton')
        btn.grid(row=0,column=self.col,sticky=tkinter.E, padx=(0, 10), pady=5)
        btn.configure(text=text,**kw)
        self.buttons.append(btn)
        self._container.update()
        self._btn_count+=1
        self.col+=1

    def remove_button(self,index):
        """Delete a button from the footer"""
        self.buttons[index].destroy()

    def configure_button(self, index:int, **kw):
        """Update the buttons properties"""
        self.buttons[index].configure(**kw)

    config_button = configure_button

    def configure(self, **kw):
        if 'bg' in kw:
            self.bg = kw['bg']
            self._container.configure(bg=self.bg)
            self._content.configure(bg=self.bg)
