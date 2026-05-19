import tkinter
import _tkinter
import dataclasses
from tkinter import ttk, messagebox
from typing import Any

from .. import has_customtkinter, EntryTypes, ScrolledConsole

__all__ = ["add_widget", "tk_widgets", "ctk_widgets", "tkp_widgets", "DeveloperTools"]

# TODO: Automatically detect tkinter.Widget and all its parameters, and methods


@dataclasses.dataclass
class _WidgetProperty:
    def __init__(self, type: str, get, set, from_: int = None, to: int = None):
        self.type = type
        self.get = get
        self.set = set
        self.from_ = from_
        self.to = to

    def kw(self) -> dict[str, int]:
        return {"from_": self.from_, "to": self.to}


class _RegisteredWidget:
    def __init__(
        self,
        cls,
        childcommand,
        deletecommand,
        deletechildcommand,
        createchildcommand,
        flasharg,
        state,
    ):
        """Internal class! Use add_widget() instead"""
        if isinstance(cls, tuple):
            self.name = []
            for c in cls:
                self.name.append(str(c.__name__))
        else:
            self.name = str(cls.__name__)
        self.cls = cls

        self.flasharg = flasharg
        self.state = state
        self.childcommand = self._builtin_childcommand(childcommand)
        self.deletecommand = deletecommand
        self.deletechildcommand = self._builtin_deletechildcommand(deletechildcommand)
        self.createchildcommand = self._builtin_createchildcommand(createchildcommand)

        self.properties = {}

    def flash(self, widget) -> None:
        """Flash the widget"""
        root: tkinter.Tk = tkinter._get_temp_root()

        def __flash(k, widget: tkinter.Widget):
            onkw = {}
            onkw[k] = "yellow"
            offkw = {}
            offkw[k] = widget.cget(k)
            root.after(100, lambda: widget.configure(**onkw))
            root.after(200, lambda: widget.configure(**offkw))
            root.after(300, lambda: widget.configure(**onkw))
            root.after(400, lambda: widget.configure(**offkw))

        if self.flasharg != None:
            __flash(self.flasharg, widget)

    def render_props(self, master: tkinter.Frame, widget: tkinter.Tk) -> bool:
        """Open edit window"""  # This should add a Properties tab under elements
        props = self.get_props(widget)
        if props != None:
            v = {}  # Stores all the tkinter Variables
            row = 0
            for k in props:
                p: _WidgetProperty = props[k]
                value = p.get(widget, k)
                lbl = str(k).replace("_", " ").title()
                label = tkinter.Label(master, text=lbl, anchor=tkinter.E)
                label.grid(row=row, column=0, sticky=tkinter.E, padx=2, pady=2)

                match p.type:
                    case "checkbox":
                        v[k] = tkinter.BooleanVar()
                    case "integer":
                        v[k] = tkinter.IntVar()
                    case "float":
                        v[k] = tkinter.DoubleVar()
                    case _:
                        v[k] = tkinter.StringVar()
                args = (widget, k, v[k], p)
                option = EntryTypes(
                    master,
                    p.type,
                    textvariable=v[k],
                    label=label,
                    command=lambda args=args: self.__call_setter(*args),
                    **p.kw(),
                )
                v[k].set(value)
                option.grid(row=row, column=1, sticky=tkinter.W, padx=2, pady=2)
                row += 1

            return True
        else:
            messagebox.showwarning(
                "PropertiesNotFound", "This widget does not have any properties!"
            )
            return False

        # Get a list of all items

    def get_props(self, widget) -> None | Any:
        """Get the widgets properties"""
        for w in self.properties:
            if w == widget.__class__.__name__:
                return self.properties[w]
        return None

    def add_prop(
        self,
        name: str,
        type: str,
        gettercommand=None,
        settercommand=None,
        widget=None,
        from_: int = None,
        to: int = None,
    ) -> None:
        """
        Add a property to this widget

        Arguments
        ---
        `name` - Name and key of the property

        `type` - The type of property. ex; str, int, float, etc

        `gettercommand` - The command to get the current value.

        `settercommand` - The command to run when configuring the widget

        `widget` - The widget that this applies to. If None it will apply to all .cls widgets
        """
        if gettercommand == None:
            gettercommand = self.__getter
        if settercommand == None:
            settercommand = self.__setter

        if widget == None:
            if isinstance(self.cls, tuple):
                for w in list(self.cls):
                    self.add_prop(name, type, widget=w)
            else:
                self.add_prop(name, type, widget=self.cls)

        else:
            w = str(widget.__name__)
            if w not in self.properties:
                self.properties[w] = {}
            self.properties[w][name] = _WidgetProperty(
                type=type, get=gettercommand, set=settercommand, from_=from_, to=to
            )

    # default setter and getter commands
    def __call_setter(
        self, w: tkinter.Widget, key: str, variable, p: _WidgetProperty
    ) -> None:
        data = {}
        data[key] = variable.get()
        p.set(w, data)

    def __setter(self, w: tkinter.Widget, data: dict) -> None:
        """The default setter (Sets the passed arg and value)"""
        w.configure(**data)

    def __getter(self, w: tkinter.Widget, key: str) -> Any:
        """The default getter (Returns the currnet value)"""
        return w.cget(key)

    # ChildCommands
    def __none(self, w: tkinter.Widget) -> None:
        return None

    def __Canvas(self, w: tkinter.Canvas):
        for id in w.find_all():
            type = w.type(id)
            yield (type, id, False)

    def __Listbox(self, w: tkinter.Listbox):
        i = 0
        for name in w.get(0, tkinter.END):
            yield (name, i, False)
            i += 1

    def __Text(self, w: tkinter.Text):
        for name in w.tag_names():
            yield ("tag", name, False)

    def __Notebook(self, w: ttk.Notebook):
        for name in w.tabs():
            c = w.nametowidget(name)
            yield (c.__class__.__name__, c, True)

    def __Container(self, w: tkinter.Widget):
        for c in w.winfo_children():
            # if isinstance(c, tkinter.Widget): yield (c.__class__.__name__, c, True) # This should get removed to support each widget seperately
            if isinstance(c, DeveloperTools):
                pass  # ignore self
            else:
                yield (c.__class__.__name__, c, True)

    def __Treeview(self, w: ttk.Treeview):
        for i in w.get_children():
            text = w.item(i, "text")
            yield (text, i, False)

    def __Menu(self, w: tkinter.Menu):
        end = w.index(tkinter.END)
        if end != None:
            for i in range(end + 1):
                name = w.entrycget(i, "label")
                yield (name, i, False)

        return None

    def __OptionMenu(self, w: tkinter.OptionMenu):
        m: tkinter.Menu = w["menu"]
        end = m.index(tkinter.END)
        if end != None:
            for i in range(end + 1):
                name = m.entrycget(i, "label")
                yield (name, i, False)
        return None

    # DeleteChildCommands
    def __CanvasItem(self, w: tkinter.Canvas, data: tuple) -> None:
        w.delete(data[2])

    def __TextTag(self, w: tkinter.Text, data: tuple) -> None:
        w.tag_delete(data[2])

    def __ListboxItem(self, w: tkinter.Listbox, data: tuple) -> None:
        w.delete(data[2])

    def __TreeviewItem(self, w: ttk.Treeview, data: tuple) -> None:
        w.delete(data[2])

    def __MenuItem(self, w: tkinter.Menu, data: tuple) -> None:
        w.delete(data[2])

    def __OptionMenuValue(self, w: tkinter.OptionMenu, data: tuple) -> None:
        try:
            m = w["menu"]
            m.delete(data[2])
        except _tkinter.TclError:
            messagebox.showwarning(
                "Developer Tools",
                "Failed to delete last item in OptionMenu! Must have at least one item in the menu!",
            )

    def _builtin_childcommand(self, name):
        match name:
            case "container":
                return self.__Container
            case "canvas":
                return self.__Canvas
            case "listbox":
                return self.__Listbox
            case "text":
                return self.__Text
            case "notebook":
                return self.__Notebook
            case "treeview":
                return self.__Treeview
            case "menu":
                return self.__Menu
            case "option_menu":
                return self.__OptionMenu
            case None:
                return self.__none
            case _:
                return name

    def _builtin_deletechildcommand(self, name):
        match name:
            case "canvas_item":
                return self.__CanvasItem
            case "listbox_item":
                return self.__ListboxItem
            case "text_tag":
                return self.__TextTag
            case "treeview_item":
                return self.__TreeviewItem
            case "menu_item":
                return self.__MenuItem
            case "option_menu_value":
                return self.__OptionMenuValue
            case _:
                return name

    # CreateChildCommands
    def __create_CanvasItem(self, w: tkinter.Canvas) -> None:
        w.create_line(0, 0, 0, 0)

    def __create_TextTag(self, w: tkinter.Text) -> None:
        w.tag_add("test", 0)

    def __create_ListboxItem(self, w: tkinter.Listbox) -> None:
        w.insert(0, "item")

    def __create_TreeviewItem(self, w: ttk.Treeview) -> None:
        print("treeview", w)

    def __create_MenuItem(self, w: tkinter.Menu) -> None:
        w.add_command(label="item")

    def __create_OptionMenuItem(self, w: tkinter.OptionMenu) -> None:
        print("optionmenu", w)

    def __create_NotebookFrame(self, w: ttk.Notebook) -> None:
        frm = tkinter.Frame(w)
        w.add(frm)

    def _builtin_createchildcommand(self, name):
        match name:
            case "canvas_item":
                return self.__create_CanvasItem
            case "listbox_item":
                return self.__create_ListboxItem
            case "text_tag":
                return self.__create_TextTag
            case "treeview_item":
                return self.__create_TreeviewItem
            case "menu_item":
                return self.__create_MenuItem
            case "option_menu_item":
                return self.__create_OptionMenuItem
            case "notebook_frame":
                return self.__create_NotebookFrame
            case _:
                return name

    def match(self, name: str) -> bool:
        if isinstance(self.name, list):
            for n in self.name:
                if n == name:
                    return True
        elif name == self.name:
            return True
        return False


