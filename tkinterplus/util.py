from typing import Callable, Self, Any
import tkinter
import locale
import os
import json
import logging
import ctypes
import easing_functions
import numpy
import tinycss

from .constants import Ease, GRID, PACK, PLACE

__all__ = [
    "winfo_geometry_manager",
    "has_customtkinter",
    "setWinStyle",
    "hex_to_rgb",
    "luminance_color",
    "text_color",
    "Ease",
    "easing",
    "Language",
    "CSSParseError",
    "Selector",
    "parseCSS",
]


def winfo_geometry_manager(master: tkinter.Tk = None) -> str | None:
    """Retruns with the geoemtry type [GRID, PACK, PLACE, None]"""
    if master is None:
        master = tkinter._get_temp_root()
    if len(master.grid_slaves()) >= 1:
        return GRID
    if len(master.pack_slaves()) >= 1:
        return PACK
    if len(master.place_slaves()) >= 1:
        return PLACE
    return None


def has_customtkinter() -> bool:
    """Check if customtkinter is installed"""
    try:
        import ctk.ctk_iconbutton as ctk_iconbutton

        return True  # customtkinter is installed
    except ImportError:
        return False  # customtkinter is not installed


def setWinStyle(window: tkinter.Tk):
    """
    Removes all buttons except the close button at the titlebar.

    Source: https://stackoverflow.com/questions/2969870/removing-minimize-maximize-buttons-in-tkinter#answer-72664499
    """

    def callback(w) -> None:
        set_window_pos = ctypes.windll.user32.SetWindowPos
        set_window_long = ctypes.windll.user32.SetWindowLongPtrW
        get_window_long = ctypes.windll.user32.GetWindowLongPtrW
        get_parent = ctypes.windll.user32.GetParent

        # Identifiers
        gwl_style = -16

        ws_minimizebox = 131072
        ws_maximizebox = 65536

        swp_nozorder = 4
        swp_nomove = 2
        swp_nosize = 1
        swp_framechanged = 32

        hwnd = get_parent(w.winfo_id())
        old_style = get_window_long(hwnd, gwl_style)  # Get the style
        new_style = (
            old_style & ~ws_maximizebox & ~ws_minimizebox
        )  # New style, without max/min buttons
        set_window_long(hwnd, gwl_style, new_style)  # Apply the new style
        set_window_pos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            swp_nomove | swp_nosize | swp_nozorder | swp_framechanged,
        )  # Updates

    if isinstance(window, (tkinter.Tk, tkinter.Toplevel)):
        if os.name == "nt":
            window.after(
                10, lambda: callback(window)
            )  # call to change style after the mainloop started. Directly call setWinStyle will not work.
            return True
        return None

    else:
        raise TypeError(
            f"Window must be tkinter.Tk or tkinter.Toplevel not {window.__class__.__name__}"
        )


