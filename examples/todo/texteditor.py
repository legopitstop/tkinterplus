from tkinterplus import TextEditor
import tkinter

root = tkinter.Tk()
root.geometry("400x400")


def callback():
    widget = TextEditor(root)
    widget.insert(0.0, "Worked")


tkinter.Button(root, text="Open", command=callback).pack()

root.mainloop()
