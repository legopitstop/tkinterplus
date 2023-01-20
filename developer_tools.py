from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import simpledialog
from tkinterplus.experimental import DeveloperTools, add_widget

# Add widgets to DeveloperTools
# add_widget(Treeview)

root = Tk()
root.title('Developer Tools')
root.minsize(500,500)

global win
win = None

def dev():
    global win
    win = DeveloperTools(root)

def test(e:Event): return e

root.bind('<Control-U>', lambda e: dev()) # Control-Shift-u
root.bind_all('<Control-s>', test) # Control-Shift-u

# Variables

VALUES = [
    'item1',
    'item2',
    'item3',
    'item4',
    'item5'
]

BUTTON = StringVar()
BUTTON.set('Button')
CHECK_BUTTON = StringVar()
CHECK_BUTTON.set('CheckButton')
ENTRY = StringVar()
ENTRY.set('Entry')
LABEL = StringVar()
LABEL.set('Label')
MENUBUTTON = StringVar()
MENUBUTTON.set('Menubutton')
MESSAGE = StringVar()
MESSAGE.set('Message')
SCALE = DoubleVar()
SCALE.set('Scale')
OPTION_MENU = StringVar()
OPTION_MENU.set('OptionMenu')
TEXT = StringVar()
TEXT.set('Text')
SPINBOX = StringVar()
SPINBOX.set('Spinbox')
COMBOBOX = StringVar()
COMBOBOX.set('Spinbox')
PROGRESSBAR = IntVar()
PROGRESSBAR.set(50)

# Widgets
Button(root, text='Tools', command=dev).pack()

tk_menu= Menu(root, tearoff=False)
for v in VALUES: tk_menu.add_command(label=v)

root.configure(menu=tk_menu)

book = ttk.Notebook(root)

# tkinter.Button
# tkinter.Canvas
# tkinter.Checkbutton
# tkinter.Entry
# tkinter.Frame
# tkinter.Label
# tkinter.Listbox
# tkinter.Menu
# tkinter.Menubutton
# tkinter.Message
# tkinter.Radiobutton
# tkinter.Scale
# tkinter.Scrollbar
# tkinter.Text
# tkinter.OptionMenu
# tkinter.LabelFrame
TK = Frame(book)
tk_button= Button(TK, textvariable=BUTTON)
tk_button.grid(row=0, column=0)

tk_canvas= Canvas(TK)
tk_canvas.create_line(0,0, 100, 100)
tk_canvas.create_line(0,100, 100, 0)
tk_canvas.grid(row=1, column=0)

tk_checkbutton= Checkbutton(TK, variable=CHECK_BUTTON, textvariable=CHECK_BUTTON)
tk_checkbutton.grid(row=2, column=0)

tk_entry= Entry(TK, textvariable=ENTRY)
tk_entry.grid(row=3, column=0)

tk_frame= Frame(TK, bg='red', width=25, height=25)
Label(tk_frame, text='Frame').pack()
tk_frame.grid(row=4, column=0)

tk_label= Label(TK, textvariable=LABEL)
tk_label.grid(row=0, column=1)

tk_listbox= Listbox(TK)
for v in VALUES: tk_listbox.insert(END, v)
tk_listbox.grid(row=1, column=1)


tk_menubutton= Menubutton(TK, textvariable=MENUBUTTON, menu=tk_menu)
tk_menubutton.grid(row=2, column=1)

tk_message= Message(TK, textvariable=MESSAGE)
tk_message.grid(row=3, column=1)

tk_radiobutton= Radiobutton(TK, variable=RADIOBUTTON, textvariable=RADIOBUTTON)
tk_radiobutton.grid(row=4, column=1)

tk_scale= Scale(TK, variable=SCALE)
tk_scale.grid(row=0, column=2)

tk_scrollbar= Scrollbar(TK)
tk_scrollbar.grid(row=1, column=2)

tk_text= Text(TK)
for v in VALUES: tk_text.insert(END, v+'\n', 'tag')
tk_text.tag_configure('tag', background='yellow')
tk_text.grid(row=2, column=2)

tk_optionmenu= OptionMenu(TK, OPTION_MENU, *VALUES)
tk_optionmenu.grid(row=3, column=2)

tk_labelframe= LabelFrame(TK, text='LabelFrame')
Label(tk_labelframe, text='LabelFrame').pack()
tk_labelframe.grid(row=4, column=2)

tk_spinbox= Spinbox(TK, textvariable=SPINBOX)
Label(tk_spinbox, text='LabelFrame').pack()
tk_spinbox.grid(row=0, column=3)

tk_paned_window= PanedWindow(TK)
Label(tk_paned_window, text='LabelFrame').pack()
tk_paned_window.grid(row=0, column=3)

TK.pack()


# ttk.Button
# ttk.Checkbutton
# ttk.Entry
# ttk.Combobox
# ttk.Frame
# ttk.Label
# ttk.LabelFrame
# ttk.Menubutton
# ttk.Notebook
# ttk.PanedWindow
# ttk.Progressbar
# ttk.Radiobutton
# ttk.Scale
# ttk.Scrollbar
# ttk.Separator
# ttk.Sizegrip
# ttk.Spinbox
# ttk.Treeview
# ttk.LabeledScale
# ttk.OptionMenu
TTK = Frame(book)

