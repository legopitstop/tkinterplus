from tkinter import EW, Tk
from tkinterplus import ROOT, Audio
import os

root = Tk()
root.minsize(500,500)

#TODO make this use winsound if platform is Windows.
# Add Audio.seek()
# improve UI (Making the audio a vertical slider inside a tooltip / custom Menu)
widget = Audio(root)
widget.load(os.path.join(ROOT, 'assets', 'sounds', 'sound.ogg'))
widget.grid(row=0,column=0, sticky=EW)


root.grid_columnconfigure(0, weight=1)
root.mainloop()