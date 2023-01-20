from tkinter import *
from tkinterplus.experimental import Audio
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

root = Tk()
root.title('Audio')
root.minsize(500,500)

#TODO make this use winsound if platform is Windows.
widget = Audio(root)
widget.open(os.path.join(LOCAL, 'examples', 'sound.ogg'))
widget.grid(row=0,column=0, sticky=EW)

# 3:30
root.grid_columnconfigure(0, weight=1)
root.configure(padx=10, pady=10)
root.mainloop()