ttk_button = ttk.Button(TTK, textvariable=BUTTON)
ttk_button.grid(row=0, column=0)

ttk_checkbutton = ttk.Checkbutton(TTK, variable=CHECKBUTTON, textvariable=CHECKBUTTON)
ttk_checkbutton.grid(row=1, column=0)

ttk_entry = ttk.Entry(TTK, textvariable=ENTRY)
ttk_entry.grid(row=2, column=0)

ttk_combobox = ttk.Combobox(TTK, textvariable=COMBOBOX)
ttk_combobox.grid(row=3, column=0)

ttk_frame = ttk.Frame(TTK)
Label(ttk_frame, text='LabelFrame').pack()
ttk_frame.grid(row=4, column=0)

ttk_label = ttk.Label(TTK, textvariable=LABEL)
ttk_label.grid(row=0, column=1)

ttk_menubutton = ttk.Menubutton(TTK, textvariable=MENUBUTTON, menu=tk_menu)
ttk_menubutton.grid(row=1, column=1)

ttk_progressbar = ttk.Progressbar(TTK, variable=PROGRESSBAR)
ttk_progressbar.grid(row=2, column=1)

ttk_radiobutton = ttk.Radiobutton(TTK, variable=RADIOBUTTON, textvariable=RADIOBUTTON)
ttk_radiobutton.grid(row=3, column=1)

ttk_scale = ttk.Scale(TTK, variable=SCALE)
ttk_scale.grid(row=4, column=1)

ttk_scrollbar = ttk.Scrollbar(TTK)
ttk_scrollbar.grid(row=0, column=2)

ttk_seperator = ttk.Separator(TTK)
ttk_seperator.grid(row=1, column=2)

ttk_sizegrip = ttk.Sizegrip(TTK)
ttk_sizegrip.grid(row=2, column=2)

ttk_spinbox = ttk.Spinbox(TTK, textvariable=SPINBOX)
ttk_spinbox.grid(row=3, column=2)

ttk_treeview = ttk.Treeview(TTK)
for i in VALUES: ttk_treeview.insert('', END, text=i)
ttk_treeview.grid(row=4, column=2)

ttk_labeled_scale = ttk.LabeledScale(TTK, variable=SCALE)
ttk_labeled_scale.grid(row=0, column=3)

ttk_option_menu = ttk.OptionMenu(TTK, OPTION_MENU, *VALUES)
ttk_option_menu.grid(row=1, column=3)

ttk_option_menu = ttk.Labelframe(TTK)
ttk_option_menu.grid(row=2, column=3)

ttk_option_menu = ttk.Panedwindow(TTK)
Label(ttk_option_menu, text='LabelFrame').pack()
ttk_option_menu.grid(row=3, column=3)

TTK.pack()

# tix.Balloon
# tix.ButtonBox
# tix.ComboBox
# tix.Control
# tix.DirList
# tix.DirTree
# tix.DirSelectBox
# tix.DirSelectDialog
# tix.ExFileSelectDialog
# tix.FileSelectBox
# tix.FileSelectDialog
# tix.FileEntry
# tix.HList
# tix.InputOnly
# tix.LabelEntry
# tix.LabelFrame
# tix.ListNoteBook
# tix.Meter
# tix.NoteBook
# tix.NoteBookFrame
# tix.OptionMenu
# tix.PanedWindow
# tix.PopupMenu
# tix.ResizeHandle
# tix.ScrolledHList
# tix.ScrolledListBox
# tix.ScrolledText
# tix.ScrolledTList
# tix.ScrolledWindow
# tix.Select
# tix.Shell
# tix.DialogShell
# tix.StdButtonBox
# tix.TList
# tix.Tree
# tix.CheckList
TIX = Frame(book)
TIX.pack()

# tkinter.Toplevel
# simpledialog.askinteger
# simpledialog.askfloat
# simpledialog.askstring
# scrolledtext.ScrolledText
def toplevel():
    toplevel = Toplevel(root)
    Button(toplevel, text='something').pack()

MISC = Frame(book)
Button(MISC, text='toplevel', command=toplevel).grid(row=0, column=0)
Button(MISC, text='askinteger', command=lambda: simpledialog.askinteger('title', 'prompt', parent=root)).grid(row=1, column=0)
Button(MISC, text='askfloat', command=lambda: simpledialog.askfloat('title', 'prompt', parent=root)).grid(row=2, column=0)
Button(MISC, text='askstring', command=lambda: simpledialog.askstring('title', 'prompt', parent=root)).grid(row=3, column=0)

ScrolledText = scrolledtext.ScrolledText(MISC)
ScrolledText.tag_configure('name', background='yellow')
ScrolledText.insert(END, 'Something', 'name')
ScrolledText.grid(row=4, column=0)
MISC.pack()

book.add(TK, text='tk')
book.add(TTK, text='ttk')
book.add(TIX, text='tix')
book.add(MISC, text='misc')

book.pack(expand=1, fill='both')

root.mainloop()
