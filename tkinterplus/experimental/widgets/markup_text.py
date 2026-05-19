# TODO
# -
from typing import Self
from _tkinter import TclError
from enum import Enum
from tkinter import colorchooser
import tkinter
import uuid
import os

from ...constants import *
from ... import MaterialIcon, Footer

__all__ = ["MarkupText"]

# NOTE This widget is still being worked on. Expect issues for missing features!
# - Store style as a diffrent varaible for exporting
# https://stackoverflow.com/questions/63099026/fomatted-text-in-tkinter

# TODO Should be refactored to match rich_message.RichMessage


# A Text widget that will format it (coloring, bold, italic, images, etc)
class MarkupText(tkinter.Frame):
    def __init__(
        self,
        master: tkinter.Tk,
        format=None,
        variable=None,
        controls: bool = True,
        fg: str = None,
        bg: str = None,
        width: int = None,
        height: int = None,
        insertbackground: str = None,
        selectbackground: str = None,
        selectforeground: str = None,
        button_bg: str = None,
        button_fg: str = None,
        button_activebackground: str = None,
        button_activeforeground: str = None,
        button_disabledforeground: str = None,
        border_width: int = None,
        border_color: str = None,
        **kw
    ):
        """Construct a formattext widget with the parent MASTER."""
        self.variable = tkinter.StringVar()
        self.fullscreen = False
        self._color = "red"

        # Variables
        self.state = "normal"
        self.format = "html"
        self.fg = "black"
        self.bg = "white"
        self.width = 50
        self.height = 20
        self.insertbackground = "black"
        self.selectbackground = "blue"
        self.selectforeground = "white"
        self.border_width = 1
        self.border_color = "white"
        self.button_bg = "#f0f0f0"
        self.button_fg = "black"
        self.button_activebackground = "#f0f0f0"
        self.button_activeforeground = "black"
        self.button_disabledforeground = "gray"

        self._fg_style = self.fg
        self._bg_style = self.bg

        super().__init__(master, width=self.width, height=self.height)

        # Bold Italic Underlined Strikethrough Blockquote [Paragrapgh, h1,h2,h3,h4,h5,h6, pre] Left Center Right Size Color UnorderedList OrderedList HorizontalLine InsertLink InsertImage
        self.toolbar = tkinter.Frame(self, bg=self.bg)
        self.toolbar.grid(row=0, column=0, sticky="ew")

        self._text = tkinter.Text(
            self,
            bg=self.bg,
            fg=self.fg,
            borderwidth=self.border_width,
            insertbackground=self.insertbackground,
            selectbackground=self.selectbackground,
            selectforeground=self.selectforeground,
        )
        self._text.grid(row=1, column=0, sticky="nesw")

        # Binds
        self.bind("<Control-b>", lambda e: self._style("BOLD"))
        self.bind("<Control-i>", lambda e: self._style("ITALIC"))
        self.bind("<Control-u>", lambda e: self._style("UNDERLINED"))

        # Bind cursor movements
        self.bind("<Button-1>", self._update_controls)
        self.bind("<Up>", self._update_controls)
        self.bind("<Down>", self._update_controls)
        self.bind("<Left>", self._update_controls)
        self.bind("<Right>", self._update_controls)
        self.bind("<Home>", self._update_controls)
        self.bind("<End>", self._update_controls)

        # Responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.configure(
            fg=fg,
            bg=bg,
            width=width,
            height=height,
            insertbackground=insertbackground,
            border_width=border_width,
            border_color=border_color,
            selectbackground=selectbackground,
            selectforeground=selectforeground,
            format=format,
            controls=controls,
            variable=variable,
            button_bg=button_bg,
            button_fg=button_fg,
            button_activebackground=button_activebackground,
            button_activeforeground=button_activeforeground,
            button_disabledforeground=button_disabledforeground,
            **kw
        )

    def update(self) -> None:
        # Text -> FormatVar
        def text_to_var(e: tkinter.Event):
            v = self._text.get(0.0, "end-1c")
            self.variable.set(v)

        self._text.bind("<KeyRelease>", text_to_var)

    def _controls(self) -> None:
        # ICONS
        self.ALIGN_LEFT = MaterialIcon(
            "format_align_left", size=(24, 24), color=self.button_fg
        )
        self.ALIGN_CENTER = MaterialIcon(
            "format_align_center", size=(24, 24), color=self.button_fg
        )
        self.ALIGN_RIGHT = MaterialIcon(
            "format_align_right", size=(24, 24), color=self.button_fg
        )
        self.CODE = MaterialIcon("code", size=(24, 24), color=self.button_fg)
        self.EXIT_FULLSCREEN = MaterialIcon(
            "fullscreen_exit", size=(24, 24), color=self.button_fg
        )
        self.BLOCKQUOTE = MaterialIcon(
            "format_quote", size=(24, 24), color=self.button_fg
        )
        self.BOLD = MaterialIcon("format_bold", size=(24, 24), color=self.button_fg)
        self.CLEAR_FORMAT = MaterialIcon(
            "format_clear", size=(24, 24), color=self.button_fg
        )
        self.ITALIC = MaterialIcon("format_italic", size=(24, 24), color=self.button_fg)
        self.ORDERED_LIST = MaterialIcon(
            "format_list_numbered", size=(24, 24), color=self.button_fg
        )
        self.UNORDERED_LIST = MaterialIcon(
            "format_list_bulleted", size=(24, 24), color=self.button_fg
        )
        self.FOREGROUND_COLOR = MaterialIcon(
            "format_color_text", size=(24, 24), color=self.fg
        )
        self.BACKGROUND_COLOR = MaterialIcon(
            "format_color_fill", size=(24, 24), color=self.bg
        )
        self.UNDERLINED = MaterialIcon(
            "format_underlined", size=(24, 24), color=self.button_fg
        )
        self.FULLSCREEN = MaterialIcon(
            "fullscreen", size=(24, 24), color=self.button_fg
        )
        self.INSERT_IMAGE = MaterialIcon("image", size=(24, 24), color=self.button_fg)
        self.INSERT_LINK = MaterialIcon("link", size=(24, 24), color=self.button_fg)
        self.UNLINK = MaterialIcon("link_off", size=(24, 24), color=self.button_fg)
        self.STRIKETHROUGH = MaterialIcon(
            "format_strikethrough", size=(24, 24), color=self.button_fg
        )

        btn = {
            "fg": self.button_fg,
            "bg": self.button_bg,
            "activebackground": self.button_activebackground,
            "activeforeground": self.button_activeforeground,
            "disabledforeground": self.button_disabledforeground,
        }

        self.bold_btn = tkinter.Button(
            self.toolbar, image=self.BOLD, command=lambda: self._style("BOLD"), **btn
        )
        self.italic_btn = tkinter.Button(
            self.toolbar,
            image=self.ITALIC,
            command=lambda: self._style("ITALIC"),
            **btn
        )
        self.underlined_btn = tkinter.Button(
            self.toolbar,
            image=self.UNDERLINED,
            command=lambda: self._style("UNDERLINED"),
            **btn
        )
        self.strikethrough_btn = tkinter.Button(
            self.toolbar,
            image=self.STRIKETHROUGH,
            command=lambda: self._style("STRIKETHROUGH"),
            **btn
        )
        self.blockquote_btn = tkinter.Button(
            self.toolbar,
            image=self.BLOCKQUOTE,
            command=lambda: self._style("BLOCKQUOTE"),
            **btn
        )
        # Type
        self.align_left_btn = tkinter.Button(
            self.toolbar,
            image=self.ALIGN_LEFT,
            command=lambda: self._style("ALIGN_LEFT"),
            **btn
        )
        self.align_center_btn = tkinter.Button(
            self.toolbar,
            image=self.ALIGN_CENTER,
            command=lambda: self._style("ALIGN_RIGHT"),
            **btn
        )
        self.align_right_btn = tkinter.Button(
            self.toolbar,
            image=self.ALIGN_RIGHT,
            command=lambda: self._style("ALIGN_RIGHT"),
            **btn
        )
        # Size
        self.fg_color_btn = tkinter.Button(
            self.toolbar,
            image=self.FOREGROUND_COLOR,
            command=lambda: self._style("FOREGROUND_COLOR", color=self._fg_style),
            **btn
        )
        self.fg_color_btn.bind("<Button-3>", lambda e: self._changeColor("fg"))

        self.bg_color_btn = tkinter.Button(
            self.toolbar,
            image=self.BACKGROUND_COLOR,
            command=lambda: self._style("BACKGROUND_COLOR", color=self._bg_style),
            **btn
        )
        self.bg_color_btn.bind("<Button-3>", lambda e: self._changeColor("bg"))

        self.unordered_list_btn = tkinter.Button(
            self.toolbar,
            image=self.UNORDERED_LIST,
            command=lambda: self._style("UNORDERED_LIST"),
            **btn
        )
        self.ordered_list_btn = tkinter.Button(
            self.toolbar,
            image=self.ORDERED_LIST,
            command=lambda: self._style("ORDERED_LIST"),
            **btn
        )
        self.insert_link_btn = tkinter.Button(
            self.toolbar,
            image=self.INSERT_LINK,
            command=lambda: self._style("INSERT_LINK"),
            **btn
        )
        self.insert_image_btn = tkinter.Button(
            self.toolbar,
            image=self.INSERT_IMAGE,
            command=lambda: self._style("INSERT_IMAGE"),
            **btn
        )

        self.fullscreen_btn = tkinter.Button(
            self.toolbar,
            image=self.FULLSCREEN,
            command=lambda: self._fullscreen(),
            **btn
        )

        # Geo
        self.bold_btn.grid(row=0, column=0)
        self.italic_btn.grid(row=0, column=1)
        self.underlined_btn.grid(row=0, column=2)
        self.strikethrough_btn.grid(row=0, column=3)
        self.blockquote_btn.grid(row=0, column=4)

        self.align_left_btn.grid(row=0, column=6)
        self.align_center_btn.grid(row=0, column=7)
        self.align_right_btn.grid(row=0, column=8)

        self.fg_color_btn.grid(row=0, column=10)
        self.bg_color_btn.grid(row=0, column=11)
        self.unordered_list_btn.grid(row=0, column=12)
        self.ordered_list_btn.grid(row=0, column=13)
        self.insert_link_btn.grid(row=0, column=14)
        self.insert_image_btn.grid(row=0, column=15)
        self.fullscreen_btn.grid(row=0, column=16, sticky="e")

    def update_style(self, name=None, value=None, style=None) -> None:
        """update the style"""
        # remove all tags
        self._text.tag_delete("all")
        self.variable.apply_style(self._text)

    def _changeColor(self, type: str) -> None:
        new_color = colorchooser.askcolor(self._color)
        if new_color[1] != None:
            c = new_color[1]

            if type == "fg":
                self._fg_style = c
                self.FOREGROUND_COLOR.configure(color=c)
                self.fg_color_btn.configure(image=self.FOREGROUND_COLOR)
            elif type == "bg":
                self._bg_style = c
                self.BACKGROUND_COLOR.configure(color=c)
                self.bg_color_btn.configure(image=self.BACKGROUND_COLOR)

    def _fullscreen(self) -> None:
        def _confirm():
            print("WORKED")
            self._fullscreen()

        if self.fullscreen == True:
            # close
            self.configure(state="normal")
            self.fullscreen_btn.configure(image=self.FULLSCREEN)
            self.fullscreen = False
            self.fullWindow.destroy()
        else:
            # full
            self.configure(state="disabled")
            self.fullscreen_btn.configure(image=self.EXIT_FULLSCREEN)
            self.fullscreen = True

            self.fullWindow = tkinter.Toplevel(self.master)
            self.fullWindow.title("Fullscreen")
            self.fullWindow.protocol("WM_DELETE_WINDOW", self._fullscreen)

            tkinter.Button(self.fullWindow, text="WORKED").grid(row=0, column=0)

            foot = Footer(self.fullWindow)
            foot.add_button("Save", _confirm)
            foot.add_button("Cancel", self._fullscreen)

    def _update_controls(self, e: tkinter.Event = None) -> None:
        """Update the controls when the user moves the cursor"""
        if self.controls:
            index = self._text.index("insert")
            styles = self.variable.get_style(float(index))
            # print('++ STYLE ++', index)

            # Reset State
            self.bold_btn.configure(state="normal")
            self.italic_btn.configure(state="normal")
            self.underlined_btn.configure(state="normal")
            self.strikethrough_btn.configure(state="normal")
            self.blockquote_btn.configure(state="normal")
            self.align_left_btn.configure(state="normal")
            self.align_center_btn.configure(state="normal")
            self.align_right_btn.configure(state="normal")
            self.unordered_list_btn.configure(state="normal")
            self.ordered_list_btn.configure(state="normal")
            self.insert_link_btn.configure(state="normal")
            self.insert_image_btn.configure(state="normal")

            # Disable
            for s in styles:
                if s.type == "BOLD":
                    self.bold_btn.configure(state="normal")
                elif s.type == "ITALIC":
                    self.italic_btn.configure(state="normal")
                elif s.type == "UNDERLINED":
                    self.underlined_btn.configure(state="normal")
                elif s.type == "STRIKETHROUGH":
                    self.strikethrough_btn.configure(state="normal")
                elif s.type == "BLOCKQUOTE":
                    self.blockquote_btn.configure(state="normal")
                elif s.type == "ALIGN_LEFT":
                    self.align_left_btn.configure(state="normal")
                elif s.type == "ALIGN_CENTER":
                    self.align_center_btn.configure(state="normal")
                elif s.type == "ALIGN_RIGHT":
                    self.align_right_btn.configure(state="normal")
                elif s.type == "UNORDERED_LIST":
                    self.unordered_list_btn.configure(state="normal")
                elif s.type == "ORDERED_LIST":
                    self.ordered_list_btn.configure(state="normal")
                elif s.type == "INSERT_LINK":
                    self.insert_link_btn.configure(state="normal")
                elif s.type == "INSERT_IMAGE":
                    self.insert_image_btn.configure(state="normal")

    def _style(self, format, **kw) -> None:
        try:
            first = self._text.index("sel_first")
            last = self._text.index("sel_last")
            self.variable.add_style(float(first), float(last), format, **kw)
            self.update_style()
        except TclError:
            pass

    # Default

    def configure(self, **kw) -> Self:
        if "variable" in kw and kw["variable"] != None:
            self.variable = kw.pop("variable")
            self._text.delete(0.0, "end")
            self._text.insert(0.0, self.variable.get(0.0, "end"))

        if "border_width" in kw and kw["border_width"] != None:
            self.border_width = kw.pop("border_width")
            self._text.configure(borderwidth=self.border_width)

        if "border_color" in kw and kw["border_color"] != None:
            self.border_color = kw.pop("border_color")
        if "button_fg" in kw and kw["button_fg"] != None:
            self.bordebutton_fgr_color = kw.pop("button_fg")
        if "button_bg" in kw and kw["button_bg"] != None:
            self.button_bg = kw.pop("button_bg")
        if "button_activebackground" in kw and kw["button_activebackground"] != None:
            self.button_activebackground = kw.pop("button_activebackground")
        if "button_activeforeground" in kw and kw["button_activeforeground"] != None:
            self.button_activeforeground = kw.pop("button_activeforeground")
        if (
            "button_disabledforeground" in kw
            and kw["button_disabledforeground"] != None
        ):
            self.button_disabledforeground = kw.pop("button_disabledforeground")

        if "state" in kw and kw["state"] != None:
            self.state = kw.pop("state")
            self._text.configure(state=self.state)

        if "format" in kw and kw["format"] != None:
            self.format = kw.pop("format")
        if "controls" in kw and kw["controls"] != None:
            self.controls = kw.pop("controls")
            if self.controls:
                self._controls()
        if "bg" in kw and kw["bg"] != None:
            self.bg = kw.pop("bg")
            self._text.configure(bg=self.bg)
        if "fg" in kw and kw["fg"] != None:
            self.fg = kw.pop("fg")
            self._text.configure(fg=self.fg)
        if "insertbackground" in kw and kw["insertbackground"] != None:
            self.insertbackground = kw.pop("insertbackground")
            self._text.configure(insertbackground=self.insertbackground)
        if "selectbackground" in kw and kw["selectbackground"] != None:
            self.selectbackground = kw.pop("selectbackground")
            self._text.configure(selectbackground=self.selectbackground)
        if "selectforeground" in kw and kw["selectforeground"] != None:
            self.selectbackground = kw.pop("selectforeground")
            self._text.configure(selectforeground=self.selectforeground)
        if "width" in kw and kw["width"] != None:
            self.width = kw.pop("width")
            super().configure(width=self.width)
        if "height" in kw and kw["height"] != None:
            self.height = kw.pop("height")
            super().configure(height=self.height)

        self.update()
        return self

    config = configure

    def bind(self, sequence: str, func, add: bool = False) -> None:
        """Bind to this widget at event SEQUENCE a call to function FUNC."""
        self._text.bind(sequence, func, add)

    def unbind(self, sequence: str, funcid: str = None) -> None:
        """Unbind for this widget for event SEQUENCE the function identified with FUNCID."""
        self._text.unbind(sequence, funcid)

    # FormatVar
    def insert(self, index1: float, chars: str) -> None:
        self.variable.insert(index1, chars)

    def get(self, index1: float, index2: float) -> None:
        self.variable.get(index1, index2)

    def delete(self, index1: float, index2: float) -> None:
        self.variable.delete(index1, index2)
