from tkinterplus.ctk import CTkListbox
import customtkinter


def main():
    root = customtkinter.CTk()
    root.title("CTkListbox")
    root.minsize(400, 400)

    lst = CTkListbox(root)
    lst.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
