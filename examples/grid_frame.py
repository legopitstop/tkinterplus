from tkinterplus import ScrolledGridFrame, GridFrame
import tkinter


def main():
    root = tkinter.Tk()
    root.geometry("400x400")

    # widget = ScrolledGridFrame(root, bg="red")
    widget = GridFrame(root, bg="red")

    for i in range(100):
        tkinter.Button(widget, text="Button " + str(i), width=10, height=0)
    widget.pack(expand=1, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
