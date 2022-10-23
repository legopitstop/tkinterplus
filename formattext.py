from tkinter import END, EW, Tk, Button
from tkinterplus import FormatText, FormatVar, StyleType

root = Tk()
root.minsize(500,500)

def export():
    print(var.lines)
    print(var.styles)

var = FormatVar()
var.insert(0.0, 'Bold')
var.add_style(0.0, END, StyleType.BOLD)

widget = FormatText(root, variable=var)
widget.grid(row=0,column=0, sticky='nesw')

# widget1 = Paragraph(root, variable=var)
# widget1.grid(row=0,column=1, sticky=EW)

btn = Button(root, text='Export', command=export)
btn.grid(row=1, column=0, columnspan=2)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.mainloop()