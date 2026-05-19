from tkinter import *
from tkinterplus import add_language
from tkinterplus.experimental import CodeBlock
import json

root = Tk()
root.title("CodeBlock")
root.minsize(500, 500)

add_language("abc.tmLanguage.json")

widget = CodeBlock(root, "abc")

# CODE = {
#     "object": {"string": "some text"},
#     "array": [{"id": 0}, {"id": 1}],
#     "string": "Hello World",
#     "intger": 1,
# }
CODE = {"array": [1, 2, 3, 4]}

# widget.insert(0.0, json.dumps(CODE, indent=4))
content = """a
(
    b
)
x
(
    (
        c
        xyz
    )
)
(
a"""
widget.insert(0.0, content)
widget.pack(expand=True, fill=BOTH)

root.mainloop()
