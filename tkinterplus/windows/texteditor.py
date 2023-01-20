import os
import tkinter
import tkinter.filedialog as filedialog
from tkinter.scrolledtext import ScrolledText
from UserFolder import User, Config
import webbrowser
from .. import ContextMenu

class TextEditor(tkinter.Toplevel):
    def __init__(self, master:tkinter.Tk=None):
        """Construct a texteditor widget with the parent MASTER."""
        tkinter.Toplevel.__init__(self,master)
        self.user = User('com.legopitstop.TextEditor')
        
        self.geometry('620x377')
        self.saved=True
        self.path=None
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.protocol('WM_DELETE_WINDOW',self.exit)

        # self.os = platform.system()
        self.os = 'Linux'
        if self.os == 'Windows': self.app = WindowsEditor(self)
        elif self.os == 'Linux': self.app = LinuxEditor(self)
        elif self.os == 'Darwin': self.app = DarwinEditor(self)
        else: self.app = DefaultEditor(self)

    def exit(self): self.destroy()

    def open(self,fp:str,mode='r'):
        """Reads, then applies the text from the file to the textarea"""
        if mode=='r':
            opn = open(fp,'r')
            self.set(opn.read())
            opn.close()
            self.path=fp
        elif mode=='w':
            print('saved')
            wrt = open(fp,'w')
            wrt.write(self.get())
            wrt.close()

    def set(self,text:str):
        """Set text in textarea"""
        self.delete()
        self.app.textarea.insert(1.0,text)

    def delete(self):
        """Clears all text in textarea"""
        self.app.textarea.delete(1.0,tkinter.END)

    def get(self):
        """Get text inside textarea"""
        return self.app.textarea.get(1.0,tkinter.END)

