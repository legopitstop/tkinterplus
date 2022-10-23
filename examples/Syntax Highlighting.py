import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
import tkinter as tk

root = tk.Tk()
root.title('Python Syntax Highlighting')

text = tk.Text(root)
text.pack()

markdown = ic.ColorDelegator()
markdown.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
markdown.idprog = re.compile(r'\s+(\w+)', re.S)

markdown.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#FFFFFF'}

# These five lines are optional. If omitted, default colours are used.
markdown.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#FFFFFF'}
markdown.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': '#FFFFFF'}
markdown.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#FFFFFF'}
markdown.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#FFFFFF'}
markdown.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#FFFFFF'}

ip.Percolator(text).insertfilter(markdown)

root.mainloop()