from tkinter import ttk
from tkinter import scrolledtext
from tkinter import simpledialog
from tkinterplus import has_customtkinter, DeveloperTools

# import tests.ctk.ctk_iconbutton as ctk_iconbutton
import tkinter


def main():

    # Add widgets to DeveloperTools
    # add_widget(Treeview)

    root = tkinter.Tk()
    root.title("Developer Tools")
    root.minsize(500, 500)

    global win
    win = None

    def dev():
        global win
        win = DeveloperTools(root)

    def ctk_iconbutton(e: tkinter.Event):
        return e

    root.bind("<Control-U>", lambda e: dev())  # Control-Shift-u
    root.bind_all("<Control-s>", ctk_iconbutton)  # Control-Shift-u

    # Variables

    VALUES = ["item1", "item2", "item3", "item4", "item5"]

    BUTTON = tkinter.StringVar()
    BUTTON.set("Button")
    CHECKBUTTON = tkinter.StringVar()
    CHECKBUTTON.set("CheckButton")
    ENTRY = tkinter.StringVar()
    ENTRY.set("Entry")
    LABEL = tkinter.StringVar()
    LABEL.set("Label")
    MENUBUTTON = tkinter.StringVar()
    MENUBUTTON.set("Menubutton")
    MESSAGE = tkinter.StringVar()
    MESSAGE.set("Message")
    SCALE = tkinter.DoubleVar()
    SCALE.set("Scale")
    OPTION_MENU = tkinter.StringVar()
    OPTION_MENU.set("OptionMenu")
    TEXT = tkinter.StringVar()
    TEXT.set("Text")
    SPINBOX = tkinter.StringVar()
    SPINBOX.set("Spinbox")
    COMBOBOX = tkinter.StringVar()
    COMBOBOX.set("Combobox")
    PROGRESSBAR = tkinter.IntVar()
    PROGRESSBAR.set(50)

    RADIOBUTTON = tkinter.BooleanVar(value=True)
    CHECKBUTTON = tkinter.BooleanVar(value=True)

    # Widgets
    tkinter.Button(root, text="Tools", command=dev).pack()
    # ctk_iconbutton.CTkButton(root, text='Tools', command=dev).pack()
    ttk.Button(root, text="Tools", command=dev).pack()

    tk_menu = tkinter.Menu(root, tearoff=False)
    for v in VALUES:
        tk_menu.add_command(label=v)

    root.configure(menu=tk_menu)

    book = ttk.Notebook(root)

    # tkinter.Button
    # tkinter.Canvas
    # tkinter.Checkbutton
    # tkinter.Entry
    # tkinter.Frame
    # tkinter.Label
    # tkinter.Listbox
    # tkinter.Menu
    # tkinter.Menubutton
    # tkinter.Message
    # tkinter.Radiobutton
    # tkinter.Scale
    # tkinter.Scrollbar
    # tkinter.Text
    # tkinter.OptionMenu
    # tkinter.LabelFrame
    TK = tkinter.Frame(book)
    tk_button = tkinter.Button(TK, textvariable=BUTTON)
    tk_button.grid(row=0, column=0)

    tk_canvas = tkinter.Canvas(TK)
    tk_canvas.create_line(0, 0, 100, 100)
    tk_canvas.create_line(0, 100, 100, 0)
    tk_canvas.grid(row=1, column=0)

    tk_checkbutton = tkinter.Checkbutton(
        TK, variable=CHECKBUTTON, textvariable=CHECKBUTTON
    )
    tk_checkbutton.grid(row=2, column=0)

    tk_entry = tkinter.Entry(TK, textvariable=ENTRY)
    tk_entry.grid(row=3, column=0)

    tk_frame = tkinter.Frame(TK, bg="red", width=25, height=25)
    tkinter.Label(tk_frame, text="Frame").pack()
    tk_frame.grid(row=4, column=0)

    tk_label = tkinter.Label(TK, textvariable=LABEL)
    tk_label.grid(row=0, column=1)

    tk_listbox = tkinter.Listbox(TK)
    for v in VALUES:
        tk_listbox.insert("end", v)
    tk_listbox.grid(row=1, column=1)

    tk_menubutton = tkinter.Menubutton(TK, textvariable=MENUBUTTON, menu=tk_menu)
    tk_menubutton.grid(row=2, column=1)

    tk_message = tkinter.Message(TK, textvariable=MESSAGE)
    tk_message.grid(row=3, column=1)

    tk_radiobutton = tkinter.Radiobutton(
        TK, variable=RADIOBUTTON, textvariable=RADIOBUTTON
    )
    tk_radiobutton.grid(row=4, column=1)

    tk_scale = tkinter.Scale(TK, variable=SCALE)
    tk_scale.grid(row=0, column=2)

    tk_scrollbar = tkinter.Scrollbar(TK)
    tk_scrollbar.grid(row=1, column=2)

    tk_text = tkinter.Text(TK)
    for v in VALUES:
        tk_text.insert("end", v + "\n", "tag")
    tk_text.tag_configure("tag", background="yellow")
    tk_text.grid(row=2, column=2)

    tk_optionmenu = tkinter.OptionMenu(TK, OPTION_MENU, *VALUES)
    tk_optionmenu.grid(row=3, column=2)

    tk_labelframe = tkinter.LabelFrame(TK, text="LabelFrame", bg="red")
    tkinter.Label(tk_labelframe, text="LabelFrame").pack()
    tk_labelframe.grid(row=4, column=2)

    tk_spinbox = tkinter.Spinbox(TK, textvariable=SPINBOX, bg="red")
    tkinter.Label(tk_spinbox, text="LabelFrame").pack()
    tk_spinbox.grid(row=0, column=3)

    tk_paned_window = tkinter.PanedWindow(TK, bg="red")
    tkinter.Label(tk_paned_window, text="Panedwindow").pack()
    tk_paned_window.grid(row=0, column=3)

    # ttk.Button
    # ttk.Checkbutton
    # ttk.Entry
    # ttk.Combobox
    # ttk.Frame
    # ttk.Label
    # ttk.LabelFrame
    # ttk.Menubutton
    # ttk.Notebook
    # ttk.PanedWindow
    # ttk.Progressbar
    # ttk.Radiobutton
    # ttk.Scale
    # ttk.Scrollbar
    # ttk.Separator
    # ttk.Sizegrip
    # ttk.Spinbox
    # ttk.Treeview
    # ttk.LabeledScale
    # ttk.OptionMenu
    TTK = ttk.Frame(book)

    ttk_button = ttk.Button(TTK, textvariable=BUTTON)
    ttk_button.grid(row=0, column=0)

    ttk_checkbutton = ttk.Checkbutton(
        TTK, variable=CHECKBUTTON, textvariable=CHECKBUTTON
    )
    ttk_checkbutton.grid(row=1, column=0)

    ttk_entry = ttk.Entry(TTK, textvariable=ENTRY)
    ttk_entry.grid(row=2, column=0)

    ttk_combobox = ttk.Combobox(TTK, textvariable=COMBOBOX)
    ttk_combobox.grid(row=3, column=0)

    ttk_frame = ttk.Frame(TTK)
    ttk.Label(ttk_frame, text="LabelFrame").pack()
    ttk_frame.grid(row=4, column=0)

    ttk_label = ttk.Label(TTK, textvariable=LABEL)
    ttk_label.grid(row=0, column=1)

    ttk_menubutton = ttk.Menubutton(TTK, textvariable=MENUBUTTON, menu=tk_menu)
    ttk_menubutton.grid(row=1, column=1)

    ttk_progressbar = ttk.Progressbar(TTK, variable=PROGRESSBAR)
    ttk_progressbar.grid(row=2, column=1)

    ttk_radiobutton = ttk.Radiobutton(
        TTK, variable=RADIOBUTTON, textvariable=RADIOBUTTON
    )
    ttk_radiobutton.grid(row=3, column=1)

    ttk_scale = ttk.Scale(TTK, variable=SCALE)
    ttk_scale.grid(row=4, column=1)

    ttk_scrollbar = ttk.Scrollbar(TTK)
    ttk_scrollbar.grid(row=0, column=2)

    ttk_seperator = ttk.Separator(TTK)
    ttk_seperator.grid(row=1, column=2)

    ttk_sizegrip = ttk.Sizegrip(TTK)
    ttk_sizegrip.grid(row=2, column=2)

    ttk_spinbox = ttk.Spinbox(TTK, textvariable=SPINBOX)
    ttk_spinbox.grid(row=3, column=2)

    ttk_treeview = ttk.Treeview(TTK)
    for i in VALUES:
        ttk_treeview.insert("", "end", text=i)
    ttk_treeview.grid(row=4, column=2)

    ttk_labeled_scale = ttk.LabeledScale(TTK, variable=SCALE)
    ttk_labeled_scale.grid(row=0, column=3)

    ttk_option_menu = ttk.OptionMenu(TTK, OPTION_MENU, *VALUES)
    ttk_option_menu.grid(row=1, column=3)

    ttk_option_menu = ttk.Labelframe(
        TTK,
        text="LabelFrame",
    )
    ttk_option_menu.grid(row=2, column=3)

    ttk_option_menu = ttk.Panedwindow(TTK)
    ttk.Label(ttk_option_menu, text="Panedwindow").pack()
    ttk_option_menu.grid(row=3, column=3)

    # tkinter.Toplevel
    # simpledialog.askinteger
    # simpledialog.askfloat
    # simpledialog.askstring
    # scrolledtext.ScrolledText
    def toplevel():
        toplevel = tkinter.Toplevel(root)
        tkinter.Button(toplevel, text="something").pack()

    MISC = tkinter.Frame(book)
    tkinter.Button(MISC, text="toplevel", command=toplevel).grid(row=0, column=0)
    tkinter.Button(
        MISC,
        text="askinteger",
        command=lambda: simpledialog.askinteger("title", "prompt", parent=root),
    ).grid(row=1, column=0)
    tkinter.Button(
        MISC,
        text="askfloat",
        command=lambda: simpledialog.askfloat("title", "prompt", parent=root),
    ).grid(row=2, column=0)
    tkinter.Button(
        MISC,
        text="askstring",
        command=lambda: simpledialog.askstring("title", "prompt", parent=root),
    ).grid(row=3, column=0)

    ScrolledText = scrolledtext.ScrolledText(MISC)
    ScrolledText.tag_configure("name", background="yellow")
    ScrolledText.insert("end", "Something", "name")
    ScrolledText.grid(row=4, column=0)

    book.add(TK, text="tk")
    book.add(TTK, text="ttk")
    book.add(MISC, text="misc")

    # Only load customtkinter widget if customtkinter module is found
    if has_customtkinter():
        CTK = ctk_iconbutton.CTkFrame(book)

        def ctk_toplevel():
            ctk_toplevel = ctk_iconbutton.CTkToplevel()
            ctk_iconbutton.CTkLabel(ctk_toplevel, text="CTkToplevel").pack()

        ctk_button = ctk_iconbutton.CTkButton(CTK, textvariable=BUTTON)
        ctk_button.grid(row=0, column=0)

        ctk_check_box = ctk_iconbutton.CTkCheckBox(CTK, variable=CHECKBUTTON)
        ctk_check_box.grid(row=1, column=0)

        ctk_combo_box = ctk_iconbutton.CTkComboBox(
            CTK, variable=COMBOBOX, values=VALUES
        )
        ctk_combo_box.grid(row=2, column=0)

        ctk_entry = ctk_iconbutton.CTkEntry(CTK, textvariable=ENTRY)
        ctk_entry.grid(row=3, column=0)

        ctk_frame = ctk_iconbutton.CTkFrame(CTK)
        ctk_iconbutton.CTkLabel(ctk_frame, text="CTkFrame").pack()
        ctk_frame.grid(row=4, column=0)

        ctk_label = ctk_iconbutton.CTkLabel(CTK, textvariable=LABEL)
        ctk_label.grid(row=0, column=1)

        ctk_option_menu = ctk_iconbutton.CTkOptionMenu(CTK, values=VALUES)
        ctk_option_menu.grid(row=1, column=1)

        ctk_progress_bar = ctk_iconbutton.CTkProgressBar(CTK, variable=PROGRESSBAR)
        ctk_progress_bar.grid(row=2, column=1)

        ctk_radio_button = ctk_iconbutton.CTkRadioButton(CTK)
        ctk_radio_button.grid(row=3, column=1)

        ctk_scrollbar = ctk_iconbutton.CTkScrollbar(CTK)
        ctk_scrollbar.grid(row=4, column=1)

        ctk_segmented_button = ctk_iconbutton.CTkSegmentedButton(CTK, values=VALUES)
        ctk_segmented_button.grid(row=0, column=2)

        ctk_slider = ctk_iconbutton.CTkSlider(CTK)
        ctk_slider.grid(row=1, column=2)

        ctk_switch = ctk_iconbutton.CTkSwitch(CTK, variable=CHECKBUTTON)
        ctk_switch.grid(row=2, column=2)

        ctk_tabview = ctk_iconbutton.CTkTabview(CTK)
        for i in VALUES:
            w = ctk_tabview.add(i)
            ctk_iconbutton.CTkLabel(w, text=i).pack()
        ctk_tabview.grid(row=3, column=2)

        ctk_textbox = ctk_iconbutton.CTkTextbox(CTK)
        ctk_textbox.insert("end", TEXT.get(), "tag")
        ctk_textbox.grid(row=4, column=2)

        book.add(CTK, text="ctk")

    book.pack(expand=1, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
