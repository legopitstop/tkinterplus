from tkinterplus.experimental import emojichooser
import tkinter

root = tkinter.Tk()
root.withdraw()

emoji, name = emojichooser.askemoji(parent=root)
print(emoji, name)
