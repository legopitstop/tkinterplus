from tkinter import BOTH, Tk, Text
from tkinterplus import ContextMenu, ContextMenuType

root = Tk()
root.minsize(500,500)

textarea = Text(root)
textarea.pack(expand=True, fill=BOTH)

def show(): pass

widget = ContextMenu(textarea, show)
widget.add_command(label='Cut', type=ContextMenuType.CUT)
widget.add_command(label='Copy', type=ContextMenuType.COPY)
widget.add_command(label='Paste', type=ContextMenuType.PASTE)

root.mainloop()