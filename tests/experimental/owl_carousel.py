from tkinter import *
from tkinterplus.experimental import OwlCarousel
from PIL import Image
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

root = Tk()
root.title('OwlCarousel')
root.minsize(500,500)

widget = OwlCarousel(root, nav=False, items=3)
widget.add_image(Image.open(os.path.join(LOCAL, 'examples', 'cobblestone.png')))
widget.add_image(Image.open(os.path.join(LOCAL, 'examples', 'debug.png')))
widget.pack(expand=True, fill=BOTH)

root.mainloop()