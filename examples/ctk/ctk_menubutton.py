from tkinterplus.ctk import CTkMenubutton, CTkMenu
import customtkinter


def main():
    root = customtkinter.CTk()
    root.title("CTkTreeView")
    root.minsize(400, 400)

    def callback():
        print("callback")

    widget = CTkMenubutton(root)
    menu = CTkMenu(root)
    menu.add_command("command1", command=callback)
    menu.add_command("command2", command=callback)
    menu.add_command("command3", command=callback)
    widget.configure(menu)
    widget.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
