import tkinter
import _tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from enum import Enum


class ChildCommands(Enum):
    Common = 'Common'
    Canvas = 'Canvas'
    Listbox = 'Listbox'
    Text = 'Text'
    Notebook = 'Notebook'
    Treeview = 'Treeview'
    Menu = 'Menu'
    OptionMenu = 'OptionMenu'

class DeleteChildCommands(Enum):
    CanvasItem = 'CanvasItem'
    ListboxItem = 'ListboxItem'
    TextTag = 'TextTag'
    TreeviewItem = 'TreeviewItem'
    MenuItem = 'MenuItem'
    OptionMenuValue = 'OptionMenuValue'

class __RegisteredWidget():
    def __init__(self, cls, childcommand=None, deletecommand=None, deletechildcommand=None):
        if isinstance(cls, tuple):
            self.name = []
            for c in cls:
                self.name.append(str(c.__name__))
        else: self.name = str(cls.__name__)
        self.cls = cls

        self.childcommand = self._builtin_childcommand(childcommand)
        self.deletecommand =  deletecommand
        self.deletechildcommand = self._builtin_deletechildcommand(deletechildcommand)
    
    # ChildCommands
    def __none(self, w:tkinter.Widget):
        return None

    def __Canvas(self, w:tkinter.Canvas):
        for id in w.find_all():
            type = w.type(id)
            yield (type, id, False)

    def __Listbox(self, w:tkinter.Listbox):
        i = 0
        for name in w.get(0, tkinter.END):
            yield (name, i, False)
            i+=1
            
    def __Text(self, w:tkinter.Text):
        for name in w.tag_names():
            yield ('tag', name, False)

    def __Notebook(self, w:ttk.Notebook):
        for name in w.tabs():
            c = w.nametowidget(name)
            yield (c.__class__.__name__, c, True)

    def __Common(self, w:tkinter.Widget):
        for c in w.winfo_children():
            # if isinstance(c, tkinter.Widget): yield (c.__class__.__name__, c, True) # This should get removed to support each widget seperately
            if isinstance(c, DeveloperTools): pass # ignore self
            else: yield (c.__class__.__name__, c, True)

    def __Treeview(self, w:ttk.Treeview):
        for i in w.get_children():
            text = w.item(i, 'text')
            yield (text, i, False)

    def __Menu(self, w:tkinter.Menu):
        end = w.index(tkinter.END)
        if end!=None:
            for i in range(end+1):
                name = w.entrycget(i, 'label')
                yield (name, i, False)

        return None
        
    def __OptionMenu(self, w:tkinter.OptionMenu):
        m:tkinter.Menu = w['menu']
        end = m.index(tkinter.END)
        if end!=None:
            for i in range(end+1):
                name = m.entrycget(i, 'label')
                yield (name, i, False)
        return None

    # DeleteChildCommands
    def __CanvasItem(self, w:tkinter.Canvas, data:tuple):
        w.delete(data[2])

    def __TextTag(self,w:tkinter.Text, data:tuple):
        w.tag_delete(data[2])

    def __ListboxItem(self,w:tkinter.Listbox, data:tuple):
        w.delete(data[2])

    def __TreeviewItem(self, w:ttk.Treeview, data:tuple):
        w.delete(data[2])

    def __MenuItem(self, w:tkinter.Menu, data:tuple):
        w.delete(data[2])

    def __OptionMenuValue(self, w:ttk.OptionMenu, data:tuple):
        try:
            m = w['menu']
            m.delete(data[2])
        except _tkinter.TclError:
            messagebox.showwarning('Developer Tools', 'Failed to delete last item in OptionMenu! Must have at least one item in the menu!')

    def _builtin_childcommand(self, name):
        match name:
            case ChildCommands.Common: return self.__Common
            case ChildCommands.Canvas: return self.__Canvas
            case ChildCommands.Listbox: return self.__Listbox
            case ChildCommands.Text: return self.__Text
            case ChildCommands.Notebook: return self.__Notebook
            case ChildCommands.Treeview: return self.__Treeview
            case ChildCommands.Menu: return self.__Menu
            case ChildCommands.OptionMenu: return self.__OptionMenu
            case None: return self.__none
            case _: return name
            
    def _builtin_deletechildcommand(self, name):
        match name:
            case DeleteChildCommands.CanvasItem: return self.__CanvasItem
            case DeleteChildCommands.ListboxItem: return self.__ListboxItem
            case DeleteChildCommands.TextTag: return self.__TextTag
            case DeleteChildCommands.TreeviewItem: return self.__TreeviewItem
            case DeleteChildCommands.MenuItem: return self.__MenuItem
            case DeleteChildCommands.OptionMenuValue: return self.__OptionMenuValue
            case _:
                return name

    def match(self, name:str):
        if isinstance(self.name, list):
            for n in self.name:
                if n == name: return True
        elif name == self.name: return True
        return False

