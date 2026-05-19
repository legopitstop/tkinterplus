import tkinter
from typing import Union, Tuple, Optional

from customtkinter.windows.widgets.core_rendering import CTkCanvas
from customtkinter.windows.widgets.ctk_scrollbar import CTkScrollbar
from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.widgets.core_rendering import DrawEngine
from customtkinter.windows.widgets.core_widget_classes import CTkBaseClass
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.utility import (
    pop_from_dict_by_set,
    check_kwargs_empty,
)

__all__ = ["CTkListbox"]


class CTkListbox(CTkBaseClass):
    """
    Listbox with x and y scrollbars, rounded corners, and all text features of tkinter.Listbox widget.
    Scrollbars only appear when they are needed. Text is wrapped on line end by default,
    set wrap='none' to disable automatic line wrapping.
    For detailed information check out the documentation.

    Detailed methods and parameters of the underlaying tkinter.Listbox widget can be found here:
    https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/listbox.html
    (most of them are implemented here too)
    """

    _scrollbar_update_time = 200  # interval in ms, to check if scrollbars are needed

    # attributes that are passed to and managed by the tkinter listbox only:
    _valid_tk_text_attributes = {
        "autoseparators",
        "cursor",
        "exportselection",
        "insertborderwidth",
        "insertofftime",
        "insertontime",
        "insertwidth",
        "maxundo",
        "padx",
        "pady",
        "selectborderwidth",
        "spacing1",
        "spacing2",
        "spacing3",
        "state",
        "tabs",
        "takefocus",
        "undo",
        "wrap",
        "xscrollcommand",
        "yscrollcommand",
    }

    def __init__(
        self,
        master: any,
        width: int = 200,
        height: int = 200,
        corner_radius: Optional[int] = None,
        border_width: Optional[int] = None,
        border_spacing: int = 3,
        bg_color: Union[str, Tuple[str, str]] = "transparent",
        fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        border_color: Optional[Union[str, Tuple[str, str]]] = None,
        text_color: Optional[Union[str, str]] = None,
        scrollbar_button_color: Optional[Union[str, Tuple[str, str]]] = None,
        scrollbar_button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
        font: Optional[Union[tuple, CTkFont]] = None,
        activate_scrollbars: bool = True,
        **kwargs
    ):

        # transfer basic functionality (_bg_color, size, __appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height)

        # color
        self._fg_color = (
            ThemeManager.theme["CTkTextbox"]["fg_color"]
            if fg_color is None
            else self._check_color_type(fg_color, transparency=True)
        )
        self._border_color = (
            ThemeManager.theme["CTkTextbox"]["border_color"]
            if border_color is None
            else self._check_color_type(border_color)
        )
        self._text_color = (
            ThemeManager.theme["CTkTextbox"]["text_color"]
            if text_color is None
            else self._check_color_type(text_color)
        )
        self._scrollbar_button_color = (
            ThemeManager.theme["CTkTextbox"]["scrollbar_button_color"]
            if scrollbar_button_color is None
            else self._check_color_type(scrollbar_button_color)
        )
        self._scrollbar_button_hover_color = (
            ThemeManager.theme["CTkTextbox"]["scrollbar_button_hover_color"]
            if scrollbar_button_hover_color is None
            else self._check_color_type(scrollbar_button_hover_color)
        )

        # shape
        self._corner_radius = (
            ThemeManager.theme["CTkTextbox"]["corner_radius"]
            if corner_radius is None
            else corner_radius
        )
        self._border_width = (
            ThemeManager.theme["CTkTextbox"]["border_width"]
            if border_width is None
            else border_width
        )
        self._border_spacing = border_spacing

        # font
        self._font = CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        self._canvas = CTkCanvas(
            master=self,
            highlightthickness=0,
            width=self._apply_widget_scaling(self._desired_width),
            height=self._apply_widget_scaling(self._desired_height),
        )
        self._canvas.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")
        self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))
        self._draw_engine = DrawEngine(self._canvas)

        self._listbox = tkinter.Listbox(
            self,
            fg=self._apply_appearance_mode(self._text_color),
            width=0,
            height=0,
            font=self._apply_font_scaling(self._font),
            highlightthickness=0,
            relief="flat",
            bg=self._apply_appearance_mode(self._fg_color),
            **pop_from_dict_by_set(kwargs, self._valid_tk_text_attributes)
        )

        check_kwargs_empty(kwargs, raise_error=True)

        # scrollbars
        self._scrollbars_activated = activate_scrollbars
        self._hide_x_scrollbar = True
        self._hide_y_scrollbar = True

        self._y_scrollbar = CTkScrollbar(
            self,
            width=8,
            height=0,
            border_spacing=0,
            fg_color=self._fg_color,
            button_color=self._scrollbar_button_color,
            button_hover_color=self._scrollbar_button_hover_color,
            orientation="vertical",
            command=self._listbox.yview,
        )
        self._listbox.configure(yscrollcommand=self._y_scrollbar.set)

        self._x_scrollbar = CTkScrollbar(
            self,
            height=8,
            width=0,
            border_spacing=0,
            fg_color=self._fg_color,
            button_color=self._scrollbar_button_color,
            button_hover_color=self._scrollbar_button_hover_color,
            orientation="horizontal",
            command=self._listbox.xview,
        )
        self._listbox.configure(xscrollcommand=self._x_scrollbar.set)

        self._create_grid_for_text_and_scrollbars(
            re_grid_listbox=True, re_grid_x_scrollbar=True, re_grid_y_scrollbar=True
        )

        self.after(50, self._check_if_scrollbars_needed)
        self._draw()

    def _create_grid_for_text_and_scrollbars(
        self,
        re_grid_listbox=False,
        re_grid_x_scrollbar=False,
        re_grid_y_scrollbar=False,
    ):

        # configure 2x2 grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(
            1,
            weight=0,
            minsize=self._apply_widget_scaling(
                max(self._corner_radius, self._border_width + self._border_spacing)
            ),
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(
            1,
            weight=0,
            minsize=self._apply_widget_scaling(
                max(self._corner_radius, self._border_width + self._border_spacing)
            ),
        )

        if re_grid_listbox:
            self._listbox.grid(
                row=0,
                column=0,
                rowspan=1,
                columnspan=1,
                sticky="nsew",
                padx=(
                    self._apply_widget_scaling(
                        max(
                            self._corner_radius,
                            self._border_width + self._border_spacing,
                        )
                    ),
                    0,
                ),
                pady=(
                    self._apply_widget_scaling(
                        max(
                            self._corner_radius,
                            self._border_width + self._border_spacing,
                        )
                    ),
                    0,
                ),
            )

        if re_grid_x_scrollbar:
            if not self._hide_x_scrollbar and self._scrollbars_activated:
                self._x_scrollbar.grid(
                    row=1,
                    column=0,
                    rowspan=1,
                    columnspan=1,
                    sticky="ewn",
                    pady=(3, self._border_spacing + self._border_width),
                    padx=(
                        max(
                            self._corner_radius,
                            self._border_width + self._border_spacing,
                        ),
                        0,
                    ),
                )  # scrollbar grid method without scaling
            else:
                self._x_scrollbar.grid_forget()

        if re_grid_y_scrollbar:
            if not self._hide_y_scrollbar and self._scrollbars_activated:
                self._y_scrollbar.grid(
                    row=0,
                    column=1,
                    rowspan=1,
                    columnspan=1,
                    sticky="nsw",
                    padx=(3, self._border_spacing + self._border_width),
                    pady=(
                        max(
                            self._corner_radius,
                            self._border_width + self._border_spacing,
                        ),
                        0,
                    ),
                )  # scrollbar grid method without scaling
            else:
                self._y_scrollbar.grid_forget()

    def _check_if_scrollbars_needed(self, event=None, continue_loop: bool = True):
        """Method hides or places the scrollbars if they are needed on key release event of tkinter.Listbox widget"""

        if self._scrollbars_activated:
            if (
                self._listbox.xview() != (0.0, 1.0)
                and not self._x_scrollbar.winfo_ismapped()
            ):  # x scrollbar needed
                self._hide_x_scrollbar = False
                self._create_grid_for_text_and_scrollbars(re_grid_x_scrollbar=True)
            elif (
                self._listbox.xview() == (0.0, 1.0)
                and self._x_scrollbar.winfo_ismapped()
            ):  # x scrollbar not needed
                self._hide_x_scrollbar = True
                self._create_grid_for_text_and_scrollbars(re_grid_x_scrollbar=True)

            if (
                self._listbox.yview() != (0.0, 1.0)
                and not self._y_scrollbar.winfo_ismapped()
            ):  # y scrollbar needed
                self._hide_y_scrollbar = False
                self._create_grid_for_text_and_scrollbars(re_grid_y_scrollbar=True)
            elif (
                self._listbox.yview() == (0.0, 1.0)
                and self._y_scrollbar.winfo_ismapped()
            ):  # y scrollbar not needed
                self._hide_y_scrollbar = True
                self._create_grid_for_text_and_scrollbars(re_grid_y_scrollbar=True)
        else:
            self._hide_x_scrollbar = False
            self._hide_x_scrollbar = False
            self._create_grid_for_text_and_scrollbars(re_grid_y_scrollbar=True)

        if self._listbox.winfo_exists() and continue_loop is True:
            self.after(
                self._scrollbar_update_time,
                lambda: self._check_if_scrollbars_needed(continue_loop=True),
            )

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)

        self._listbox.configure(font=self._apply_font_scaling(self._font))
        self._canvas.configure(
            width=self._apply_widget_scaling(self._desired_width),
            height=self._apply_widget_scaling(self._desired_height),
        )
        self._create_grid_for_text_and_scrollbars(
            re_grid_listbox=True, re_grid_x_scrollbar=True, re_grid_y_scrollbar=True
        )
        self._draw(no_color_updates=True)

    def _set_dimensions(self, width=None, height=None):
        super()._set_dimensions(width, height)

        self._canvas.configure(
            width=self._apply_widget_scaling(self._desired_width),
            height=self._apply_widget_scaling(self._desired_height),
        )
        self._draw()

    def _update_font(self):
        """pass font to tkinter widgets with applied font scaling and update grid with workaround"""
        self._listbox.configure(font=self._apply_font_scaling(self._font))

        # Workaround to force grid to be resized when text changes size.
        # Otherwise grid will lag and only resizes if other mouse action occurs.
        self._canvas.grid_forget()
        self._canvas.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")

    def destroy(self):
        if isinstance(self._font, CTkFont):
            self._font.remove_size_configure_callback(self._update_font)

        super().destroy()

    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)

        if not self._canvas.winfo_exists():
            return

        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(
            self._apply_widget_scaling(self._current_width),
            self._apply_widget_scaling(self._current_height),
            self._apply_widget_scaling(self._corner_radius),
            self._apply_widget_scaling(self._border_width),
        )

        if no_color_updates is False or requires_recoloring:
            if self._fg_color == "transparent":
                self._canvas.itemconfig(
                    "inner_parts",
                    fill=self._apply_appearance_mode(self._bg_color),
                    outline=self._apply_appearance_mode(self._bg_color),
                )
                self._listbox.configure(
                    fg=self._apply_appearance_mode(self._text_color),
                    bg=self._apply_appearance_mode(self._bg_color),
                )
                self._x_scrollbar.configure(
                    fg_color=self._bg_color,
                    scrollbar_color=self._scrollbar_button_color,
                    scrollbar_hover_color=self._scrollbar_button_hover_color,
                )
                self._y_scrollbar.configure(
                    fg_color=self._bg_color,
                    scrollbar_color=self._scrollbar_button_color,
                    scrollbar_hover_color=self._scrollbar_button_hover_color,
                )
            else:
                self._canvas.itemconfig(
                    "inner_parts",
                    fill=self._apply_appearance_mode(self._fg_color),
                    outline=self._apply_appearance_mode(self._fg_color),
                )
                self._listbox.configure(
                    fg=self._apply_appearance_mode(self._text_color),
                    bg=self._apply_appearance_mode(self._fg_color),
                )
                self._x_scrollbar.configure(
                    fg_color=self._fg_color,
                    button_color=self._scrollbar_button_color,
                    button_hover_color=self._scrollbar_button_hover_color,
                )
                self._y_scrollbar.configure(
                    fg_color=self._fg_color,
                    button_color=self._scrollbar_button_color,
                    button_hover_color=self._scrollbar_button_hover_color,
                )

            self._canvas.itemconfig(
                "border_parts",
                fill=self._apply_appearance_mode(self._border_color),
                outline=self._apply_appearance_mode(self._border_color),
            )
            self._canvas.configure(bg=self._apply_appearance_mode(self._bg_color))

        self._canvas.tag_lower("inner_parts")
        self._canvas.tag_lower("border_parts")

    def configure(self, require_redraw=False, **kwargs):
        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(
                kwargs.pop("fg_color"), transparency=True
            )
            require_redraw = True

            # check if CTk widgets are children of the frame and change their _bg_color to new frame fg_color
            for child in self.winfo_children():
                if isinstance(child, CTkBaseClass) and hasattr(child, "_fg_color"):
                    child.configure(bg_color=self._fg_color)

        if "border_color" in kwargs:
            self._border_color = self._check_color_type(kwargs.pop("border_color"))
            require_redraw = True

        if "text_color" in kwargs:
            self._text_color = self._check_color_type(kwargs.pop("text_color"))
            require_redraw = True

        if "scrollbar_button_color" in kwargs:
            self._scrollbar_button_color = self._check_color_type(
                kwargs.pop("scrollbar_button_color")
            )
            self._x_scrollbar.configure(button_color=self._scrollbar_button_color)
            self._y_scrollbar.configure(button_color=self._scrollbar_button_color)

        if "scrollbar_button_hover_color" in kwargs:
            self._scrollbar_button_hover_color = self._check_color_type(
                kwargs.pop("scrollbar_button_hover_color")
            )
            self._x_scrollbar.configure(
                button_hover_color=self._scrollbar_button_hover_color
            )
            self._y_scrollbar.configure(
                button_hover_color=self._scrollbar_button_hover_color
            )

        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            self._create_grid_for_text_and_scrollbars(
                re_grid_listbox=True, re_grid_x_scrollbar=True, re_grid_y_scrollbar=True
            )
            require_redraw = True

        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            self._create_grid_for_text_and_scrollbars(
                re_grid_listbox=True, re_grid_x_scrollbar=True, re_grid_y_scrollbar=True
            )
            require_redraw = True

        if "border_spacing" in kwargs:
            self._border_spacing = kwargs.pop("border_spacing")
            self._create_grid_for_text_and_scrollbars(
                re_grid_listbox=True, re_grid_x_scrollbar=True, re_grid_y_scrollbar=True
            )
            require_redraw = True

        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)

            self._update_font()

        self._listbox.configure(
            **pop_from_dict_by_set(kwargs, self._valid_tk_text_attributes)
        )
        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "corner_radius":
            return self._corner_radius
        elif attribute_name == "border_width":
            return self._border_width
        elif attribute_name == "border_spacing":
            return self._border_spacing

        elif attribute_name == "fg_color":
            return self._fg_color
        elif attribute_name == "border_color":
            return self._border_color
        elif attribute_name == "text_color":
            return self._text_color

        elif attribute_name == "font":
            return self._font

        else:
            return super().cget(attribute_name)

    def bind(self, sequence=None, command=None, add=None):
        """called on the tkinter.Listbox"""

        # if sequence is <KeyRelease>, allow only to add the binding to keep the _listbox_modified_event() being called
        if sequence == "<KeyRelease>":
            return self._listbox.bind(sequence, command, add="+")
        else:
            return self._listbox.bind(sequence, command, add)

    def unbind(self, sequence, funcid=None):
        """called on the tkinter.Listbox"""
        return self._listbox.unbind(sequence, funcid)

    def focus(self):
        return self._listbox.focus()

    def focus_set(self):
        return self._listbox.focus_set()

    def focus_force(self):
        return self._listbox.focus_force()

    def insert(self, index, text, tags=None):
        self._check_if_scrollbars_needed()
        return self._listbox.insert(index, text, tags)

    def get(self, index1, index2=None):
        return self._listbox.get(index1, index2)

    def bbox(self, index):
        return self._listbox.bbox(index)

    def delete(self, index1, index2=None):
        return self._listbox.delete(index1, index2)

    def index(self, i):
        return self._listbox.index(i)

    def scan_dragto(self, x, y):
        return self._listbox.scan_dragto(x, y)

    def scan_mark(self, x, y):
        return self._listbox.scan_mark(x, y)

    def search(self, pattern, index, *args, **kwargs):
        return self._listbox.search(pattern, index, *args, **kwargs)

    def see(self, index):
        return self._listbox.see(index)

    def xview(self, *args):
        return self._listbox.xview(*args)

    def xview_moveto(self, fraction):
        return self._listbox.xview_moveto(fraction)

    def xview_scroll(self, n, what):
        return self._listbox.xview_scroll(n, what)

    def yview(self, *args):
        return self._listbox.yview(*args)

    def yview_moveto(self, fraction):
        return self._listbox.yview_moveto(fraction)

    def yview_scroll(self, n, what):
        return self._listbox.yview_scroll(n, what)
