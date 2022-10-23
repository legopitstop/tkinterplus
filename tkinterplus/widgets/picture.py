from tkinter import ANCHOR, NW, CENTER, S, Canvas, Tk, StringVar
from tkinter.font import nametofont
from PIL import Image, ImageTk
import os

from .. import ROOT

class Picture(Canvas):
    def __init__(self, master:Tk, image:Image=None, width:int=None, height:int=None, text:str=None, fg:str=None, bg:str=None, textvariable:StringVar=None):
        """Display an image on the window"""
        super().__init__(master, bd=0, highlightthickness=0)
        self.image = Image.open(os.path.join(ROOT, 'assets', 'images', 'missing.png'))
        self.width = None
        self.height = None
        self.text = None
        self.textvariable = StringVar()
        self.fg = 'black'
        self.bg = '#f0f0f0'

        self.configure(
            image=image,
            width=width,
            height=height,
            text=text,
            fg=fg,
            bg=bg,
            textvariable=textvariable
        )

    def _update_text(self, a=None, b=None, c=None):
        self.text = self.textvariable.get()
        self.itemconfigure('TEXT', text=self.text)

    def update(self):
        # Clear canvas to redraw
        self.delete('IMAGE')
        self.delete('TEXT')

        # Resize image
        if self.width == None: self.width = 1
        if self.height == None: self.height = 1
        self.imagetk = ImageTk.PhotoImage(self.image.resize((self.width, self.height), Image.NEAREST))
        self.create_image(0,0,image=self.imagetk,anchor=NW,tag='IMAGE')
        self.tag_lower('IMAGE')

        if self.text!=None:
            self.create_text(self.width/2, self.height+20, text=self.text, fill=self.fg, justify=CENTER, anchor=S, tag='TEXT')

            # Get the height of the font
            text = self.itemcget('TEXT', 'font')
            if text == 'TkDefaultFont':
                font = nametofont(text)
                text_height = font.actual('size') * 2
            else:
                print('Unknown')
                text_height = 20

        else: text_height = 0

        # Update canvas dimentions
        super().configure(width=self.width, height=self.height + text_height)

    def configure(self,**kw):
        """Modify the widget"""
        if 'image' in kw and kw['image']!=None:
            self.image = kw['image']
            if self.width==None:self.width = self.image.width
            if self.height==None:self.height = self.image.height

        if 'text' in kw and kw['text']!=None: self.text = kw['text']
        if 'textvariable' in kw and kw['textvariable']!=None:
            self.textvariable = kw['textvariable']
            self.text = self.textvariable.get()
            self.textvariable.trace_add('write', self._update_text)

        if 'width' in kw and kw['width']!=None:self.width = kw['width']
        if 'height' in kw and kw['height']!=None:self.height = kw['height']

        if 'fg' in kw and kw['bg']!=None:
            self.bg = kw['bg']
            super().configure(bg=self.bg)
        if 'fg' in kw and kw['fg']!=None:
            self.fg = kw['fg']
            self.itemconfigure('TEXT', fill=self.fg)

        self.update()

        

    config = configure