widgets = []


def add_widget(
    cls: tkinter.Widget | tuple,
    childcommand: str = None,
    deletecommand=None,
    deletechildcommand=None,
    createchildcommand=None,
    flasharg: str = "background",
    state: str = "normal",
) -> _RegisteredWidget:
    """
    Add a custom widget to the Developer Tools window

    Arguments
    ---
    `cls` - The widget class to match. Can optionally be a tuple of classes to match any. Example: tkinter.Frame or (tkinter.Tk, tkinter.Frame)

    `childcommand` - The command to return the tree view data. Should return something like: [(name:str, cls, haschildren:bool)] if "haschildren" is true it will check for children in this widget

    `deletecommand` - The command to remove this widget. default is `.destroy()`

    `deletechildcommand` - The command to remove children

    `flasharg` - The argument to flash yellow. default: 'background'
    """
    w = _RegisteredWidget(
        cls,
        childcommand,
        deletecommand,
        deletechildcommand,
        createchildcommand,
        flasharg,
        state,
    )
    widgets.insert(0, w)
    return w


def tk_widgets() -> None:
    """Register all tkinter widgets"""
    tk_none = (
        tkinter.Button,
        tkinter.Checkbutton,
        tkinter.Entry,
        tkinter.Label,
        tkinter.Menubutton,
        tkinter.Message,
        tkinter.Radiobutton,
        tkinter.Scale,
        tkinter.Scrollbar,
        tkinter.Spinbox,
    )

    tk_containers = (
        tkinter.Tk,
        tkinter.Toplevel,
        tkinter.Frame,
        tkinter.LabelFrame,
        tkinter.PanedWindow,
    )

    ttk_none = (
        ttk.Button,
        ttk.Checkbutton,
        ttk.Entry,
        ttk.Combobox,
        ttk.Label,
        ttk.Menubutton,
        ttk.Progressbar,
        ttk.Radiobutton,
        ttk.Scale,
        ttk.Scrollbar,
        ttk.Separator,
        ttk.Sizegrip,
        ttk.Spinbox,
        ttk.LabeledScale,
    )

    ttk_containers = (ttk.Frame, ttk.Labelframe, ttk.Panedwindow)

    container = add_widget(tk_containers, "container", state="readonly")
    container.add_prop("background", "color")
    container.add_prop("highlightbackground", "color")
    container.add_prop("highlightcolor", "color")
    container.add_prop("borderwidth", "integer")
    container.add_prop("height", "integer")
    container.add_prop("highlightthickness", "integer")
    container.add_prop("padx", "integer")
    container.add_prop("pady", "integer")
    container.add_prop("width", "integer")
    container.add_prop("cursor", "short")
    # container.add_prop('colormap': '')
    # container.add_prop('relief': _Relief)
    # container.add_prop('takefocus': _TakeFocusValue )

    add_widget(ttk_containers, "container", flasharg=None)
    none = add_widget(tk_none)
    none.add_prop("text", "short", widget=tkinter.Button)

    none.add_prop("activebackground", "color")
    none.add_prop("activeforeground", "color")
    none.add_prop("background", "color")
    none.add_prop("foreground", "color")
    none.add_prop("highlightbackground", "color")
    none.add_prop("highlightcolor", "color")
    none.add_prop("disabledforeground", "color")

    none.add_prop("borderwidth", "integer", from_=0)
    none.add_prop("highlightthickness", "integer", from_=0)
    none.add_prop("padx", "integer", from_=0)
    none.add_prop("pady", "integer", from_=0)
    none.add_prop("underline", "integer", from_=-1)
    none.add_prop("wraplength", "integer", from_=0)
    none.add_prop("repeatdelay", "integer", from_=0)
    none.add_prop("repeatinterval", "integer", from_=0)
    none.add_prop("anchor", "short")  # Enum
    none.add_prop("justify", "short")  # Enum
    none.add_prop("relief", "short")  # Enum

    add_widget(ttk_none, flasharg=None)
    add_widget(
        ttk.Notebook, "notebook", flasharg=None, createchildcommand="notebook_frame"
    )
    add_widget(
        ttk.Treeview,
        "treeview",
        deletechildcommand="treeview_item",
        createchildcommand="treeview_item",
        flasharg=None,
    )
    add_widget(
        (tkinter.OptionMenu, ttk.OptionMenu),
        "option_menu",
        deletechildcommand="option_menu_item",
        createchildcommand="option_menu_item",
    )
    add_widget(
        tkinter.Menu,
        "menu",
        deletechildcommand="menu_item",
        createchildcommand="menu_item",
    )
    add_widget(
        tkinter.Text,
        "text",
        deletechildcommand="text_tag",
        createchildcommand="text_tag",
    )
    add_widget(
        tkinter.Listbox,
        "listbox",
        deletechildcommand="listbox_item",
        createchildcommand="listbox_item",
    )
    add_widget(
        tkinter.Canvas,
        "canvas",
        deletechildcommand="canvas_item",
        createchildcommand="canvas_item",
    )