none = (
    tkinter.Button,
    tkinter.Checkbutton,
    tkinter.Entry,
    tkinter.Label,
    tkinter.Menubutton,
    tkinter.Message,
    tkinter.Radiobutton,
    tkinter.Scale,
    tkinter.Scrollbar,
    tkinter.Spinbox,
    ttk.Button,
    ttk.Checkbutton,
    ttk.Entry,
    ttk.Combobox,
    ttk.Label,
    ttk.Menubutton,
    ttk.Progressbar,
    ttk.Radiobutton,
    ttk.Scale,
    ttk.Scrollbar,
    ttk.Separator,
    ttk.Sizegrip,
    ttk.Spinbox,
    ttk.LabeledScale
)
common = (
    tkinter.Tk,
    tkinter.Toplevel,
    tkinter.Frame,
    tkinter.LabelFrame,
    tkinter.PanedWindow,
    ttk.Frame,
    ttk.Labelframe,
    ttk.Panedwindow
)


widgets = [
    __RegisteredWidget(tkinter.Canvas, ChildCommands.Canvas, deletechildcommand=DeleteChildCommands.CanvasItem),
    __RegisteredWidget(tkinter.Listbox, ChildCommands.Listbox, deletechildcommand=DeleteChildCommands.ListboxItem),
    __RegisteredWidget(tkinter.Text, ChildCommands.Text, deletechildcommand=DeleteChildCommands.TextTag),
    __RegisteredWidget(tkinter.Menu, ChildCommands.Menu, deletechildcommand=DeleteChildCommands.MenuItem),
    __RegisteredWidget((tkinter.OptionMenu, ttk.OptionMenu), ChildCommands.OptionMenu, deletechildcommand=DeleteChildCommands.OptionMenuValue),
    
    __RegisteredWidget(ttk.Treeview, ChildCommands.Treeview, deletechildcommand=DeleteChildCommands.TreeviewItem),
    __RegisteredWidget(ttk.Notebook, ChildCommands.Notebook),
    
    __RegisteredWidget(none),
    __RegisteredWidget(common, ChildCommands.Common) # Common containers
]

def add_widget(cls, childcommand=None, deletecommand=None, deletechildcommand=None ):
    """
    Add a custom widget to the Developer Tools window

    Arguments
    ---
    `cls` - The widget class to match. Can optionally be a tuple of classes to match any. Example: tkinter.Frame or (tkinter.Tk, tkinter.Frame)

    `command` - The command to return the tree view data. Should return something like: [(name:str, cls, haschildren:bool)] if "haschildren" is true it will check for children in this widget
    """
    w = __RegisteredWidget(cls, childcommand, deletecommand, deletechildcommand)
    widgets.insert(0, w)
    return w

class Redirector(object):
    def __init__(self, widget, tag='stdout'):
        self.widget = widget
        self.tag = tag
    
    def write(self, str):
        self.widget.configure(state='normal')
        self.widget.insert('end', str, (self.tag))
        self.widget.configure(state='disabled')

