from tkinter import *
from tkinterplus.experimental import Paragraph
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

root = Tk()
root.title('Paragraph')
root.minsize(500,500)

widget = Paragraph(root, )
widget.pack()

root.mainloop()