from typing import Self
from PIL import Image, ImageTk
import warnings
import tkinter
import os
import requests
import base64
import hashlib
import threading
import queue

from . import FILLED, OUTLINED, ROUNDED, SHARP, TWOTONE, ROOT_PATH, Asset

__all__ = ["IconError", "Icon", "Job", "init", "MaterialIcon"]


class IconError(Exception):
    pass


# TODO: use pydantic.BaseModel
class Icon:
    def __init__(self, file: str, color: str = None, size: tuple = None, **kw):
        """
        Load icon

        Arguments
        ---
        `file` - The path to the image to use.

        `color` - The color of the icon. Uses native color by defauit.

        `size` - The size of the icon. Uses native size by default.

        Methods
        ---
        update, configure, show, bind_widget, unbind_widget, bind, unbind, get
        """
        self._image = None
        self.children = []
        self._binds = {"updated": None}
        self._redraw = True

        self.configure(redraw=False, file=file, size=size, color=color, **kw)

    @property
    def file(self) -> str:
        return getattr(
            self, "_file", os.path.join(ROOT_PATH, "assets", "icons", "missing.png")
        )

    @file.setter
    def file(self, value: str):
        if value is None:
            self.file = os.path.join(ROOT_PATH, "assets", "icons", "missing.png")
        elif isinstance(value, Asset):
            self.file = os.path.join(ROOT_PATH, "assets", "icons", value._value_)
        else:
            setattr(self, "_file", str(value))

    @property
    def size(self) -> tuple:
        return getattr(self, "_size", (40, 40))

    @size.setter
    def size(self, value: int | tuple | list):
        if value is None:
            self.size = (40, 40)
        elif isinstance(value, int):
            self._size = (value, value)
        elif isinstance(value, tuple):
            if len(value) == 2:
                setattr(self, "_size", (int(value[0]), int(value[1])))
            else:
                raise IndexError(f"Expected 2 values but got {len(value)} instead.")
        elif isinstance(value, list):
            if len(value) == 2:
                self.size = (int(value[0]), int(value[1]))
            else:
                raise IndexError(f"Expected 2 values but got {len(value)} instead.")
        else:
            raise TypeError(
                f"Expected int, tuple or list but got {value.__class__.__name__} instead."
            )

    @property
    def color(self) -> str | None:
        return getattr(self, "_color", None)

    @color.setter
    def color(self, value: str):
        if value is None:
            setattr(self, "_color", None)
        else:
            setattr(self, "_color", str(value))

    def update(self) -> Self:
        """
        Update all children widgets that have been bound with Icon.bind_widget()
        """
        if self._image is None or self._photo is None or self._redraw == True:
            # Load from file
            self._image = (
                Image.open(self.file).convert("RGBA").resize(self.size, Image.BICUBIC)
            )
            # Apply color
            mask = self._image.copy()
            pixels = mask.load()  # create the pixel map
            for i in range(mask.size[0]):
                for j in range(mask.size[1]):
                    if pixels[i, j] != (0, 0, 0, 0):
                        pixels[i, j] = (0, 0, 0, 0)  # 128 Replace filled with black
                    else:
                        pixels[i, j] = (255, 255, 255)  # Replace transparent with white
            overlay = Image.new("RGBA", self._image.size, self.color)
            # self._image = Image.composite(self._image,overlay,mask).convert('RGBA')
            # Create imageTk
            self._photo = ImageTk.PhotoImage(self._image)

        for c in self.children:
            c.configure(image=self.get("imagetk"))
        if self._binds["updated"] is not None:
            self._binds["updated"](self)
        return self

    def configure(self, **kw) -> Self:
        if "file" in kw and kw["file"] != None:
            self.file = kw.pop("file")
        if "color" in kw and kw["color"] != None:
            self.color = kw.pop("color")
        if "size" in kw and kw["size"] != None:
            self.size = kw.pop("size")
        self.update()
        return self

    config = configure

    def show(self, title: str = None) -> Self:
        """
        Displays this image. This method is mainly intended for debugging purposes.
        """
        self.get("imagefile").show(title)
        return self

    def bind_widget(self, widget: tkinter.Tk) -> Self:
        """
        Widget to update when this icon is updated.

        Arguments
        ---
        `widget` - The widget to bind.
        """
        self.children.append(widget)
        return self

    def unbind_widget(self, widget: tkinter.Tk) -> Self:
        """
        Unbind widget from this icon.

        Arguments
        ---
        `widget` - The widget to unbind.
        """
        try:
            self.children.remove(widget)
        except ValueError:
            pass
        return self

    def bind(self, sequence: str, func) -> Self:
        """
        Runs this function callback when it needs to update.

        Arguments
        ---
        `sequence` - bind sequence for this widget. Only `<<updated>>` is valid.

        `func` - The callback function.
        """
        match sequence:
            case "<<updated>>":
                self._binds["updated"] = func
            case _:
                raise IconError(f"Unknown bind sequence '{sequence}'")
        return self

    def unbind(self, sequence: str) -> Self:
        """
        Binding to unbind

        Arguments
        ---
        `sequence` - The sequence to remove.
        """
        return self

    def get(self, format="imagetk"):
        """
        Returns the icon in the selected format.

        Arguments
        ---
        `format` - The image format to return.

        Formats
        ---
        - `imagefile` - ImageFile.ImageFile
        - `imagetk` - tkinter.PhotoImage
        """
        match format.lower():
            case "imagefile":
                return self._image
            case "imagetk":
                return self._photo
        raise ValueError(format)

    def __repr__(self):
        return self.get("imagetk")

    def __str__(self):
        return str(self.get("imagetk"))


