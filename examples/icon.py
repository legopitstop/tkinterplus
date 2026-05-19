from tkinterplus import MaterialIcon
import tkinter


def main():
    root = tkinter.Tk()
    root.title("FormatText")
    root.minsize(500, 500)

    icon1 = MaterialIcon("search")
    icon2 = MaterialIcon("home")
    icon3 = MaterialIcon("account_circle")
    icon4 = MaterialIcon("settings")
    icon5 = MaterialIcon("done")
    icon6 = MaterialIcon("info")

    label1 = tkinter.Label(root, image=icon1, text="icon1", compound="left")
    label2 = tkinter.Label(root, image=icon2, text="icon2", compound="left")
    label3 = tkinter.Label(root, image=icon3, text="icon3", compound="left")
    label4 = tkinter.Label(root, image=icon4, text="icon4", compound="left")
    label5 = tkinter.Label(root, image=icon5, text="icon5", compound="left")
    label6 = tkinter.Label(root, image=icon6, text="icon6", compound="left")

    icon1.bind_widget(label1)
    icon2.bind_widget(label2)
    icon3.bind_widget(label3)
    icon4.bind_widget(label4)
    icon5.bind_widget(label5)
    icon6.bind_widget(label6)

    label1.pack()
    label2.pack()
    label3.pack()
    label4.pack()
    label5.pack()
    label6.pack()

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()


if __name__ == "__main__":
    main()