def easing(ease: Ease, start: int, end: int) -> Any:
    if not isinstance(ease, Ease):
        raise TypeError(f"{ease} should be Easing not {ease.__class__.__name__}")
    f = None
    match ease:
        case Ease.LINEAR:
            f = easing_functions.LinearInOut(start, end, end)
        case Ease.BOUNCE_IN:
            f = easing_functions.BounceEaseIn(start, end, end)
        case Ease.BOUNCE_OUT:
            f = easing_functions.BounceEaseOut(start, end - 1, end)
        case Ease.BOUNCE_IN_OUT:
            f = easing_functions.BounceEaseInOut(start, end - 1, end)
        case Ease.SINE_IN:
            f = easing_functions.SineEaseIn(start, end + 1, end)
        case Ease.SINE_OUT:
            f = easing_functions.SineEaseOut(start, end - 1, end)
        case Ease.SINE_IN_OUT:
            f = easing_functions.SineEaseInOut(start, end - 1, end)
        case Ease.CIRCULAR_IN:
            f = easing_functions.CircularEaseIn(start, end + 6, end)
        case Ease.CIRCULAR_OUT:
            f = easing_functions.CircularEaseOut(start, end - 1, end)
        case Ease.CIRCULAR_IN_OUT:
            f = easing_functions.CircularEaseInOut(start, end - 1, end)
        case Ease.QUAD_IN:
            f = easing_functions.QuadEaseIn(start, end + 1, end)
        case Ease.QUAD_OUT:
            f = easing_functions.QuadEaseOut(start, end - 1, end)
        case Ease.QUAD_IN_OUT:
            f = easing_functions.QuadEaseInOut(start, end - 1, end)
        case Ease.CUBIC_IN:
            f = easing_functions.CubicEaseIn(start, end + 2, end)
        case Ease.CUBIC_OUT:
            f = easing_functions.CubicEaseOut(start, end - 1, end)
        case Ease.CUBIC_IN_OUT:
            f = easing_functions.CubicEaseInOut(start, end - 1, end)
        case Ease.QUARTIC_IN:
            f = easing_functions.QuarticEaseIn(start, end + 3, end)
        case Ease.QUARTIC_OUT:
            f = easing_functions.QuarticEaseOut(start, end - 1, end)
        case Ease.QUARTIC_IN_OUT:
            f = easing_functions.QuarticEaseInOut(start, end - 1, end)
        case Ease.QUINTIC_IN:
            f = easing_functions.QuinticEaseIn(start, end + 5, end)
        case Ease.QUINTIC_OUT:
            f = easing_functions.QuinticEaseOut(start, end - 1, end)
        case Ease.QUINTIC_IN_OUT:
            f = easing_functions.QuinticEaseInOut(start, end - 1, end)
        case Ease.EXPONENTIAL_IN:
            f = easing_functions.ExponentialEaseIn(start, end + 7, end)
        case Ease.EXPONENTIAL_OUT:
            f = easing_functions.ExponentialEaseOut(start, end - 1, end)
        case Ease.EXPONENTIAL_IN_OUT:
            f = easing_functions.ExponentialEaseInOut(start, end - 1, end)
        case Ease.ELASTIC_IN:
            f = easing_functions.ElasticEaseIn(start, end, end)
        case Ease.ELASTIC_OUT:
            f = easing_functions.ElasticEaseOut(start, end - 1, end)
        case Ease.ELASTIC_IN_OUT:
            f = easing_functions.ElasticEaseInOut(start, end - 1, end)
        case Ease.BACK_IN:
            f = easing_functions.BackEaseIn(start, end + 9, end)
        case Ease.BACK_OUT:
            f = easing_functions.BackEaseOut(start, end - 1, end)
        case Ease.BACK_IN_OUT:
            f = easing_functions.BackEaseInOut(start, end - 1, end)
        case _:
            raise NotImplementedError(f'"{ease}" is not a valid easing function')
    x = numpy.arange(start, end, 1, dtype=int)
    return list(map(round, map(f, x)))


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def luminance_color(r: int, g: int, b: int) -> float:
    a = [r / 255.0, g / 255.0, b / 255.0]
    a = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in a]
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]


