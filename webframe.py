from tkinter import *
from tkinterplus.experimental import WebFrame

root = Tk()
root.title('WebFrame')
root.minsize(100,100)

root.config(bg='black')

ctk_tabs = WebFrame(root, src='https://example.com')
ctk_tabs.pack(expand=1, fill='both')

root.mainloop()
