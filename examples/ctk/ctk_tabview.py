from customtkinter import CTkTabview, CTkButton
from tkinterplus.experimental import Tabview
import tkinter


def main():
    root = tkinter.Tk()
    root.title("Tabview")
    root.minsize(100, 100)

    ctk_tabs = CTkTabview(root)
    ctk_tabs.pack(expand=1, fill="x")

    ctk_tabs.tab()
    ctk_tabs.tab()

    ctk_tab1 = ctk_tabs.add("tab1")
    CTkButton(ctk_tab1, text="tab1").pack()
    ctk_tab2 = ctk_tabs.add("tab2")
    CTkButton(ctk_tab2, text="tab2").pack()

    tabs = Tabview(root)
    tabs.pack(expand=1, fill="x")

    tab1 = tabs.add("tab1")
    tkinter.Button(tab1, text="tab1").pack()

    tab2 = tabs.add("tab2")
    tkinter.Button(tab2, text="tab2").pack()

    root.configure(padx=10, pady=10)
    root.mainloop()


if __name__ == "__main__":
    main()
