from tkinter import BOTH, Tk, Label
from tkinterplus import ScrolledFrame

root = Tk()
root.minsize(500,500)

widget = ScrolledFrame(root)

for i in range(100):
    Label(widget, text='Label'+str(i)).pack()
widget.pack(expand=True, fill=BOTH)

root.mainloop()