import os
from tkinter import END, NW, Menu, StringVar, Text, Tk, Toplevel, filedialog,PanedWindow

from tkinterplus import ContextMenu, ContextMenuType, Paragraph,ScrollableFrame

LOCAL = os.path.dirname(os.path.realpath(__file__))

class LivePreview():
    def __init__(self):
        self.r = Tk()
        self.r.title('Live Preview')
        self.r.geometry('800x600')

        # Varables
        self.formats = ['markdown','html', 'bbcode', 'wikitext', 'custom']
        self.FORMATS={}
        self.FORMAT='markdown'
        self.FILE=None
        self.SAVED=None

        # Widgets
        pane = PanedWindow(self.r,showhandle=False)

        self.input = Text(self.r,width=50,height=40,bd=2,undo=True)
        pane.add(self.input)

        self.output=Paragraph(self.r,text='',bg='white')
        pane.add(self.output)
        pane.grid(row=0,column=0)

        # Binds
        self.r.bind('<Control-s>',lambda e:self.save())
        self.r.bind('<Control-o>',lambda e:self.open())
        self.input.bind('<KeyRelease>',lambda e:self.bind_update())

        # menu
        menu =Menu(self.r)
        fileMenu = Menu(self.r,tearoff=False)
        fileMenu.add_command(label='Open', command=self.open)
        fileMenu.add_command(label='Save', command=self.save)

        formatMenu = Menu(self.r,tearoff=False)
        for format in self.formats:
            self.FORMATS[format] = StringVar()
            formatMenu.add_checkbutton(label=format,offvalue=False,onvalue=True,variable=self.FORMATS[format],command=lambda: self.change_format(format))
        self.FORMATS['markdown'].set(True)

        menu.add_cascade(label='File',menu=fileMenu)
        menu.add_cascade(label='Format',menu=formatMenu)

        # Context Menu
        context = ContextMenu(self.input)
        context.add_command(label='Open',command=self.open)
        context.add_separator()
        context.add_command(label='Cut',type=ContextMenuType.CUT)
        context.add_command(label='Copy',type=ContextMenuType.COPY)
        context.add_command(label='Paste',type=ContextMenuType.PASTE)
        context.add_separator()
        context.add_command(label='Delete',type=ContextMenuType.DELETE)
        # context.add_command(label='Select All',type=ContextMenuType.SELECT_ALL)
        # context.add_command(label='Undo',type=ContextMenuType.UNDO)
        # context.add_command(label='Redo',type=ContextMenuType.REDO)

        self.r.config(menu=menu)

        # Apply defaults
        self.open(LOCAL+'/default.md')

        # display win
        self.r.mainloop()

    def get_render(self):
        """Returns the format renderer type"""
        if self.FORMAT == 'markdown':
            # return Format(StyleType.MARKDOWN)
            pass
        else:
            print('Invalid format')

    def bind_update(self):
        self.SAVED=False
        self.update()

    def update(self):
        """Updates the output with the text and format"""
        self.output.config(text=self.input.get('0.0',END), format=self.get_render())

        # Update title
        if self.FILE!=None:
            filename = os.path.basename(self.FILE)
            if self.SAVED:
                self.r.title('Live Preview - '+filename)
            else:
                self.r.title('Live Preview - *'+filename)
        else:
            self.r.title('Live Preview')

    def open(self,fp=None):
        """Open and view a file"""
        # Open the file or use the one provided
        if fp==None:
            filetypes= [('Text Documents','.txt .md .html .bbcode'),('Any','*.*')]
            file = filedialog.askopenfilename(defaultextension='.txt',filetypes=filetypes,parent=self.r)
        else:
            file = fp

        # Add doc to Text area
        if file!='':
            self.input.delete('0.0',END)
            self.FILE = file
            self.SAVED=True
            opn = open(file,'r')
            self.input.insert("0.0",opn.read())
            opn.close()
            self.update()
    
    def save(self):
        """Save the input to the same file"""
        wrt = open(self.FILE, 'w')
        wrt.write(self.input.get('0.0',END))
        wrt.close()
        self.SAVED=True
        self.update()

    def change_format(self,format):
        """Change the formatter"""
        print(format)

if __name__=='__main__':
    LivePreview()