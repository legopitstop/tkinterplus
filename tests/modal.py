from tkinter import Tk, Button, Label, messagebox
from tkinterplus import Modal, modalbox
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

root = Tk()
root.minsize(500,500)

widget = Modal(root)
Label(widget, text="This is a modal, It's like a Toplevel window but is in the master widget").pack(expand=True)

Button(root, text='Open Custom Modal', command=widget.show).pack()
title = 'title'
message = 'message'
Button(root, text='modalbox', command=lambda: modalbox.showinfo(title, message)).pack()
Button(root, text='messagebox', command=lambda: messagebox.showinfo(title, message)).pack()

root.mainloop()