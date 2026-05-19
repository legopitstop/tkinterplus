from tkinterplus import ask_mime
import tkinter

root = tkinter.Tk()
root.title("Mime Picker")
root.minsize(500, 500)


def callback():
    print(ask_mime())


button = tkinter.Button(root, text="Ask Mime", command=callback)
button.pack()

root.mainloop()
