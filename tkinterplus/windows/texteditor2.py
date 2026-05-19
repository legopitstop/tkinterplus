import tkinter


class TextEditor(tkinter.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.text = tkinter.Text(self, highlightthickness=0, borderwidth=0)
        self.text.pack(expand=1, fill="both")

    def insert(self, index: float, char: str) -> None:
        self.text.insert(index, char)

    def remove(self, index1, index2) -> None:
        self.text.delete(index1, index2)
