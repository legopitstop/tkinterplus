from tkinter import Tk, Button, StringVar, Entry
from tkinterplus import Picture, Tooltip
from PIL import Image
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

index = 0
def var_tip():
    global index
    try:
        index+=1
        var.set(values[index])
    except IndexError:
        index=0
        var.set(values[index])

root = Tk()
root.minsize(500,500)

lbl0 = Button(root, text='simple')
lbl0.pack(ipadx=10, ipady=10, padx=5, pady=5)

lbl1 = Button(root, text='variable', command=var_tip)
lbl1.pack(ipadx=10, ipady=10, padx=5, pady=5)

lbl2 = Button(root, text='static')
lbl2.pack(ipadx=10, ipady=10, padx=5, pady=5)

lbl3 = Button(root, text='custom')
lbl3.pack(ipadx=10, ipady=10, padx=5, pady=5)

Tooltip(lbl0, text='This is a simple tooltip')

values = [
    'This is a variable tooltip',
    'It can be changed!',
    'Allows you to easly update the tip!'
]

var = StringVar()
var.set(values[index])
Tooltip(lbl1, textvariable=var, borderwidth=0)

static_tip = Tooltip(lbl2, text='This tooltip will not follow the mouse!\nEnter tooltip text:', follow=False, anchor='sw', x=0, y=0)
Entry(static_tip, textvariable=var).pack()

custom_tip = Tooltip(lbl3, bg='blue',ipadx=5, ipady=5, borderwidth=4)
Picture(custom_tip, bg='blue', fg='white', image=Image.open(os.path.join(LOCAL, 'images', 'sample.png')), text='Hello World').pack()

root.mainloop()