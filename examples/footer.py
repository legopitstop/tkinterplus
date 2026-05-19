from tkinter.ttk import Progressbar
from tkinterplus import Footer
import tkinter


def main():
    root = tkinter.Tk()
    root.title("Footer")
    root.minsize(200, 100)
    root.configure(bg="white")

    tkinter.Message(root, text="Hello World", bg="white").grid(row=0, column=0)
    # Message(root, text='Hello World', bg='white').pack()
    # Message(root, text='Hello World', bg='white').place(x=0, y=0)

    def ok():
        print("OK")
        root.destroy()

    widget = Footer(root)
    widget.add_button(text="OK", command=ok)
    widget.add_button(text="Cancel", command=root.destroy)

    bar = Progressbar(widget, value=50)
    bar.pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