class Job:
    def __init__(self, icon: Icon):
        self.icon: MaterialIcon = icon
        self.auth = os.getenv("GITHUB_TOKEN")  # Get token from .env file

    def task_done(self):
        self.icon.configure(
            file=os.path.join(self.icon.cache_path, self.icon._filename())
        )
        __queue__.task_done()

    def get(self, url: str) -> dict:
        if self.auth:
            headers = {"Authorization": "Bearer " + self.auth}
            res = requests.get(url, headers=headers).json()
        else:
            res = requests.get(url).json()
        # Error should be printed to console but should not break the entire script. Use the default icon if error.
        if "message" in res:
            raise IconError(
                res["message"] + " Documentation: " + res["documentation_url"]
            )
        return res

    def fetch_icon(self):
        # Test that the icon exists
        if self.icon.exists() is None:
            repo = self.get(
                "https://api.github.com/repos/google/material-design-icons/git/trees/26bf62e3918daebf134ef32b74b822953bb19015"
            )
            for ti in repo["tree"]:
                cats = self.get(ti["url"])
                for c in cats["tree"]:
                    if c["path"] == self.icon.name:
                        styles = self.get(c["url"])
                        match self.icon.style:
                            case "filled":
                                url = styles["tree"][0]["url"]
                            case "outlined":
                                url = styles["tree"][1]["url"]
                            case "rounded":
                                url = styles["tree"][2]["url"]
                            case "sharp":
                                url = styles["tree"][3]["url"]
                            case "two_tone":
                                url = styles["tree"][4]["url"]
                            case _:
                                raise IconError(
                                    'icon style must be [filled, outlined, rounded, sharp, two_tone] but got "%s"'
                                    % self.icon.style
                                )
                        res = self.get(url)["tree"][3]["url"]
                        res2 = self.get(res)["tree"][0]["url"]
                        blob = self.get(res2)["tree"][0]["url"]
                        img = self.get(blob)["content"]
                        os.makedirs(self.icon.cache_path, exist_ok=True)
                        filename = self.icon._filename()
                        with open(
                            os.path.join(self.icon.cache_path, filename), "wb"
                        ) as f:
                            f.write(base64.b64decode(img))
                        return os.path.join(self.icon.cache_path, filename)
            raise IconError('icon "%s" could not be found!' % self.icon.name)


__queue__ = queue.Queue()
__thread__ = None


def _worker() -> None:
    # wait until internet is enabled
    while True:
        try:
            requests.get('https://github.com/"', timeout=5)
            break
        except (requests.ConnectionError, requests.Timeout):
            pass

    while True:
        item: Job = __queue__.get()
        item.fetch_icon()
        item.task_done()


def init():
    global __thread__
    if __thread__ is None:
        __thread__ = threading.Thread(target=_worker, daemon=True)
        __thread__.start()


class _IconHelper(Icon):
    def __init__(self, cache_path: str = None, offline: bool = None, **kw):
        """
        Helper class to download an icon from an API.

        Arguments
        ---
        `cache_path` - The directory to place all downloaded icons.

        `offline` - When true it will not download any icons.

        `file` - The path to the image to use.

        `color` - The color of the icon. Uses native color by defauit.

        `size` - The size of the icon. Uses native size by default.

        Methods
        ---
        exists, update, configure, show, bind_widget, unbind_widget, bind, unbind, get
        """
        super().__init__(file=Asset.MISSING, **kw)
        self.offline = False
        self.cache_path = os.path.join(os.getcwd(), ".cache")

        init()  # Start queue loop it not running
        self.configure(cache_path=cache_path, offline=offline, **kw)

    def _filename(self) -> str:
        return hashlib.sha1(
            str(self.name + "_" + self.style).encode("utf-8")
        ).hexdigest()

    def exists(self) -> str | None:
        """Checks if the icon is already cached"""
        path = os.path.join(self.cache_path, self._filename())
        if os.path.exists(path) and os.path.isfile(path):
            return path
        return None

    def configure(self, **kw) -> None:
        if "offline" in kw and kw["offline"] != None:
            self.offline = kw.pop("offline")
        if "cache_path" in kw and kw["cache_path"] != None:
            self.cache_path = kw.pop("cache_path")
        super().configure(**kw)

    config = configure


