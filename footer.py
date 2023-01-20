from tkinter import *
from tkinter.ttk import Progressbar
from tkinterplus import Footer

root = Tk()
root.title('Footer')
root.minsize(200,100)
root.configure(bg='white')

Message(root, text='Hello World', bg='white').grid(row=0,column=0)
# Message(root, text='Hello World', bg='white').pack()
# Message(root, text='Hello World', bg='white').place(x=0, y=0)

def ok():
    print('OK')
    root.destroy()

widget = Footer(root)
widget.add_button(text='OK', command=ok)
widget.add_button(text='Cancel', command=root.destroy)

bar = Progressbar(widget, value=50)
bar.pack(expand=True, fill=BOTH)

root.mainloop()