def ctk_widgets() -> None:
    """Register all customtkinter widgets"""
    if has_customtkinter():
        from customtkinter import (
            CTkButton,
            CTkCheckBox,
            CTkComboBox,
            CTkEntry,
            CTkLabel,
            CTkProgressBar,
            CTkRadioButton,
            CTkScrollbar,
            CTkSlider,
            CTkSwitch,
            CTk,
            CTkToplevel,
            CTkFrame,
            CTkSegmentedButton,
            CTkTabview,
            CTkOptionMenu,
            CTkTextbox,
        )

        def ctk_tabview(w: CTkTabview):
            for name in w._name_list:
                v = w.tab(name)
                yield (name, v, True)

        def ctk_option_menu(w: CTkOptionMenu):
            i = 0
            for v in w.cget("values"):
                yield (v, i, False)
                i += 1

        def ctk_segmentedbtn(w: CTkSegmentedButton):
            i = 0
            for v in w.cget("values"):
                yield (v, i, False)
                i += 1

        def ctk_option_menu_del(w: CTkOptionMenu, data: tuple):
            values = list(w.cget("values"))
            values.remove(data[1])
            w.configure(values=values)

        def ctk_segmentedbtn_del(w: CTkSegmentedButton, data: tuple):
            w.delete(data[1])

        def ctk_tabview_del(w: CTkTabview, data: tuple):
            w.delete(data[1])

        ctk_none = (
            CTkButton,
            CTkCheckBox,
            CTkComboBox,
            CTkEntry,
            CTkLabel,
            CTkProgressBar,
            CTkRadioButton,
            CTkScrollbar,
            CTkSlider,
            CTkSwitch,
        )
        ctk_containers = (CTk, CTkToplevel, CTkFrame, CTkTabview)

        # TODO Fix colors
        none = add_widget(ctk_none, flasharg="fg_color")
        none.add_prop("bg_color", "color")
        # none.add_prop('fg_color', 'color')
        # none.add_prop('hover_color', 'color')
        # none.add_prop('border_color', 'color')
        # none.add_prop('text_color', 'color')
        # none.add_prop('text_color_disabled', 'color')
        # none.add_prop('background_corner_colors', 'color')

        none.add_prop("width", "integer")
        none.add_prop("height", "integer")
        none.add_prop("corner_radius", "integer")
        none.add_prop("border_width", "integer")
        none.add_prop("border_spacing", "integer")
        # none.add_prop('round_width_to_even_numbers', 'checkbox')
        # none.add_prop('round_height_to_even_numbers', 'checkbox')
        none.add_prop("text", "short")
        none.add_prop("state", "short")
        none.add_prop("hover", "checkbox")
        # none.add_prop('compound', 'enum')
        # none.add_prop('anchor', 'enum')

        container = add_widget(ctk_containers, "container", flasharg="fg_color")
        container.add_prop("width", "integer")
        container.add_prop("height", "integer")
        container.add_prop("corner_radius", "integer")
        container.add_prop("border_width", "integer")
        # container.add_prop('bg_color', 'color')
        # container.add_prop('fg_color', 'color')
        # container.add_prop('border_color', 'color')
        # container.add_prop('background_corner_colors', 'color')

        add_widget(
            (CTkOptionMenu, CTkComboBox),
            ctk_option_menu,
            deletechildcommand=ctk_option_menu_del,
            flasharg="fg_color",
        )
        add_widget(
            CTkTextbox, "text", deletechildcommand="text_tag", flasharg="fg_color"
        )
        add_widget(
            CTkSegmentedButton,
            ctk_segmentedbtn,
            deletechildcommand=ctk_segmentedbtn_del,
            flasharg="fg_color",
        )
        add_widget(
            CTkTabview,
            ctk_tabview,
            deletechildcommand=ctk_tabview_del,
            flasharg="fg_color",
        )


