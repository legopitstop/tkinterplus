from tkinter import *
from tkinterplus import TextEditor

root = Tk()
root.title('TextEditor')
root.minsize(100,100)

def texteditor():
    win = TextEditor(root)
    # win.title('test')

Button(root, text='Open', command=texteditor).pack()
root.configure(padx=10, pady=10)
root.mainloop()