def text_color(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    bg_luminance = luminance_color(r, g, b)
    return "black" if bg_luminance > 0.179 else "white"


class EventHelper:
    @staticmethod
    def on_resize(master: tkinter.Tk, callback: Callable) -> str:
        """
        Run function when MASTER has been resized.

        :rtype: str
        """
        master._width = master.winfo_width()
        master._height = master.winfo_height()

        def resizing(e):
            width = master.winfo_width()
            height = master.winfo_height()
            if width != master._width or height != master._height:
                master._width = width
                master._height = height
                callback(e)

        return master.bind("<Configure>", resizing, add="+")

    @staticmethod
    def on_moved(master: tkinter.Tk, callback: Callable) -> str:
        """
        Run function when MASTER has been moved.

        :rtype: str
        """
        master._x = master.winfo_x()
        master._y = master.winfo_y()

        def moving(e):
            x = master.winfo_x()
            y = master.winfo_y()
            if x != master._x or y != master._y:
                master._x = x
                master._y = y
                callback(e)

        return master.bind("<Configure>", moving, add="+")


class Language:
    def __init__(self, default_language_code: str = None):
        """Translate text from a language JSON file"""
        self.default_code = default_language_code
        self.code, self._ = locale.getdefaultlocale()
        self.langs = {}
        self.variables = []

    def add_directory(self, path: str) -> None:
        """Add a directory of files"""
        for file in os.listdir(path):
            self.add_file(os.path.join(path, file))

    def add_file(self, fp: str) -> None:
        with open(fp, "r") as file:
            try:
                data = json.load(file)
                code = os.path.basename(fp).replace(".json", "").casefold()

                if code in self.langs:  # Merge data
                    for key in data:
                        self.langs[code][key] = data[key]
                else:
                    self.langs[code] = data  # Set data
            except json.decoder.JSONDecodeError as err:
                logging.debug('Failed to load langauge JSON "%s": %s', fp, err)

    def code_exists(self, language_code: str) -> bool:
        """Test if the language code exists"""
        if language_code.casefold() in self.langs:
            return True
        else:
            return False

    def translate(self, key: str) -> str:
        """Translate the text using the provided translation file."""
        code = self.code.casefold()
        default_code = self.default_code.casefold()
        if self.code_exists(code):
            if key in self.langs[code]:
                return self.langs[code][key]
            else:
                return key
        elif self.code_exists(default_code):
            if key in self.langs[default_code]:
                return self.langs[default_code][key]
            else:
                return key
        else:
            return key

    def _on_set(self) -> None:
        for variable in self.variables:
            variable[0].set(self.translate(variable[1]))

    def bind_variable(self, textvariable: tkinter.StringVar, key: str) -> None:
        """bind to textvariable"""
        textvariable.set(self.translate(key))
        self.variables.append((textvariable, key))

    def set(self, language_code: str) -> None:
        """Update the language code"""
        self.code = language_code
        self._on_set()


class CSSParseError(Exception):
    pass


class Selector(object):
    def __init__(self, value: str = None):
        self.tag = None
        self.cls = None
        self.id = None

        if value != None:
            cls = value.split(".")
            if len(cls) > 1:
                value = value.replace("." + cls[1], "")
                self.cls = cls[1]
            id = value.split("#")
            if len(id) > 1:
                value = value.replace("#" + id[1], "")
                self.id = id[1]
            if value != "":
                self.tag = value

    @property
    def link(self):
        return getattr(self, "_link", False)

    @link.setter
    def link(self, value):
        if value is None:
            self._link = False
        else:
            self._link = True

    def __str__(self) -> str:
        res = ""
        if self.tag is not None:
            res = self.tag
        if self.cls is not None:
            res += "." + self.cls
        if self.id is not None:
            res += "#" + self.id
        if self.link:
            res += ":link"
        return res

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Selector):
            if self.tag == "*":
                return True  # Always match

            if self.tag != None:
                if self.tag != __value.tag:
                    return False

            if self.cls != None:
                if self.cls != __value.cls:
                    return False

            if self.id != None:
                if self.id != __value.id:
                    return False

            if self.link != None:
                if self.link != __value.link:
                    return False
            return True
        return False


class parseCSS:
    def __init__(self):
        self.parser = tinycss.make_parser("page3")
        self.stylesheet = None

    def from_string(self, css: str) -> Self:
        """Parse CSS from string"""
        self.stylesheet = self.parser.parse_stylesheet_bytes(bytes(css, "utf-8"))
        if len(self.stylesheet.errors) > 1:
            raise CSSParseError(self.stylesheet.errors[0])
        return self

    def from_file(self, fp: str) -> Self:
        """Parse CSS from file"""
        self.stylesheet = self.parser.parse_stylesheet_file(fp)
        if len(self.stylesheet.errors) > 1:
            raise CSSParseError(self.stylesheet.errors[0])
        return self

    def getRules(self, selector: Selector) -> list:
        rules = []
        for r in self.stylesheet.rules:
            css = r.selector.as_css().split(",")
            for sel in css:
                if Selector(sel) == selector:
                    print(sel, selector)
                    rules.append(r)
        return rules

    def get(self, selector: Selector) -> dict:
        rules = self.getRules(selector)
        res = {}
        for r in rules:
            for dec in r.declarations:
                name = dec.name
                value = None
                simple = [
                    "color",
                    "background-color",
                    "display",
                    "margin-block-start",
                    "margin-block-end",
                    "margin-inline-start",
                    "margin-inline-end",
                    "font-weight",
                    "font-style",
                    "text-decoration",
                ]

                unit = [
                    "font-size",
                    "margin-top",
                    "margin-bottom",
                    "margin-right",
                    "margin-left",
                ]
                if name in simple:
                    value = dec.value[0].as_css()
                else:
                    if selector.tag != "*":
                        all = self.get(Selector("*"))
                    if name in unit:
                        value = dec.value[0].as_css()
                        if value.endswith("px"):
                            value = int(value.replace("px", ""))
                        elif value.endswith("em"):
                            em = float(value.replace("em", ""))
                            value = round(all.get("font-size") * em)
                            # value = int(value.replace('px', ''))

                        else:
                            value = int(value)

                res[name] = value
        return res
