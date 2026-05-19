from tkinterplus.ctk import CTkTreeView
import customtkinter


def main():

    root = customtkinter.CTk()
    root.title("CTkTreeView")
    root.minsize(400, 400)

    lst = CTkTreeView(root)
    lst.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
