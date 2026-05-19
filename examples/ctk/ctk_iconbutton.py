from customtkinter import CTk, CTkFrame, CTkLabel
from tkinterplus.ctk import CTkIconButton
import os


def main():

    LOCAL = os.path.dirname(os.path.realpath(__file__))

    root = CTk()
    root.title("test")
    root.minsize(400, 400)

    def tab(name: str):
        home_frm.forget()
        apps_frm.forget()
        gaming_frm.forget()
        movies_frm.forget()
        library_frm.forget()
        home_btn.configure(state="normal")
        apps_btn.configure(state="normal")
        gaming_btn.configure(state="normal")
        movies_btn.configure(state="normal")
        library_btn.configure(state="normal")

        match name:
            case "home":
                home_frm.grid(row=0, column=1, sticky="nesw")
                home_btn.configure(state="disabled")
            case "apps":
                apps_frm.grid(row=0, column=1, sticky="nesw")
                apps_btn.configure(state="disabled")
            case "gaming":
                gaming_frm.grid(row=0, column=1, sticky="nesw")
                gaming_btn.configure(state="disabled")
            case "movies":
                movies_frm.grid(row=0, column=1, sticky="nesw")
                movies_btn.configure(state="disabled")
            case "library":
                library_frm.grid(row=0, column=1, sticky="nesw")
                library_btn.configure(state="disabled")
            case _:
                print("None!")

    nav = CTkFrame(root, fg_color="#202020")

    # 48
    home_btn = CTkIconButton(nav, icon="home", text="Home", command=lambda: tab("home"))
    apps_btn = CTkIconButton(nav, icon="home", text="Apps", command=lambda: tab("apps"))
    gaming_btn = CTkIconButton(
        nav, icon="home", text="Gaming", command=lambda: tab("gaming")
    )
    movies_btn = CTkIconButton(
        nav, icon="home", text="Movies & TV", command=lambda: tab("movies")
    )
    library_btn = CTkIconButton(
        nav, icon="home", text="Library", command=lambda: tab("library")
    )
    help_btn = CTkIconButton(nav, icon="help", text="Help", command=lambda: tab("help"))

    home_btn.grid(row=0, column=0, sticky="ew")
    apps_btn.grid(row=1, column=0, sticky="ew")
    gaming_btn.grid(row=2, column=0, sticky="ew")
    movies_btn.grid(row=3, column=0, sticky="ew")
    library_btn.grid(row=4, column=0, sticky="ews")
    help_btn.grid(row=5, column=0, sticky="ews")

    nav.grid(row=0, column=0, sticky="ns")
    nav.grid_rowconfigure(4, weight=1)

    home_frm = CTkFrame(root)
    CTkLabel(home_frm, text="Home").pack()

    apps_frm = CTkFrame(root)
    CTkLabel(apps_frm, text="Apps").pack()

    gaming_frm = CTkFrame(root)
    CTkLabel(gaming_frm, text="Gaming").pack()

    movies_frm = CTkFrame(root)
    CTkLabel(movies_frm, text="Movies & TV").pack()

    library_frm = CTkFrame(root)
    CTkLabel(library_frm, text="Library").pack()

    tab("home")

    # Responsive
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()
