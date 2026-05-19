from tkinterplus.experimental import Carousel
from PIL import Image
import tkinter
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

root = tkinter.Tk()
root.title("OwlCarousel")
root.minsize(500, 500)

widget = Carousel(root, nav=False, items=3)
widget.add_image(
    Image.open(os.path.join(LOCAL, "tests", "assets", "images", "cobblestone.png"))
)
widget.add_image(
    Image.open(os.path.join(LOCAL, "tests", "assets", "images", "debug.png"))
)
widget.pack(expand=True, fill="both")

root.mainloop()
