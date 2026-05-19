from tkinterplus import FileButton, DirectoryButton, ColorButton, BindButton
import tkinter


def main():
    root = tkinter.Tk()
    root.title("Buttons")
    root.minsize(500, 500)

    BUTTON1 = tkinter.StringVar()
    BUTTON2 = tkinter.StringVar()
    BUTTON3 = tkinter.StringVar()
    BUTTON4 = tkinter.StringVar()

    button1 = FileButton(root, variable=BUTTON1, command=lambda: print(BUTTON1.get()))
    button2 = DirectoryButton(
        root, variable=BUTTON2, command=lambda: print(BUTTON2.get())
    )
    button3 = ColorButton(root, variable=BUTTON3, command=lambda: print(BUTTON3.get()))
    button4 = BindButton(
        root,
        variable=BUTTON4,
        command=lambda: print(BUTTON4.get()),
        bindcommand=lambda e: print(e),
        bind_all=True,
    )

    BUTTON1.set("C:/Users/1589l/Downloads/copper armor/copper_boots.png")
    BUTTON2.set("C:/Users/1589l/Downloads/copper armor")
    # BUTTON3.set("SystemButtonFace")
    BUTTON3.set("#000000")
    BUTTON4.set("<Control-s>")

    button1.pack()
    button2.pack()
    button3.pack()
    button4.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
