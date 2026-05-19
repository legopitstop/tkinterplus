from tkinterplus import Table
import tkinter

root = tkinter.Tk()
root.geometry("400x400")

widget = Table(root)
column1 = widget.header("header1")
column2 = widget.header("header2")
column3 = widget.header("header3")
widget.pack(expand=1, fill="both")

root.mainloop()
