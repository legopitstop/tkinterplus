from customtkinter import CTkButton, CTkImage

from .. import MaterialIcon

__all__ = ["CTkIconButton"]


# TODO: Make icons less blurry.
class CTkIconButton(CTkButton):
    def __init__(
        self,
        master,
        icon: str = None,
        text: str = None,
        size: tuple[int] | int = None,
        **kw,
    ):
        super().__init__(
            master,
            width=0,
            fg_color="transparent",
            text_color_disabled="red",
            hover_color="#2d2d2d",
        )
        self.configure(icon=icon, text=text, size=size, **kw)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if value is None:
            self.text = "CTkIconButton"
        else:
            self.text = str(value)

    @property
    def icon(self) -> str:
        return self._icon

    @icon.setter
    def icon(self, value: str):
        if value is None:
            self._icon = "home"
        else:
            self._icon = str(value)

        self.dark_icon = MaterialIcon(
            self.icon, style="outlined", size=self.size, color="black"
        )
        self.dark_icon.bind("<<updated>>", self._update_icon)

        self.light_icon = MaterialIcon(
            self.icon, style="outlined", size=self.size, color="white"
        )
        self.light_icon.bind("<<updated>>", self._update_icon)

        self._update_icon()

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: int | tuple | list):
        if value is None:
            self._size = (40, 40)
        elif isinstance(value, int):
            self._size = (value, value)
        elif isinstance(value, tuple):
            if len(value) == 2:
                self._size = (int(value[0]), int(value[1]))
            else:
                raise IndexError(f"Expected 2 values but got {len(value)} instead.")
        elif isinstance(value, list):
            if len(value) == 2:
                self._size = (int(value[0]), int(value[1]))
            else:
                raise IndexError(f"Expected 2 values but got {len(value)} instead.")
        else:
            raise TypeError(
                f"Expected int, tuple or list but got {value.__class__.__name__} instead."
            )

    def _update_icon(self, e=None):
        self.img = CTkImage(
            self.dark_icon.get("imagefile"),
            self.light_icon.get("imagefile"),
            size=self.size,
        )
        super().configure(image=self.img)

    def configure(self, **kw):
        for n in ["image", "compound"]:  # remove
            if n in kw:
                kw.pop(n)
        if "size" in kw:
            self.size = kw.pop("size")
        if "icon" in kw and kw["icon"] is not None:
            self.icon = kw.pop("icon")
        super().configure(compound="top", **kw)
        return self
