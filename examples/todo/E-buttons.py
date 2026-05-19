from tkinterplus.experimental import EmojiButton, IconButton
import tkinter

root = tkinter.Tk()
root.title("BindButton")
root.minsize(500, 500)

BUTTON1 = tkinter.StringVar()
BUTTON2 = tkinter.StringVar()

button1 = EmojiButton(root, variable=BUTTON1, command=lambda: print(BUTTON1.get()))
button2 = IconButton(root, variable=BUTTON2, command=lambda: print(BUTTON2.get()))

BUTTON1.set("😀")
BUTTON2.set("")

button1.pack()
button2.pack()

root.mainloop()
