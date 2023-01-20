from tkinter import *
from tkinterplus import Form

root = Tk()
root.title('Form')
root.minsize(500,500)

def submit(data):
    print(data)
    root.destroy()

widget = Form(root)
widget.add_title('My Form')
widget.add_dropdown('Choose your age', '1-18', '19-UP')
widget.add_file('Choose a profile picture', [('Image', '*.png')])
widget.add_paragraph('paragraph')
widget.add_submit_button(submit)

widget.pack()

root.mainloop()