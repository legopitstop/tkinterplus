from tkinter import DISABLED, EW, NORMAL, W, Frame, PhotoImage, Tk, StringVar, Button

#NOTE This widget is still being worked on. Expect issues for missing features!
class Tabview(Frame):
    def __init__(self, master:Tk=None, variable:StringVar=None, bg:str=None):
        """Construct a tabs widget with the parent MASTER."""
        self._tab_dict = {}
        self._column = 0
        self.variable = StringVar()
        self.bg = '#f0f0f0'

        # Widgets
        super().__init__(master, bg=self.bg)
        self.btns = Frame(self, bg=self.bg)
        self.btns.grid(row=0,column=0, sticky=EW)

        # Resopnsve
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.configure(
            variable=variable,
            bg=bg
        )

    def _get_tab(self, name:str):
        for t in self.tabs:
            if t['name'] == name: return t
        return None

    def _create_tab(self) -> Frame:
        return Frame

    def remove(self, name:str):
        """Remove the tab"""
        t = self._get_tab(name)
        if t!=None:
            t['frame'].destroy()
            t['button'].destroy()
            self.tabs.remove(t)
  
    def tab(self, name:str) -> Frame:
        """returns reference to the tab with given name"""
        if name in self._tab_dict: return self._tab_dict[name]
        else: raise ValueError(f"Tabview has no tab named '{name}'")

    def insert(self, index:int, name:str) -> Frame:
        """creates new tab with given name at position index"""
        raise ValueError(f"Tabview already has tab named '{name}'")

    

    def add(self, name:str) -> Frame:
        return self.insert(len(self._tab_dict), name)

    # remove
    def _add(self, name:str) -> Frame:
        """appends new tab with given name"""
        tab = Frame(self, bg=self.bg)
        if name is None: name = tab.winfo_name()

        # Add buttons
        btn = Button(self.btns, command=lambda n=name: self.show_tab(n))
        btn.grid(row=0, column=self._column, sticky=W, padx=(0, 2))
        self.tabs.append({'button': btn, 'frame': tab, 'name': name})

        self.tabconfigure(
            name=name
        )

        self._column+=1
        tab.bind('<Destroy>', lambda e, n=name: self.remove(n))
        
        raise ValueError(f"Tabview already has tab named '{name}'")
        return tab


    def move(self, new_index:int, name:str):
        raise ValueError(f"Tabview has no tab named '{name}'")

    def delete(self, name:str):
        """delete tab by name"""
        raise ValueError(f"Tabview has no tab named '{name}'")

    def set(self, name:str):
        """select tab by name"""
        raise ValueError(f"Tabview has no tab named '{name}'")

    # replaced with .set()
    def show_tab(self, name:str):
        self.hide_tab('all')
        t = self._get_tab(name)
        if t!=None:
            t['button'].configure(state=DISABLED)
            t['frame'].grid(row=1, column=0, sticky='nesw')
            self.variable.set(name)
        
    def hide_tab(self, name:str):
        if name!='all':
            t = self._get_tab(name)
            if t!=None:
                t['button'].configure(state=NORMAL)
                t['frame'].grid_forget()
                self.variable.set('')
        else:
            for t in self.tabs:
                t['button'].configure(state=NORMAL)
                t['frame'].grid_forget()

    # add to self.configure() with prefix "button_<arg>"
    def tabconfigure(self, name:str, **kw):
        t = self._get_tab(name)
        if t!=None: t['button'].configure(**kw)


    def configure(self,**kw):
        if 'variable' in kw and kw['variable']!=None: self.variable = kw['variable']
        if 'bg' in kw and kw['bg']!=None:
            self.bg = kw['bg']
            super().configure(bg=self.bg)
            self.btns.configure(bg=self.bg)
            for t in self.tabs:
                t['frame'].configure(bg=self.bg)
    config = configure
    