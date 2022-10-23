from tkinter import Tk, Label
from tkinterplus import Footer

root = Tk()
root.minsize(100,100)
root.configure(bg='white')

Label(root, text='Hello World', bg='white').grid(row=0,column=0)

def ok():
    print('OK')
    root.destroy()

widget = Footer(root)
widget.add_button(text='OK', command=ok)
widget.add_button(text='Cancel', command=root.destroy)

root.mainloop()