def tkp_widgets() -> None:
    """Register all tkinterplus widgets"""
    pass


tk_widgets()
ctk_widgets()
tkp_widgets()


# Crash: Tool > Console > EXIT > Tool (CRASH)
class DeveloperTools(tkinter.Toplevel):
    def __init__(self, master: tkinter.Tk = None):
        super().__init__(master)
        self.title("Developer Tools")

        # Variable
        self.selected = None
        self.COMMAND = tkinter.StringVar()

        # TOP NAV
        self._topnav = ttk.Notebook(self)

        # Widgets
        self._widgets = tkinter.Frame(self._topnav)

        self.widgets = ttk.Treeview(self._widgets, show="tree", columns=("one"))
        scroll = tkinter.Scrollbar(self._widgets, command=self.widgets.yview)
        self.widgets.configure(yscrollcommand=scroll.set)
        self.widgets.grid(row=0, column=0, sticky="nesw")
        scroll.grid(row=0, column=1, sticky=tkinter.NS)

        self._widget_props = ttk.Notebook(self._widgets)

        self.widget_properties = tkinter.Frame(self._widget_props, padx=10, pady=10)
        self.widget_properties.grid(row=0, column=0, sticky="nesw")

        self.widget_binds = tkinter.Frame(self._widget_props)
        tkinter.Label(self.widget_binds, text="binds").pack()
        self.widget_binds.grid(row=0, column=0, sticky="nesw")

        self._widget_props.add(self.widget_properties, text="Properties")
        self._widget_props.add(self.widget_binds, text="Binds")
        self._widget_props.grid(row=1, column=0, sticky="nesw")

        # Responsive
        self._widgets.grid_rowconfigure(0, weight=1)
        self._widgets.grid_columnconfigure(0, weight=1)
        self._widgets.pack(expand=1, fill=tkinter.BOTH)

        # Console
        self._console = tkinter.Frame(self._topnav)

        self.console = ScrolledConsole(self._console)
        self.console.grid(row=0, columnspan=2, column=0, sticky="nesw")
        tkinter.Label(self._console, text="> ").grid(row=1, column=0, sticky=tkinter.W)
        self.command = tkinter.Entry(self._console, textvariable=self.COMMAND)
        self.command.grid(row=1, column=1, sticky=tkinter.EW)

        self._console.grid_columnconfigure(1, weight=1)
        self._console.grid_rowconfigure(0, weight=1)
        self._console.pack(expand=1, fill=tkinter.BOTH)

        # Sources
        self._sources = tkinter.Frame(self._topnav)
        self._sources.pack(expand=1, fill=tkinter.BOTH)

        # Add to notebook
        self._topnav.add(self._widgets, text="Widgets")
        self._topnav.add(self._console, text="Console")
        self._topnav.add(self._sources, text="Sources")
        self._topnav.pack(expand=1, fill=tkinter.BOTH)

        # Binds
        # self.widgets.bind('<Button-3>', lambda e: self.edit(self.widgets))
        self.widgets.bind("<Button-3>", lambda e: self.context_menus(e, self.widgets))
        # self.widgets.bind('<<TreeviewSelect>>', lambda e: self.highlight(self.widgets)) # HOVER
        # self.widgets.bind('<<Double-TreeviewSelect>>', self.on_select_widget)
        self.widgets.bind("<Double-1>", self.on_select_widget)

        self.widgets.bind("<Delete>", lambda e: self.destroy_widget())
        self.widgets.bind("<Control-d>", lambda e: self.deselect())

        self.command.bind("<Return>", lambda e: self.run_command(self.COMMAND.get()))

        self.update_widget_list()
        self.bind_all("<Map>", self.refresh)
        self.bind_all("<Unmap>", self.refresh)

    def run_command(self, command: str) -> None:
        match command:
            case "clear":
                self.console.clear()
            case _:
                exec(command, globals(), locals())
        self.COMMAND.set("")

    def refresh(self, e: tkinter.Event = None) -> None:
        """Update the Developer Tools Window"""
        self.update_widget_list()

    def on_select_widget(self, e: tkinter.Event) -> None:
        for c in self.widget_properties.winfo_children():
            c.destroy()
        sel = self.get_selected(False)
        if sel != None:
            self.selected = self.nametowidget(str(sel[2]))
        if self.selected != None:
            r: _RegisteredWidget = self.find_registered(self.selected)
            if r != None:
                if r.get_props(self.selected):
                    r.render_props(self.widget_properties, self.selected)
        else:
            print("NO SEL")

    def destroy(self) -> None:
        self.unbind_all("<Map>")
        self.unbind_all("<Unmap>")
        super().destroy()

    def update_widget_list(self) -> None:
        """Refresh the widget list"""
        # TODO: Should save all selected/open items so when refreshed it can reselect/open those items
        for i in self.widgets.get_children():
            self.widgets.delete(i)
        children = self.get_children(self.master)
        self._create_widgets(self.widgets, children)

    def get_children(self, master: tkinter.Widget) -> list:
        """Returns all children widgets from the root window"""
        # (type, name, widget, children)
        out = []

        w = self.find_registered(master)
        if w != None:
            if w.childcommand != None:
                children = w.childcommand(master)
                if children != None:
                    for name, cls, children in list(children):
                        c = []
                        if children == True:
                            c = self.get_children(cls)
                        out.append((name, cls, c))

        return out

    def _create_widgets(self, tree: ttk.Treeview, children, parent="") -> None:
        for value, widget, childs in children:
            _parent = tree.insert(
                parent, index=tkinter.END, text=str(value), values=[widget]
            )
            if len(childs) >= 1:
                self._create_widgets(tree, childs, _parent)

    def deselect(self, items: str = None) -> None:
        if items == None:
            for i in self.widgets.selection():
                self.widgets.selection_remove(i)
        self.widgets.selection_remove(items)

    def deselect_all(self) -> None:
        """Dselect all widgets"""
        for i in self.widgets.selection():
            self.widgets.selection_remove(i)

    def get_selected(self, multiple: bool = True) -> list[tkinter.Tk] | tkinter.Tk:
        if multiple:
            return [
                self.master.nametowidget(self.widgets.item(id, "values")[0])
                for id in self.widgets.selection()
            ]
        w = self.get_selected(True)
        return w[0] if len(w) >= 1 else None

    def find_registered(self, widget: str) -> None | _RegisteredWidget:
        global widgets
        for w in widgets:
            if isinstance(widget, str):
                if w.match(widget):
                    return w
            elif isinstance(w.cls, list):
                for ww in w.cls:
                    if isinstance(widget, ww):
                        return w
            elif isinstance(widget, w.cls):
                return w
        return None

    def destroy_widget(self) -> None:
        """
        Remove selected widgets.
        """
        ws = self.get_selected()
        for _w in ws:
            r = self.find_registered(_w[1])
            if r != None:
                if r.deletecommand == None:
                    q = self.master.nametowidget(_w[2])
                    q.destroy()
                else:
                    r.deletecommand(_w)

            else:
                p = self.find_registered(_w[0][0])
                if p != None:
                    if p.deletechildcommand != None:
                        w = self.master.nametowidget(_w[0][1])
                        p.deletechildcommand(w, _w)
                    else:
                        print(f"deletechildcommand not found! {_w}")  # This line debug
                else:
                    print(f"Widget not found! {_w}")  # This line should be error
        self.update_widget_list()

    def context_menus(self, e: tkinter.Event, widget: tkinter.Widget) -> None:
        menu = tkinter.Menu(widget, tearoff=False)
        if isinstance(widget, ttk.Treeview):
            sel = self.get_selected(False)
            if sel != None:
                menu.add_command(label="New", command=self.new)
                menu.add_command(label="Edit", command=self.edit)
                menu.add_command(label="Flash", command=self.flash)
                menu.add_command(
                    label="Delete", foreground="red", command=self.destroy_widget
                )
            else:
                menu.add_command(label="New", command=self.new)

        x = self.winfo_x() + widget.winfo_x()
        y = self.winfo_y() + widget.winfo_y() + 10
        menu.tk_popup(e.x + x, e.y + y)
        menu.grab_release()

    def new(self) -> None:
        """
        Create a new widget from selection.
        """
        w = self.get_selected(False)
        if w is not None:
            rw = self.find_registered(w)
            if rw is not None and rw.createchildcommand is not None:
                rw.createchildcommand(w)
                self.update_widget_list()

    def edit(self) -> None:
        """
        Edit selected widget.
        """
        w = self.get_selected(False)
        if w is not None:
            rw = self.find_registered(w)
            if rw is not None:
                rw.render_props(self.widget_properties, w)

    def flash(self) -> None:
        """
        Flash the selected widgets.
        """
        for w in self.get_selected():
            r = self.find_registered(w)
            if r != None:
                r.flash(w)
