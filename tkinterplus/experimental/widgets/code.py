import tkinter


class CodeX(tkinter.Frame):
    def __init__(self, master, bg="white", fg="black"):
        super().__init__(master)
        self.lnnum = tkinter.Frame(self, bg=bg)
        for i in range(10):
            tkinter.Label(
                self.lnnum, text=i + 1, bg=bg, fg=fg, anchor="e", justify="right"
            ).grid(row=i, column=0, sticky="ew")

        self.lnnum.grid(row=0, column=0, sticky="ns")

        self.text = tkinter.Text(self, fg=fg, bg=bg, borderwidth=0)
        self.text.grid(row=0, column=1, sticky="nesw")
        self.text.insert(0.0, open(__file__).read())

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.update()

    def update(self) -> None:
        super().update()
        res = self.text.get(0.0, "end")
