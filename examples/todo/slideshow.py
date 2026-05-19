from tkinterplus.experimental import Slideshow
from tkinterplus import Picturebox
from PIL import Image
import tkinter
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

root = tkinter.Tk()
root.title("Slideshow")
root.minsize(500, 500)

images = [
    Image.open(os.path.join(LOCAL, "tests", "assets", "images", "barrel_bottom.png")),
    Image.open(os.path.join(LOCAL, "tests", "assets", "images", "barrel_side.png")),
    Image.open(os.path.join(LOCAL, "tests", "assets", "images", "barrel_top_open.png")),
    Image.open(os.path.join(LOCAL, "tests", "assets", "images", "barrel_top.png")),
]

widget = Slideshow(
    root, images=images, width=200, height=200, buttons=True, state="disabled"
)
widget.pack()

# widget1 = Picture(root, image=images[0], width=200, height=200, text='My Picture', bg='black', fg='white')
# widget1.pack()

root.mainloop()
