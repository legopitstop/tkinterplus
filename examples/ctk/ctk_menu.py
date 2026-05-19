from tkinterplus.ctk import CTkMenu
import tkinter
import customtkinter


def main():
    root = customtkinter.CTk()
    root.title("CTkMenu")
    root.minsize(400, 400)

    def callback():
        print("callback")

    CHECK = tkinter.IntVar(value=True)
    RADIO = tkinter.StringVar(value="1")

    menu = CTkMenu(root)
    menu2 = CTkMenu(menu)
    menu2.add_command("command", command=callback)
    menu2.add_separator()
    menu2.add_checkbutton("checkbutton", onvalue=1, offvalue=0, variable=CHECK)
    menu2.add_separator()
    menu2.add_radiobutton("radiobutton1", value="1", variable=RADIO)
    menu2.add_radiobutton("radiobutton2", value="2", variable=RADIO)

    menu3 = CTkMenu(menu)
    menu3.add_cascade("cascade3", menu=menu2)

    menu.add_cascade("cascade1", menu=menu2)
    menu.add_cascade("cascade2", menu=menu3)

    root.configure(menu=menu)
    root.mainloop()


if __name__ == "__main__":
    main()
