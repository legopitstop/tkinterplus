from tkinter import *
from tkinterplus import Input

root = Tk()
root.title('Input')
root.minsize(500,500)

widget1 = Input(root, Input.COLOR)
widget2 = Input(root, Input.TEXT)
widget3 = Input(root, Input.PASSWORD)
widget4 = Input(root, Input.NUMBER)
widget5 = Input(root, Input.FILE)
widget6 = Input(root, Input.DIRECTORY)

widget1.pack()
widget2.pack()
widget3.pack()
widget4.pack()
widget5.pack()
widget6.pack()

root.mainloop()