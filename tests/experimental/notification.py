from tkinter import *
from tkinterplus.experimental import Notification

root = Tk()
root.title('Notification')
root.minsize(500,500)

widget = Notification(root, text='Hello World!')

Button(root, text='Show', command=lambda: widget.show()).pack()
Button(root, text='Hide', command=widget.hide).pack()

root.grid_columnconfigure(0, weight=1)
root.configure(padx=10, pady=10)
root.mainloop()