class MaterialIcon(_IconHelper):
    def __init__(self, name: str, style: str = None, **kw):
        """
        Download and use Google's material icons. https://fonts.google.com/icons?selected=Material+Icons

        **NOTE**: You may want to add authentication to prevent Github from rate limiting this IP. https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting

        Arguments
        ---
        `name` - Name of the Material Icon to use.

        `style` - Style of icon to use. filled (default), outlined, rounded, sharp, twotone.

        `color` - The color of the icon. Uses native color by defauit.

        `size` - The size of the icon. Uses native size by default.

        Methods
        ---
        exists, update, configure, show, bind_widget, unbind_widget, bind, unbind, get
        """
        super().__init__(**kw)
        self.configure(style=style, name=name, **kw)

    @property
    def name(self) -> str:
        return getattr(self, "_name", "home")

    @name.setter
    def name(self, value: str):
        if value is None:
            self._name = "home"
        else:
            self._name = str(value)
        path = self.exists()
        if path is None:
            if self.offline:
                warnings.warn("Can't download icon as offline mode is enabled!")
            else:
                __queue__.put(Job(self))
        else:
            self.configure(file=path)

    @property
    def style(self) -> str:
        return getattr(self, "_style", FILLED)

    @style.setter
    def style(self, value: str):
        if value is None:
            self._style = FILLED
        elif value in [FILLED, OUTLINED, ROUNDED, SHARP, TWOTONE]:
            self._style = str(value)
        else:
            raise IconError(f"{value} is not a valid icon style!")

    def _get(self, url: str) -> dict:
        if self.auth != None:
            headers = {"Authorization": "Bearer " + self.auth}
            res = requests.get(url, headers=headers).json()
        else:
            res = requests.get(url).json()
        if "message" in res:
            raise IconError(
                res["message"] + " Documentation: " + res["documentation_url"]
            )
        return res

    def configure(self, **kw) -> None:
        if "style" in kw and kw["style"] != None:
            self.style = kw.pop("style")
        if "name" in kw and kw["name"] != None:
            self.name = kw.pop("name")
        super().configure(**kw)

    config = configure


# TODO remove me! uses a new version
class MaterialIcon2(Icon):
    def __init__(
        self,
        name: str,
        style: str = None,
        cache_path: str = None,
        offline: bool = None,
        **kw,
    ):
        """
        Download and use Google's material icons.

        Browse for any icon: https://fonts.google.com/icons?selected=Material+Icons

        **NOTE**: You may want to add authentication to prevent Github from rate limiting this IP. https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
        """
        super().__init__(file=Asset.MISSING, **kw)
        self.offline = False
        self.cache_path = os.path.join(os.getcwd(), ".cache")

        init()  # Start queue loop it not running
        self.configure(
            style=style, name=name, cache_path=cache_path, offline=offline, **kw
        )

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is None:
            self._name = "home"
        else:
            self._name = str(value)
        path = self.exists()
        if path is None:
            if self.offline:
                warnings.warn("Can't download icon as offline mode is enabled!")
            else:
                __queue__.put(Job(self))
        else:
            self.configure(file=path)

    @property
    def style(self) -> str:
        return self._style

    @style.setter
    def style(self, value: str):
        if value is None:
            self._style = FILLED
        elif value in [FILLED, OUTLINED, ROUNDED, SHARP, TWOTONE]:
            self._style = str(value)
        else:
            raise IconError(f"{value} is not a valid icon style!")

    def _get(self, url: str):
        if self.auth != None:
            headers = {"Authorization": "Bearer " + self.auth}
            res = requests.get(url, headers=headers).json()
        else:
            res = requests.get(url).json()
        if "message" in res:
            raise IconError(
                res["message"] + " Documentation: " + res["documentation_url"]
            )
        return res

    def _hash_name(self):
        return hashlib.sha1(
            str(self.name + "_" + self.style).encode("utf-8")
        ).hexdigest()

    def exists(self):
        """Checks if the icon is already cached"""
        path = os.path.join(self.cache_path, self._hash_name())
        if os.path.exists(path) and os.path.isfile(path):
            return path
        return None

    def configure(self, **kw):
        if "offline" in kw and kw["offline"] != None:
            self.offline = kw.pop("offline")
        if "style" in kw and kw["style"] != None:
            self.style = kw.pop("style")
        if "name" in kw and kw["name"] != None:
            self.name = kw.pop("name")
        if "cache_path" in kw and kw["cache_path"] != None:
            self.cache_path = kw.pop("cache_path")
        super().configure(**kw)

    config = configure
