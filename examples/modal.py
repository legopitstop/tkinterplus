from tkinter import messagebox, simpledialog
from tkinterplus import Modal, modalbox, simplemodal
import tkinter
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))


def main():
    root = tkinter.Tk()
    root.title("Modal")
    root.minsize(500, 500)

    title = "title"
    message = "message"
    custom_message = (
        "This is a modal, It's like a Toplevel window but is in the master widget"
    )

    widget = Modal(root, padx=5, pady=5)
    tkinter.Label(widget, text=custom_message).pack(expand=True)

    def toplevel():
        level = tkinter.Toplevel(root, padx=5, pady=5)
        tkinter.Label(level, text=custom_message).pack(expand=True)

    class CustomModalDialog(simplemodal.Dialog):
        def __init__(self, parent=None, title=None):
            super().__init__(parent, title)

        def body(self, master):
            tkinter.Label(master, text="CustomModalDialog").pack()

    class CustomDialog(simpledialog.Dialog):
        def __init__(self, parent=None, title=None):
            super().__init__(parent, title)

        def body(self, master):
            tkinter.Label(master, text="CustomDialog").pack()

    modals = tkinter.LabelFrame(root, text="Modals")
    tkinter.Button(root, text="Open Custom Modal", command=widget.show).pack()
    tkinter.Button(
        root, text="modalbox", command=lambda: modalbox.showinfo(title, message)
    ).pack()
    modals.pack(pady=5)

    modals = tkinter.LabelFrame(root, text="Tkinter")
    tkinter.Button(root, text="toplevel", command=toplevel).pack()
    tkinter.Button(
        root, text="messagebox", command=lambda: messagebox.showinfo(title, message)
    ).pack()
    modals.pack(pady=5)

    root.mainloop()

    root.mainloop()


if __name__ == "__main__":
    main()