class WindowsEditor():
    def __init__(self, master):
        """Text editor for Windows https://en.wikipedia.org/wiki/Windows_Notepad"""
        self.m:TextEditor = master
        self.m.title('Notepad')
        # config
        d = Config(self.m.user)
        d.setItem('win.wordwrap', True)
        d.setItem('win.statusbar', True)
        # d.setItem('win.keybinds', {'Open': 'Control-o','Save': 'Control-s','SaveAs': 'Control-S','Print': 'Print','Search': 'Control-e','Find': 'Control-f','FindNext': 'F3','FindPrevious': 'Shift-F3','Replace': 'Control-h','GoTo': 'Control-g','TimeDate': 'F5','ZoomIn': 'Control-Plus','ZoomOut': 'Control-Minus','RestoreDefaultZoom': 'Control-0','Help':'Control-question'})
        self.c = d.section('win')  

        # Varables
        self.WORD_WRAP=tkinter.BooleanVar()
        self.WORD_WRAP.set(self.c.getItem('win.wordwrap'))
        self.STATUS_BAR=tkinter.BooleanVar()
        self.STATUS_BAR.set(self.c.getItem('win.statusbar'))

        # Widgets
        self.textarea = ScrolledText(self.m,bd=0,width=69,height=23,undo=True)
        self.textarea.grid(row=0,column=0,sticky='nesw')
        xscroll = tkinter.Scrollbar(self.m,orient=tkinter.HORIZONTAL, command=self.textarea.xview)
        xscroll.grid(row=1, column=0, sticky='nsew')
        self.textarea['xscrollcommand'] = xscroll.set
        
        # Binds
        self.m.bind('<Control-f>', lambda e: self.window('find'))
        self.m.bind('<F3>', lambda e: self.context('find_next'))
        self.m.bind('<Shift-F>', lambda e: self.context('find_previous'))
        self.m.bind('<Control-g>', lambda e: self.window('go_to'))
        self.m.bind('<Control-o>', lambda e: self.context('open'))
        self.m.bind('<Print>', lambda e: self.context('print'))
        self.m.bind('<Control-h>', lambda e: self.window('replace'))
        self.m.bind('<Control-0>', lambda e: self.context('restore_zoom'))
        self.m.bind('<Control-s>', lambda e: self.context('save'))
        self.m.bind('<Control-S>', lambda e: self.context('save_as'))
        self.m.bind('<Control-f>', lambda e: self.context('search'))
        self.m.bind('<F5>', lambda e: self.context('time_date'))
        self.m.bind('<Control-+>', lambda e: self.context('zoom_in'))
        # self.m.bind('<Control-->', lambda e: self._context('zoom_out'))
        self.m.bind('<Control-question>', lambda e: self.window('help'))
        
        # ContextMenu
        context=ContextMenu(self.textarea)
        context.add_command(label='Undo',command=lambda: self.context('undo'))
        context.add_command(label='Redo',command=lambda: self.context('redo'))
        context.add_separator()
        context.add_command(label='Cut',command=lambda: self.context('cut'))
        context.add_command(label='Copy',command=lambda: self.context('copy'))
        context.add_command(label='Paste',command=lambda: self.context('paste'))
        context.add_command(label='Delete',command=lambda: self.context('delete'))
        context.add_separator()
        context.add_command(label='Select All',command=lambda: self.context('select_all'))
        context.add_separator()
        context.add_command(label='Search Internet...',command=lambda: self.context('search'))
        
        # menu
        menu=tkinter.Menu(self.m,tearoff=False)
        file=tkinter.Menu(menu,tearoff=False)
        file.add_command(label='Open...',command=lambda: self.context('open'))
        file.add_command(label='Save',command=lambda: self.context('save'))
        file.add_command(label='Save As...',command=lambda: self.context('save_as'))
        file.add_separator()
        file.add_command(label='Page Setup...',command=lambda: self.context('page_setup'))
        file.add_command(label='Print...',command=lambda: self.context('print'))
        file.add_separator()
        file.add_command(label='Exit',command=self.m.exit)            
        
        edit=tkinter.Menu(menu,tearoff=False)
        edit.add_command(label='Undo',command=lambda: self.context('undo'))
        edit.add_command(label='Redo',command=lambda: self.context('redo'))
        edit.add_separator()
        edit.add_command(label='Cut',command=lambda: self.context('cut'))
        edit.add_command(label='Copy',command=lambda: self.context('copy'))
        edit.add_command(label='Paste',command=lambda: self.context('paste'))
        edit.add_command(label='Delete',command=lambda: self.context('delete'))
        edit.add_separator()
        edit.add_command(label='Search Internet...',command=lambda: self.context('search'))
        edit.add_command(label='Find...',command=lambda: self.window('find'))
        edit.add_command(label='Find Next',command=lambda: self.context('find_next'))
        edit.add_command(label='Find Previous',command=lambda: self.context('find_previous'))
        edit.add_command(label='Replace...',command=lambda: self.window('replace'))
        edit.add_command(label='Go To...',command=lambda: self.window('go_to'))
        edit.add_separator()
        edit.add_command(label='Select All',command=lambda: self.context('select_all'))
        edit.add_command(label='Time/Date',command=lambda: self.context('time_date'))
        
        format=tkinter.Menu(menu,tearoff=False)
        format.add_checkbutton(label='Word Wrap',offvalue=False,onvalue=True,variable=self.WORD_WRAP,command=self.update)
        format.add_command(label='Font...',command=lambda: self.window('font'))
        
        view=tkinter.Menu(menu,tearoff=False)
        
        zoom=tkinter.Menu(view,tearoff=False)
        zoom.add_command(label='Zoom In',command=lambda: self.context('zoom_in'))
        zoom.add_command(label='Zoom Out',command=lambda: self.context('zoom_out'))
        zoom.add_command(label='Restore Default Zoom',command=lambda: self.context('restore_zoom'))
        
        view.add_cascade(label='Zoom',menu=zoom)
        view.add_checkbutton(label='Status bar',offvalue=False,onvalue=True,variable=self.STATUS_BAR,command=self.update)
        
        help=tkinter.Menu(menu,tearoff=False)
        help.add_command(label='Keybinds',command=lambda: self.window('keybinds'))
        help.add_command(label='About',command=lambda: self.window('about'))
        
        menu.add_cascade(label='File',menu=file)
        menu.add_cascade(label='Edit',menu=edit)
        menu.add_cascade(label='Format',menu=format)
        menu.add_cascade(label='View',menu=view)
        menu.add_cascade(label='Help',menu=help)
        self.m.configure(menu=menu)
        
        # UPDATE
        self.update()

    def update(self):
        print('UPDATE')
        if self.STATUS_BAR.get():
            self.statusbar = tkinter.Frame(self.m)

            pos = tkinter.LabelFrame(self.statusbar)
            tkinter.Label(pos,text='Ln 14, Col 9').grid(row=0,column=0,sticky=tkinter.E)
            tkinter.Frame(pos,width=100).grid(row=0,column=1)
            pos.grid(row=0,column=0)
            
            zoom = tkinter.LabelFrame(self.statusbar)
            tkinter.Label(zoom,text='100%').grid(row=0,column=0,sticky=tkinter.E)
            zoom.grid(row=0,column=1)
            
            test = tkinter.LabelFrame(self.statusbar)
            tkinter.Label(test,text='UTF-8').grid(row=0,column=0,sticky=tkinter.E)
            tkinter.Frame(test,width=100).grid(row=0,column=1)
            test.grid(row=0,column=2)

            self.statusbar.grid(row=2,column=0,sticky=tkinter.E)
        else:
            try: self.statusbar.destroy()
            except AttributeError: pass

        if self.WORD_WRAP.get():
            self.textarea['wrap'] = tkinter.WORD

        else:
            self.textarea['wrap'] = tkinter.NONE
    
    def context(self, id:str):
        if id=='open':
            file = filedialog.askopenfilename(defaultextension='.txt',parent=self.m)
            if os.path.exists(file):
                self.m.open(file,'r')

        elif id=='save':
            if self.m.path!=None:
                self.m.open(self.m.path,'w')
            else:
                self._context('save_as')

        elif id=='save_as':
            file = filedialog.asksaveasfilename(confirmoverwrite=True,defaultextension='.txt',parent=self.m)
            if file!='':
                self.m.open(file,'w')

        elif id=='undo':
            self.textarea.edit_undo()

        elif id=='redo':
            self.textarea.edit_redo()

        elif id=='cut':
            self.context('copy')
            self.context('delete')

        elif id=='copy':
            focus = self.textarea.focus_get()
            if focus.winfo_class() == 'Text':
                try:
                    focus.clipboard_clear()
                    focus.clipboard_append(focus.selection_get())
                except: return False
            
        elif id=='paste':
            self.context('delete')
            focus:tkinter.Text = self.textarea.focus_get()
            if focus.winfo_class() == 'Text':
                try: focus.insert(focus.index(tkinter.INSERT), focus.clipboard_get())
                except: return False
            
        elif id=='delete':
            focus:tkinter.Text = self.textarea.focus_get()
            if focus.winfo_class() == 'Text':
                try:
                    first =focus.index(tkinter.SEL_FIRST)
                    last=focus.index(tkinter.SEL_LAST)
                    focus.delete(first,last)
                except: return False

        elif id=='select_all':
            focus = self.textarea.focus_get()
            focus.tag_add(tkinter.SEL, "1.0", tkinter.END)
            focus.mark_set(tkinter.INSERT, "1.0")
            focus.see(tkinter.INSERT)
        
        elif id=='search':
            focus = self.textarea.focus_get()
            if focus.winfo_class() == 'Text':
                try:
                    webbrowser.open('https://www.google.com/search?q='+focus.selection_get().replace(' ','+'))
                except: return False
        else:
            print('Context',id)

    def window(self, id:str):
        if id=='none':
            pass

        else:
            print('Window',id)

