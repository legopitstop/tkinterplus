from tkinterplus import ContextMenu
import tkinter

root = tkinter.Tk()
root.title("ContextMenu")
root.minsize(500, 500)

textarea = tkinter.Text(root)
textarea.pack(expand=1, fill="both")

listbox = tkinter.Listbox(root)
listbox.insert(0, "item 1")
listbox.insert(0, "item 2")
listbox.pack(expand=1, fill="both")


def show():
    pass


widget = ContextMenu(textarea, show)
widget.add_command(label="Cut")
widget.add_command(label="Copy")
widget.add_command(label="Paste")

widget2 = ContextMenu(listbox, show)
widget2.add_command(label="Cut")
widget2.add_command(label="Copy")
widget2.add_command(label="Paste")

root.mainloop()
