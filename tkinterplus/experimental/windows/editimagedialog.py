import tkinter
from tkinter.simpledialog import Dialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

__all__ = ["askEditImage"]


class _QueryEditImage(Dialog):
    def __init__(
        self, parent, title=None, file: str = None, width: int = 200, height: int = 200
    ):
        self.width = width
        self.height = height
        filetypes = [("Image", ".png")]
        self.file = file
        self._x = self.width / 2
        self._y = self.height / 2
        if file is None:
            self.file = askopenfilename(parent=parent, title=title, filetypes=filetypes)
        super().__init__(parent, title)
        super().resizable(False, False)

    def _update(self, e: tkinter.IntVar):
        scale = self.SCALE.get() / 100
        x = round(self.width * scale)
        y = round(self.height * scale)
        if x > 0 and y > 0:
            temp = self.src.copy().resize((x, y), Image.NEAREST)
            self._PhotoImage = ImageTk.PhotoImage(temp)
            self.preview.itemconfigure("PREVIEW", image=self._PhotoImage)

    def _pan(self, e: tkinter.Event):
        x0, y0 = self.preview.coords("PREVIEW")
        x = x0 + e.x - self._x
        y = y0 + e.y - self._y
        self.preview.moveto("PREVIEW", x, y)

    def body(self, master: tkinter.Toplevel):
        self.SCALE = tkinter.IntVar()
        self.SCALE.set(100)
        self.src = (
            Image.open(self.file)
            .convert("RGBA")
            .resize((self.width, self.height), Image.NEAREST)
        )
        self._PhotoImage = ImageTk.PhotoImage(self.src)
        canvas_w = round(self.width)
        canvas_h = round(self.height)
        self.preview = tkinter.Canvas(
            master, width=canvas_w, height=canvas_h
        )  # Use canvas instead
        self.preview.create_image(
            round(canvas_w / 2),
            round(canvas_h / 2),
            image=self._PhotoImage,
            tags=["PREVIEW"],
        )
        self.preview.create_line(2, 2, 2, canvas_h)
        self.preview.create_line(canvas_w, 2, canvas_w, canvas_h)
        self.preview.create_line(2, 2, canvas_w, 2)
        self.preview.create_line(2, canvas_h, canvas_w, canvas_h)
        self.preview.bind("<B1-Motion>", self._pan)
        self.preview.pack()
        tkinter.Scale(
            master,
            variable=self.SCALE,
            from_=50,
            to=150,
            showvalue=False,
            orient="horizontal",
            command=self._update,
        ).pack(expand=1, fill="x")

    def buttonbox(self):
        box = tkinter.Frame(self)

        w = tkinter.Button(
            box, text="Cancel", width=10, command=self.cancel, default=tkinter.ACTIVE
        )
        w.pack(side=tkinter.LEFT, padx=5, pady=5)
        w = tkinter.Button(box, text="Apply", width=10, command=self.ok)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def getresult(self):
        return "something"


def askeditimage(parent, title=None):
    return _QueryEditImage(parent, title)
