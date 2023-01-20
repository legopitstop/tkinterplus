from tkinter import *
from tkinterplus import Modal, modalbox
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

root = Tk()
root.title('Modal')
root.minsize(500,500)

title = 'title'
message = 'message'
custom_message = "This is a modal, It's like a Toplevel window but is in the master widget"

widget = Modal(root, padx=5, pady=5)
Label(widget, text=custom_message).pack(expand=True)

def toplevel():
    level = Toplevel(root, padx=5, pady=5)
    Label(level, text=custom_message).pack(expand=True)


modals = LabelFrame(root, text='Modals')
Button(root, text='Open Custom Modal', command=widget.show).pack()
Button(root, text='modalbox', command=lambda: modalbox.showinfo(title, message)).pack()
modals.pack(pady=5)

modals = LabelFrame(root, text='Tkinter')
Button(root, text='toplevel', command=toplevel).pack()
Button(root, text='messagebox', command=lambda: messagebox.showinfo(title, message)).pack()
modals.pack(pady=5)



root.mainloop()