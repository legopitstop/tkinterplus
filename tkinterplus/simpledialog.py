"""
More simple dialogs
"""

from tkinter import messagebox
import webbrowser

__all__ = ["askopenurl"]


# TODO: Make custom dialog that has buttons
# [open] [copy] [cancel]
def askopenurl(title: str, url: str, **kw) -> bool:
    res = messagebox.askyesno(
        title, f"Do you want to open the external website?\n\n{url}", **kw
    )
    if res:
        webbrowser.open(url)
    return res
