from tkinter import HORIZONTAL, INSERT, SEL_FIRST, SEL_LAST, SEL, END, E, NORMAL, W, WORD, NONE, LabelFrame, Button, Frame, StringVar, Label, Entry, Toplevel, Tk, BooleanVar, Scrollbar, Menu, filedialog, Text
from tkinter.scrolledtext import ScrolledText
from UserFolder import User
import webbrowser
import yaml

from .. import ContextMenu, Footer

class TextEditor(Toplevel):
    def __init__(self, master:Tk=None, title:str=None, iconbitmap:str=None):
        Toplevel.__init__(self,master)

        # Config
        self.user = User('com.legopitstop.TextEditor')
        self.default_config = {'WordWrap': True,'StatusBar': True, 'Keybinds': {'Open': 'Control-o','Save': 'Control-s','SaveAs': 'Control-S','Print': 'Print','Search': 'Control-e','Find': 'Control-f','FindNext': 'F3','FindPrevious': 'Shift-F3','Replace': 'Control-h','GoTo': 'Control-g','TimeDate': 'F5','ZoomIn': 'Control-Plus','ZoomOut': 'Control-Minus','RestoreDefaultZoom': 'Control-0','Help':'Control-question'}}
        if self.user.exists('config.yml'):
            self._config = self.config('r')
        else:
            self._config = self.default_config
            self.config('w')
        
        self.geometry('620x377')
        self.saved=True
        self.path=None
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.minsize(620,377)

        # Config
        if title!=None: self.title(title)
        if iconbitmap!=None: self.iconbitmap(iconbitmap)
        
        # Varables
        self.WORD_WRAP=BooleanVar()
        self.WORD_WRAP.set(self._config['WordWrap'])
        self.STATUS_BAR=BooleanVar()
        self.STATUS_BAR.set(self._config['StatusBar'])

        # Widgets
        self.textarea = ScrolledText(self,bd=0,width=69,height=23,undo=True)
        self.textarea.grid(row=0,column=0,sticky='nesw')

        xscroll = Scrollbar(self,orient=HORIZONTAL, command=self.textarea.xview)
        xscroll.grid(row=1, column=0, sticky='nsew')
        self.textarea['xscrollcommand'] = xscroll.set

        # Binds
        self.protocol('WM_DELETE_WINDOW',self.exit)
        self.bind(self.getBind('Find'), lambda e: self._window('find'))
        self.bind(self.getBind('FindNext'), lambda e: self._context('find_next'))
        self.bind(self.getBind('FindPrevious'), lambda e: self._context('find_previous'))
        self.bind(self.getBind('GoTo'), lambda e: self._window('go_to'))
        self.bind(self.getBind('Open'), lambda e: self._context('open'))
        self.bind(self.getBind('Print'), lambda e: self._context('print'))
        self.bind(self.getBind('Replace'), lambda e: self._window('replace'))
        self.bind(self.getBind('RestoreDefaultZoom'), lambda e: self._context('restore_zoom'))
        self.bind(self.getBind('Save'), lambda e: self._context('save'))
        self.bind(self.getBind('SaveAs'), lambda e: self._context('save_as'))
        self.bind(self.getBind('Search'), lambda e: self._context('search'))
        self.bind(self.getBind('TimeDate'), lambda e: self._context('time_date'))
        self.bind(self.getBind('ZoomIn'), lambda e: self._context('zoom_in'))
        self.bind(self.getBind('ZoomOut'), lambda e: self._context('zoom_out'))
        self.bind(self.getBind('Help'), lambda e: self._window('help'))

        # self.bind('<Key>', lambda e: print(e))


        # ContextMenu
        context=ContextMenu(self.textarea)
        context.add_command(label='Undo',command=lambda: self._context('undo'))
        context.add_command(label='Redo',command=lambda: self._context('redo'))
        context.add_separator()
        context.add_command(label='Cut',command=lambda: self._context('cut'))
        context.add_command(label='Copy',command=lambda: self._context('copy'))
        context.add_command(label='Paste',command=lambda: self._context('paste'))
        context.add_command(label='Delete',command=lambda: self._context('delete'))
        context.add_separator()
        context.add_command(label='Select All',command=lambda: self._context('select_all'))
        context.add_separator()
        context.add_command(label='Search Internet...',command=lambda: self._context('search'))

        # menu
        menu=Menu(self,tearoff=False)
        file=Menu(menu,tearoff=False)
        file.add_command(label='Open...',command=lambda: self._context('open'))
        file.add_command(label='Save',command=lambda: self._context('save'))
        file.add_command(label='Save As...',command=lambda: self._context('save_as'))
        file.add_separator()
        file.add_command(label='Page Setup...',command=lambda: self._context('page_setup'))
        file.add_command(label='Print...',command=lambda: self._context('print'))
        file.add_separator()
        file.add_command(label='Exit',command=self.exit)
        
        edit=Menu(menu,tearoff=False)
        edit.add_command(label='Undo',command=lambda: self._context('undo'))
        edit.add_command(label='Redo',command=lambda: self._context('redo'))
        edit.add_separator()
        edit.add_command(label='Cut',command=lambda: self._context('cut'))
        edit.add_command(label='Copy',command=lambda: self._context('copy'))
        edit.add_command(label='Paste',command=lambda: self._context('paste'))
        edit.add_command(label='Delete',command=lambda: self._context('delete'))
        edit.add_separator()
        edit.add_command(label='Search Internet...',command=lambda: self._context('search'))
        edit.add_command(label='Find...',command=lambda: self._window('find'))
        edit.add_command(label='Find Next',command=lambda: self._context('find_next'))
        edit.add_command(label='Find Previous',command=lambda: self._context('find_previous'))
        edit.add_command(label='Replace...',command=lambda: self._window('replace'))
        edit.add_command(label='Go To...',command=lambda: self._window('go_to'))
        edit.add_separator()
        edit.add_command(label='Select All',command=lambda: self._context('select_all'))
        edit.add_command(label='Time/Date',command=lambda: self._context('time_date'))

        format=Menu(menu,tearoff=False)
        format.add_checkbutton(label='Word Wrap',offvalue=False,onvalue=True,variable=self.WORD_WRAP,command=self.update)
        format.add_command(label='Font...',command=lambda: self._window('font'))

        view=Menu(menu,tearoff=False)
        zoom=Menu(view,tearoff=False)
        zoom.add_command(label='Zoom In',command=lambda: self._context('zoom_in'))
        zoom.add_command(label='Zoom Out',command=lambda: self._context('zoom_out'))
        zoom.add_command(label='Restore Default Zoom',command=lambda: self._context('restore_zoom'))
        view.add_cascade(label='Zoom',menu=zoom)
        view.add_checkbutton(label='Status bar',offvalue=False,onvalue=True,variable=self.STATUS_BAR,command=self.update)

        help=Menu(menu,tearoff=False)
        help.add_command(label='Keybinds',command=lambda: self._window('keybinds'))
        help.add_command(label='About',command=lambda: self._window('about'))

        menu.add_cascade(label='File',menu=file)
        menu.add_cascade(label='Edit',menu=edit)
        menu.add_cascade(label='Format',menu=format)
        menu.add_cascade(label='View',menu=view)
        menu.add_cascade(label='Help',menu=help)
        self.configure(menu=menu)

        # UPDATE
        self.update()

    def getBind(self,id):
        return '<'+self._config['Keybinds'][id]+'>'

    def _context(self,id):
        if id=='open':
            file = filedialog.askopenfilename(defaultextension='.txt',parent=self)
            if file!='':
                self.open(file,'r')

        elif id=='save':
            if self.path!=None:
                self.open(self.path,'w')
            else:
                self._context('save_as')

        elif id=='save_as':
            file = filedialog.asksaveasfilename(confirmoverwrite=True,defaultextension='.txt',parent=self)
            if file!='':
                self.open(file,'w')

        elif id=='undo':
            self.textarea.edit_undo()

        elif id=='redo':
            self.textarea.edit_redo()

        elif id=='cut':
            self._context('copy')
            self._context('delete')

        elif id=='copy':
            focus = self.textarea.focus_get()
            if focus.winfo_class() == 'Text':
                try:
                    focus.clipboard_clear()
                    focus.clipboard_append(focus.selection_get())
                except: return False
            
        elif id=='paste':
            self._context('delete')
            focus:Text = self.textarea.focus_get()
            if focus.winfo_class() == 'Text':
                try: focus.insert(focus.index(INSERT), focus.clipboard_get())
                except: return False
            
        elif id=='delete':
            focus:Text = self.textarea.focus_get()
            if focus.winfo_class() == 'Text':
                try:
                    first =focus.index(SEL_FIRST)
                    last=focus.index(SEL_LAST)
                    focus.delete(first,last)
                except: return False

        elif id=='select_all':
            focus = self.textarea.focus_get()
            focus.tag_add(SEL, "1.0", END)
            focus.mark_set(INSERT, "1.0")
            focus.see(INSERT)
        
        elif id=='search':
            focus = self.textarea.focus_get()
            if focus.winfo_class() == 'Text':
                try:
                    webbrowser.open('https://www.google.com/search?q='+focus.selection_get().replace(' ','+'))
                except: return False
        else:
            print('Context',id)

    def _window(self,id):
        if id=='keybinds':
            binds = Toplevel(self)
            binds.title('Keybinds')

            # Function
            def show(e):
                print(e)

            
            def close():
                for k in self.key:
                    self._config['Keybinds'][k] = self.key[k]['var'].get()
                self.config('w')
                binds.destroy()

            def default(key):
                """set the deafult keybind"""
                if id=='Find': self.key[key].set('Control-f')
                elif id=='FindNext': self.key[key].set('F3')
                elif id=='FindPrevious': self.key[key].set('Shift-F3')
                elif id=='GoTo': self.key[key].set('Control-g')
                elif id=='Help': self.key[key].set('Control-question')
                elif id=='Open': self.key[key].set('Control-o')
                elif id=='Print': self.key[key].set('Print')
                elif id=='Replace': self.key[key].set('Control-h')
                elif id=='RestoreDefaultZoom': self.key[key].set('Control-0')
                elif id=='Save': self.key[key].set('Control-s')
                elif id=='SaveAs': self.key[key].set('Control-S')
                elif id=='Search': self.key[key].set('Control-e')
                elif id=='TimeDate': self.key[key].set('F5')
                elif id=='ZoomIn': self.key[key].set('Control-equal')
                elif id=='ZoomOut': self.key[key].set('Control-minus')
                else: print('Invalid id "%s"'%(id))

            # Widget
            keybinds =Frame(binds)
            keybinds.grid(row=0,column=0,padx=5,pady=5)

            self.key={}
            row=0
            for key in self._config['Keybinds']:
                self.key[key]={}
                self.key[key]['var'] = StringVar()
                val = self._config['Keybinds'][key]
                self.key[key]['var'].set(val)

                Label(keybinds,text=key).grid(row=row,column=0,sticky=E)

                self.key[key]['Entry'] = Entry(keybinds,textvariable=self.key[key]['var'],state=NORMAL)
                self.key[key]['Entry'].bind('KeyRelease',show)
                self.key[key]['Entry'].grid(row=row,column=1,sticky=W)

                self.key[key]['Button'] = Button(keybinds,text='reset',command=lambda: default(key),state=NORMAL)
                self.key[key]['Button'].grid(row=row,column=2,sticky=W)
                row+=1
            
            foot = Footer(binds)
            foot.add_button(text='Close',command=close)

        else:
            print('Window',id)


    def update(self):
        print('UPDATE')
        if self.STATUS_BAR.get():
            self.statusbar = Frame(self)

            pos = LabelFrame(self.statusbar)
            Label(pos,text='Ln 14, Col 9').grid(row=0,column=0,sticky=E)
            Frame(pos,width=100).grid(row=0,column=1)
            pos.grid(row=0,column=0)
            
            zoom = LabelFrame(self.statusbar)
            Label(zoom,text='100%').grid(row=0,column=0,sticky=E)
            zoom.grid(row=0,column=1)
            
            test = LabelFrame(self.statusbar)
            Label(test,text='UTF-8').grid(row=0,column=0,sticky=E)
            Frame(test,width=100).grid(row=0,column=1)
            test.grid(row=0,column=2)

            self.statusbar.grid(row=2,column=0,sticky=E)
        else:
            try: self.statusbar.destroy()
            except AttributeError: pass

        if self.WORD_WRAP.get():
            self.textarea['wrap'] = WORD

        else:
            self.textarea['wrap'] = NONE

    def exit(self):
        """Safely close the window"""
        self.config('w')
        self.destroy()
    
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
        self.textarea.insert(1.0,text)

    def delete(self):
        """Clears all text in textarea"""
        self.textarea.delete(1.0,END)

    def get(self):
        """Get text inside textarea"""
        return self.textarea.get(1.0,END)

    def config(self,mode='r'):
        """GET and save the config file."""
        if mode=='r':
            opn = self.user.open('config.yml','r')
            out = yaml.load(opn.read(),yaml.FullLoader)
            opn.close()
            return out
        elif mode=='w':
            wrt = self.user.open('config.yml','w')
            self._config['StatusBar'] = self.STATUS_BAR.get()
            self._config['WordWrap'] = self.WORD_WRAP.get()
            wrt.write(yaml.dump(self._config))
            wrt.close()