# Crash: Tool > Console > EXIT > Tool (CRASH)
class DeveloperTools(tkinter.Toplevel):
    def __init__(self, master:tkinter.Tk=None):
        super().__init__(master)
        self.title('Developer Tools')
        self.attributes('-topmost', True, '-toolwindow', True)

        # Variable
        self.COMMAND = tkinter.StringVar()

        # TOP NAV
        self._topnav = ttk.Notebook(self)

        # Elements
        self._widgets = tkinter.Frame(self._topnav)
        self.widgets = ttk.Treeview(self._widgets, show='tree', columns=('one'))
        scroll = tkinter.Scrollbar(self._widgets, command=self.widgets.yview)
        self.widgets.configure(yscrollcommand=scroll.set)
        self.widgets.pack(side='left', expand=1, fill='both')
        scroll.pack(side='right', fill='y')

        self._widgets.pack(expand=1, fill=tkinter.BOTH)

        # Console
        self._console = tkinter.Frame(self._topnav)

        self.console = ScrolledText(self._console, state=tkinter.DISABLED)
        self.console.tag_configure('stderr', foreground='#b22222')
        # sys.stdout = Redirector(self.console, 'stdout')
        # sys.stderr = Redirector(self.console, 'stderr')
        self.console.grid(row=0, columnspan=2, column=0, sticky='nesw')
        tkinter.Label(self._console, text='> ').grid(row=1, column=0, sticky=tkinter.W)
        self.command = tkinter.Entry(self._console, textvariable=self.COMMAND)
        self.command.grid(row=1, column=1, sticky=tkinter.EW)

        self._console.grid_columnconfigure(1, weight=1)
        self._console.grid_rowconfigure(0, weight=1)
        self._console.pack(expand=1, fill=tkinter.BOTH)

        # Sources
        self._sources = tkinter.Frame(self._topnav)
        self._sources.pack(expand=1, fill=tkinter.BOTH)

        # Styles
        self._styles = tkinter.Frame(self._topnav)
        self._styles.pack(expand=1, fill=tkinter.BOTH)

        # Binds
        self._binds = tkinter.Frame(self._topnav)
        binds = ScrolledText(self._binds)
        for event in self.master.event_info(): binds.insert(tkinter.END, str(event)+'\n') # temp
        binds.configure(state=tkinter.DISABLED)
        binds.pack(expand=1, fill=tkinter.BOTH)
        self._binds.pack(expand=1, fill=tkinter.BOTH)

        # Add to notebook
        self._topnav.add(self._widgets, text='Widgets')
        self._topnav.add(self._console, text='Console')
        self._topnav.add(self._sources, text='Sources')
        self._topnav.add(self._styles, text='Styles')
        self._topnav.add(self._binds, text='Binds')
        self._topnav.pack(expand=1, fill=tkinter.BOTH)

        # Binds
        # self.widgets.bind('<Button-3>', lambda e: self.edit(self.widgets))
        self.widgets.bind('<Button-3>', lambda e: self.context_menus(e, self.widgets))
        # self.widgets.bind('<<TreeviewSelect>>', lambda e: self.highlight(self.widgets)) # HOVER
        self.widgets.bind('<Delete>', lambda e: self.destroy_widget())
        self.widgets.bind('<Control-d>', lambda e: self.deselect())

        self.command.bind('<Return>', lambda e: print(self.COMMAND.get()))

        self.update_widget_list()
        self.bind_all('<Map>', self.refresh)
        self.bind_all('<Unmap>', self.refresh)

    def refresh(self, e:tkinter.Event=None):
        """Update the Developer Tools Window"""
        self.update_widget_list()

    def destroy(self):
        self.unbind_all('<Map>')
        self.unbind_all('<Unmap>')
        super().destroy()

    def update_widget_list(self):
        """Refresh the widget list"""
        # TODO: Should save all selected/open items so when refreshed it can reselect/open those items
        for i in self.widgets.get_children(): self.widgets.delete(i)
        children = self.get_children(self.master)
        self._create_widgets(self.widgets, children)

    def get_children(self, master:tkinter.Widget):
        """Returns all children widgets from the root window"""
        # (type, name, widget, children)
        out = []

        w = self.find_registered(master)
        if w!=None:
            if w.childcommand!=None:
                children = w.childcommand(master)
                if children !=None:
                    for name, cls, children in list(children):
                        c = []
                        if children==True: c = self.get_children(cls)
                        out.append((name, cls, c))

        return out

    def _create_widgets(self, tree:ttk.Treeview, children, parent=''):
        for value, widget, childs in children:
            _parent = tree.insert(parent, index=tkinter.END, text=str(value), values=[widget])
            if len(childs)>=1: 
                self._create_widgets(tree, childs, _parent)

    def deselect(self, items:str=None):
        if items == None:
            for i in self.widgets.selection():
                self.widgets.selection_remove(i)
        self.widgets.selection_remove(items)

    def deselect_all(self):
        """Dselect all widgets"""
        for i in self.widgets.selection(): self.widgets.selection_remove(i)

    def get_selected(self, multiple:bool=False):
        """Get Selected widget from tree (parent, name, cls)"""
        ids = self.widgets.selection()
        if multiple:
            res = []
            for id in ids:
                text = self.widgets.item(id, 'text')
                values = self.widgets.item(id, 'values')
                parent = self.widgets.parent(id)
                p = None
                if parent!=None:
                    ptext = self.widgets.item(parent, 'text')
                    pvalues = self.widgets.item(parent, 'values')
                    p = (ptext, *pvalues)
                try: res.append((p, text, *values))
                except: pass
            return res

        else:
            if len(ids) >=1:
                text = self.widgets.item(ids[0], 'text')
                values = self.widgets.item(ids[0], 'values')
                p = None
                if parent!=None:
                    ptext = self.widgets.item(parent, 'text')
                    pvalues = self.widgets.item(parent, 'values')
                    p = (ptext, *pvalues)
                return (p, text, *values)

    def find_registered(self, widget:str):
        global widgets
        for w in widgets:
            if isinstance(widget, str):
                if w.match(widget): return w
            elif isinstance(w.cls, list):
                for ww in w.cls:
                    if isinstance(widget, ww): return w
            elif isinstance(widget, w.cls): return w
        return None

    def destroy_widget(self):
        """Remove a widget"""
        ws = self.get_selected(multiple=True)
        for _w in ws:
            r = self.find_registered(_w[1])
            if r!=None:
                if r.deletecommand==None:
                    q = self.master.nametowidget(_w[2])
                    q.destroy()
                else: r.deletecommand(_w)

            else:
                p = self.find_registered(_w[0][0])
                if p!=None:
                    if p.deletechildcommand!=None:
                        w = self.master.nametowidget(_w[0][1])
                        p.deletechildcommand(w, _w)
                    else: print(f'deletechildcommand not found! {_w}') # This line debug
                else: print(f'Widget not found! {_w}') # This line should be error
        self.update_widget_list()

    def context_menus(self, e:tkinter.Event, widget:tkinter.Widget):
        menu = tkinter.Menu(widget, tearoff=False)
        if isinstance(widget, ttk.Treeview):
            sel = self.get_selected()
            if sel!=None:
                menu.add_command(label='Edit', command=self.edit)
                menu.add_command(label='Delete', foreground='red', command=self.destroy_widget)
            else:
                menu.add_command(label='New')

        x = self.winfo_x() + widget.winfo_x()
        y = self.winfo_y() + widget.winfo_y()
        menu.tk_popup(e.x+x, e.y+y)
        menu.grab_release()

    def edit(self, widgets:ttk.Treeview):
        id = widgets.selection()[0]
        name = widgets.item(id, 'values')[0]
        try:
            widget = self.master.nametowidget(name)
            widget.configure(background='yellow')
        except KeyError: print('Failed!')

    def highlight(self, elements:ttk.Treeview):
        def flash(widget:tkinter.Widget):
            color = widget.cget('background')
            self.master.after(100, lambda: widget.configure(background='lightblue'))
            self.master.after(200, lambda: widget.configure(background=color))
            self.master.after(300, lambda: widget.configure(background='lightblue'))
            self.master.after(400, lambda: widget.configure(background=color))
        id = elements.selection()[0]
        name = elements.item(id, 'values')[0]
        try:
            widget = self.master.nametowidget(name)
            flash(widget)
        except KeyError: pass