class LinuxEditor():
    def __init__(self, master):
        """Text editor for Linux https://en.wikipedia.org/wiki/Vim_(text_editor)"""
        self.m:TextEditor = master
        self.m.title('Vim')
        
        # Config
        d = Config(self.m.user)
        self.c = d.section('lin')

        # Binds

        # Widgets
        self.textarea = ScrolledText(self.m,bd=0,width=69,height=23,undo=True, bg='black', fg='white', insertbackground='white', insertwidth=10)
        self.textarea.grid(row=0,column=0,sticky='nesw')
        

class DarwinEditor():
    def __init__(self, master):
        """Text editor for Darwin https://en.wikipedia.org/wiki/TextEdit"""
        self.m:TextEditor = master
        self.m.title('TextEdit')
        
        # Config
        d = Config(self.m.user)
        self.c = d.section('mac')
        
        # Binds
        
        # Menu
        self.menu = tkinter.Menu(self.m)
        self.textedit = tkinter.Menu(self.menu)
        self.textedit.add_command(label='About')
        self.textedit.add_separator()
        self.textedit.add_command(label='Preferences...')
        self.textedit.add_separator()
        self.textedit.add_cascade(label='Services')
        self.textedit.add_separator()
        self.textedit.add_command(label='Hide TextEdit')
        self.textedit.add_command(label='Hide Others')
        self.textedit.add_command(label='Show All')
        self.textedit.add_separator()
        self.textedit.add_command(label='Quit TextEdit', command=self.m.exit)
        self.menu.add_cascade(label='TextEdit', menu=self.textedit)

        self.file = tkinter.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.menu)
        
        self.edit = tkinter.Menu(self.menu)
        self.menu.add_cascade(label='Edit', menu=self.edit)
        
        self.format = tkinter.Menu(self.menu)
        self.format.add_cascade(label='Font')
        self.format.add_cascade(label='Text')
        self.format.add_separator()
        self.format.add_command(label='Make Plain Text')
        self.format.add_command(label='Prevent Editing')
        self.format.add_command(label='Wrap to Page')
        self.format.add_command(label='Allow Hyphenation')
        self.format.add_command(label='Make Layout Vertical')
        self.format.add_separator()
        self.format.add_command(label='List...')
        self.format.add_command(label='Table...')
        self.menu.add_cascade(label='Format', menu=self.format)
        
        self.view = tkinter.Menu(self.menu)
        self.view.add_command(label='Show Tab Bar')
        self.view.add_separator()
        self.view.add_command(label='Actual zoom')
        self.view.add_command(label='Zoom In')
        self.view.add_command(label='Zoom Out')
        self.view.add_separator()
        self.view.add_command(label='Enter Full Screen')
        self.menu.add_cascade(label='View', menu=self.view)
        
        self.window = tkinter.Menu(self.menu)
        self.menu.add_cascade(label='Window', menu=self.window)
        
        self.help = tkinter.Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.help)

        self.m.configure(menu=self.menu)

        # Widgets
        self.textarea = ScrolledText(self.m,bd=0,width=69,height=23,undo=True)
        self.textarea.grid(row=0,column=0,sticky='nesw')

class DefaultEditor():
    def __init__(self, master):
        """The default editor"""
        self.m:TextEditor = master
        self.m.title('TextEditor')
        self.textarea = ScrolledText(self.m,bd=0,width=69,height=23,undo=True, wrap=tkinter.NONE)
        self.textarea.grid(row=0,column=0,sticky='nesw')
        xscroll = tkinter.Scrollbar(self.m,orient=tkinter.HORIZONTAL, command=self.textarea.xview)
        xscroll.grid(row=1, column=0, sticky='nsew')
        self.textarea['xscrollcommand'] = xscroll.set