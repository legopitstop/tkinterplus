from tkinterplus.experimental import CodeX
import tkinter

root = tkinter.Tk()
root.title("Code")
root.minsize(500, 500)

widget = CodeX(root)
widget.pack(expand=1, fill="both")

root.mainloop()
