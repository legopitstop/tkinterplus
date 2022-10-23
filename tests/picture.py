from tkinter import Tk
from tkinterplus import Picture
from PIL import Image
import os
LOCAL = os.path.dirname(os.path.realpath(__file__))

root = Tk()
root.minsize(256,256)

img = Image.open(os.path.join(LOCAL, 'assets', 'sample.png'))
widget = Picture(root, image=img, bg='gray', text='Hello World', width=256, height=256)
widget.pack()

root.mainloop()