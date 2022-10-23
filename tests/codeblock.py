from tkinter import EW, Tk
from tkinterplus import CodeBlock

root = Tk()

widget = CodeBlock(root)
widget.insert(0.0, 'code')
widget.grid(row=0,column=0, sticky=EW)

root.grid_columnconfigure(0, weight=1)
root.mainloop()