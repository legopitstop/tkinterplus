from tkinterplus.experimental import MarkupText

# from tkinterplus import FormatVar, StyleType
import tkinter

root = tkinter.Tk()
root.title("MarkupText")
root.minsize(500, 500)


def callback():
    print(widget.get(0.0, "end"))


widget = MarkupText(root)
widget.grid(row=0, column=0, sticky="nesw")

btn = tkinter.Button(root, text="Show", command=callback)
btn.grid(row=1, column=0, columnspan=2)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.mainloop()
