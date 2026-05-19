from typing import Self
from tkinter.font import Font, nametofont
from PIL import Image, ImageTk, ImageFile
import tkinter
import os

from .. import ROOT_PATH

__all__ = ["Picturebox"]


class Picturebox(tkinter.Canvas):
    def __init__(
        self,
        master: tkinter.Tk,
        image: ImageFile.ImageFile = None,
        width: int = None,
        height: int = None,
        text: str = None,
        fg: str = None,
        bg: str = None,
        font: Font = None,
        textvariable: tkinter.StringVar = None,
        **kw,
    ):
        """Construct a picture widget with the parent MASTER."""
        super().__init__(master, bd=0, highlightthickness=0)
        self.image = Image.open(
            os.path.join(ROOT_PATH, "assets", "icons", "missing.png")
        )
        self.width = None
        self.height = None
        self.text = None
        self.textvariable = tkinter.StringVar()
        self.fg = "black"
        self.bg = "#f0f0f0"
        self.font = Font(size=12)

        self.configure(
            image=image,
            width=width,
            height=height,
            text=text,
            fg=fg,
            bg=bg,
            textvariable=textvariable,
            font=font,
            **kw,
        )

    def _update_text(self, a=None, b=None, c=None) -> None:
        self.text = self.textvariable.get()
        self.itemconfigure("TEXT", text=self.text)

    def update(self) -> None:
        # Clear canvas to redraw
        self.delete("IMAGE")
        self.delete("TEXT")

        # Resize image
        width = self.width
        height = self.height
        if width == None:
            width = 1
        if height == None:
            height = 1
        self.imagetk = ImageTk.PhotoImage(
            self.image.resize((width, height), Image.NEAREST)
        )
        self.create_image(0, 0, image=self.imagetk, anchor=tkinter.NW, tag="IMAGE")
        self.tag_lower("IMAGE")

        if self.text != None:
            # Get the height of the font
            if self.font == "TkDefaultFont":
                font = nametofont(self.font)
                text_height = font.actual("size") * 2
            else:
                text_height = self.font.cget("size") * 2

            self.create_text(
                width / 2,
                height + text_height - 3,
                text=self.text,
                fill=self.fg,
                justify="center",
                anchor="s",
                font=self.font,
                tag="TEXT",
            )

        else:
            text_height = 0

        # Update canvas dimentions
        super().configure(width=width, height=height + text_height)

    def configure(self, **kw) -> Self:
        """Modify the widget"""
        if "image" in kw and kw["image"] != None:
            img = kw.pop("image")
            if isinstance(img, (ImageFile.ImageFile, Image.Image)):
                self.image = img
                if self.width == None:
                    self.width = self.image.width
                if self.height == None:
                    self.height = self.image.height
            elif isinstance(img, str):
                img = Image.open(img)
                self.configure(image=img)

            else:
                raise TypeError(
                    f"image must be ImageFile or str but got {img.__class__.__name__} instead."
                )

        if "text" in kw and kw["text"] != None:
            self.text = kw.pop("text")
        if "textvariable" in kw and kw["textvariable"] != None:
            self.textvariable = kw.pop("textvariable")
            self.text = self.textvariable.get()
            self.textvariable.trace_add("write", self._update_text)

        if "width" in kw and kw["width"] != None:
            self.width = kw.pop("width")
        if "height" in kw and kw["height"] != None:
            self.height = kw.pop("height")
        if "font" in kw and kw["font"] != None:
            self.font = kw.pop("font")

        if "bg" in kw and kw["bg"] != None:
            self.bg = kw.pop("bg")
            super().configure(bg=self.bg)
        if "fg" in kw and kw["fg"] != None:
            self.fg = kw.pop("fg")
            self.itemconfigure("TEXT", fill=self.fg)

        self.update()
        return self

    config = configure
