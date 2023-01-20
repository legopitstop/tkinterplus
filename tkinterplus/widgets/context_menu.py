import tkinter
import _tkinter

class ContextMenu(tkinter.Menu):
    def __init__(self,master: tkinter.Tk,showcommand=None):
        """Make a right click context menu."""
        tkinter.Menu.__init__(self,master, tearoff=False)
        self.master=master
        self.state = tkinter.NORMAL
        self.showcommand = None
        self.enable()
        self.configure(showcommand=showcommand)

    def _mouse(self,e):
        """Internal Function"""
        if self.showcommand!=None: self.showcommand()
        try: self.tk_popup(e.x_root, e.y_root, 0)
        finally: self.grab_release()

    def conifgure(self,**kw):
        """Config the context menu"""
        if 'showcommand' in kw and kw['showcommand']!=None: self.showcommand = kw['showcommand']
        if 'state' in kw and kw['state']!=None:
            self.state = kw['state']
            if self.state==tkinter.NORMAL: self.enable()
            elif self.state==tkinter.DISABLED or self.state=='readonly': self.disable()
    config = conifgure
    

    def _app(self,e):
        """Internal Function"""
        try: self.tk_popup(0,0, 0)
        finally: self.grab_release()

    def disable(self):
        """Unbind context menu so it will not show"""
        self.master.unbind("<Button-3>")
        self.master.unbind('<App>')
    
    def enable(self):
        """Bind the context menu so it will show"""
        self.master.bind("<Button-3>", self._mouse)
        self.master.bind('<App>', self._app)
    
    #NOTE Disable btn if selected widget is not a `Text` widget.
    # def add_command(self,cnf:dict=None, accelerator:str=None, activebackground=None, activeforeground=None, background=None, bitmap=None, columnbreak:int=None, command=None, compound=None, font=None, foreground=None, hidemargin:bool=None, image=None, label:str=None, state=None, underline:int=None, **kw):

    def add_command(self,cnf={},**kw):
        """
        Add command menu item. add type for a built-in command ie. type=ContextMenuType.COPY
        
        Arguments
        ---
        label, command, type
        """
        # self.winfo_atomname()
        def cut():
            copy()
            delete()

        def copy():
            try:
                focus = self.focus_get()
                if focus.winfo_class() == 'Text':
                    focus.clipboard_clear()
                    focus.clipboard_append(focus.selection_get())
                    return True
                else:
                    return False
            except _tkinter.TclError:
                return False

        def paste():
            delete()
            focus = self.focus_get()
            focus.insert(focus.index(tkinter.INSERT), focus.clipboard_get())
            return True

        def delete():
            focus = self.focus_get()
            try:
                first =focus.index(tkinter.SEL_FIRST)
                last=focus.index(tkinter.SEL_LAST)
                focus.delete(first,last)
                return True
            except _tkinter.TclError:
                return False

        def select_all():
            focus = self.focus_get()
            focus.tag_add(tkinter.SEL, "1.0", tkinter.END)
            focus.mark_set(tkinter.INSERT, "1.0")
            focus.see(tkinter.INSERT)
            return True

        def undo():
            try:
                focus:tkinter.Text = self.focus_get()
                focus.edit_undo()
                return True
            except AttributeError:
                return False
        
        def redo():
            try:
                focus:tkinter.Text = self.focus_get()
                focus.edit_redo()
                return True
            except _tkinter.TclError:
                return False
            except AttributeError:
                return False

        def run_command(name):
            focus = self.focus_get()
            if focus.winfo_class() == 'Text':
                print('WORKED: ',name)

        # Apply commands to type
        try:
            type = kw['type']
            kw['command'] = lambda: run_command(type)
            del kw['type']
        except: pass

        self.add('command', cnf or kw)
