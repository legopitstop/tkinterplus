from tkinterplus import ScrolledFrame
import tkinter


def main():
    root = tkinter.Tk()
    root.title("ScrolledFrame")
    root.minsize(500, 500)

    widget = ScrolledFrame(root)

    for i in range(100):
        tkinter.Label(widget, text="Label" + str(i)).pack()
    widget.pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
