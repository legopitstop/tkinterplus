from tkinter import *
from tkinterplus import BindButton

root = Tk()
root.title('BindButton')
root.minsize(500,500)

BIND = StringVar()

def callback():
    print(BIND.get())

widget = BindButton(root, variable=BIND, command=callback, width=20)
widget.pack()

BIND.set('<Control-s>')

root.mainloop()