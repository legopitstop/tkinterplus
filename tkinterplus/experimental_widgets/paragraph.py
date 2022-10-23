from tkinter import DISABLED, NORMAL, END, Frame, Tk, Text
import json
import os

from .. import ROOT, FormatVar


#NOTE This widget is still being worked on. Expect issues for missing features!
class Paragraph(Text):
    def __init__(self, master:Tk, variable:FormatVar=None, type:str=None, bg_color:str=None, fg_color:str=None, border_width:int=None, border_color:str=None):
        """Creates a Widget that contains text that can be formatted."""
        self.variable = FormatVar()
        self.state = DISABLED
        self.bg_color = 'black'
        self.fg_color = 'white'
        self.format_data = None # Unknown?
        self.border_width = 1
        self.border_color = 'white'
        super().__init__(master, bg=bg_color, fg=fg_color, borderwidth=self.border_width)

        self.configure(
            state=DISABLED,
            type=type,
            bg_color=bg_color,
            fg_color=fg_color,
            variable=variable,
            border_width=border_width,
            border_color=border_color
        )

    def update(self):
        # Check for variable updates
        def var_to_text(a,b,c):
            self.delete(0.0, END)
            self.insert(0.0, self.variable.get(0.0, END))
        self.variable.trace_add('write', var_to_text)

    def load_document(self, fp):
        """Load the contents of a document"""
        with open(fp) as opn:
            self.delete(0.0, END)
            self.insert(0.0, opn.read())

    def load_format(self, file:str):
        """Load a JSON that contains the format for the chars"""
        with open(file) as opn:
            self.format_data = json.load(opn)

    def format(self):
        """Format the text"""
        if self.format_data!=None:
            print('WORKED')
            # bold = Pattern(self.text, self.format_data, 'markup.bold')
            # bold.indexes()

    def configure(self,**kw):
        if 'variable' in kw and kw['variable']!=None: self.variable = kw['variable']
        if 'border_width' in kw and kw['border_width']!=None:
            self.border_width = kw['border_width']
            super().configure(borderwidth=self.border_width)

        if 'border_color' in kw and kw['border_color']!=None: self.border_color = kw['border_color']
        
        if 'type' in kw and kw['type']!=None:
            self.type = kw['type']
            path = os.path.join(ROOT, 'languages', self.type+'.json')
            if os.path.exists(path): self.load_format(path)
            # else: raise MIMENotFoundError('format not found')

        if 'bg_color' in kw and kw['bg_color']!=None:
            self.bg_color = kw['bg_color']
            super().configure(bg=self.bg_color)
        if 'fg_color' in kw and kw['fg_color']!=None:
            self.fg_color = kw['fg_color']
            super().configure(fg=self.fg_color)
        if 'state' in kw and kw['state']!=None:
            self.state = kw['state']
            super().configure(state=self.state)

        self.update()

    config = configure

    # FormatVar
    def insert(self, index1:float, chars:str):
        self.configure(state=NORMAL)
        super().insert(index1, chars)
        self.configure(state=DISABLED)

    def delete(self, index1:float, index2:float):
        self.configure(state=NORMAL)
        super().delete(index1, index2)
        self.configure(state=DISABLED)

    def get(self, index1:float, index2:float): self.variable.get(index1, index2)