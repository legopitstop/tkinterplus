from tkinter import *
from tkinterplus.experimental import CanvasPlus
from tkinterplus import Modal

root = Tk()
root.title('ModalCanvas')
root.minsize(500,500)

canvas = CanvasPlus(root)
canvas.pack(expand=1, fill=BOTH)

# widget = Label(canvas, text='worked')
widget = Modal(canvas)
Label(widget, text='Worked').pack()

canvas.create_window(0,0, window=widget, anchor='nw')

root.mainloop()