from tkinterplus.experimental import Markup, Markdown
import tkinter
import os

PATH = os.path.dirname(os.path.realpath(__file__))

root = tkinter.Tk()
root.title("Markup")
root.minsize(500, 500)


def callback():
    print(widget.get())


md = Markdown()

text = """
# header1
## header2
### header3
#### header4
##### header5
###### header6

Hello World!

**Bold**

*italic*

[example.com](https://example.com)
"""

# widget = Markup(root, format=md)
widget = Markup(root, format=md)
widget.set(text)
# widget.load_file(os.path.join(PATH, 'markup.html'))
widget.grid(row=0, column=0, sticky="nesw")

btn = tkinter.Button(root, text="Show", command=callback)
btn.grid(row=1, column=0, columnspan=2)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.mainloop()
