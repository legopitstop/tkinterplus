from tkinter import *
from tkinterplus.experimental import CodeBlock
import json

root = Tk()
root.title('CodeBlock')
root.minsize(500,500)

widget = CodeBlock(root, 'json')

CODE = {
    'object': {
        'string': 'some text'
    },
    'array': [
        {
            'id': 0
        },
        {
            'id': 1
        }
    ],
    'string': 'Hello World',
    'intger': 1
}

widget.insert(0.0, json.dumps(CODE, indent=4))
widget.pack(expand=True, fill=BOTH)

root.mainloop()