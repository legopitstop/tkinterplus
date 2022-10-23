from tkinter import DISABLED, E, END, EW, LEFT, CENTER, NORMAL, RIGHT, INSERT, SEL, SEL_FIRST, SEL_LAST, Event, filedialog, simpledialog, Toplevel, colorchooser, Text, Frame, Tk, PhotoImage, Button
from tkinter.font import Font
from _tkinter import TclError
from enum import Enum
import uuid
import os

from tkinterplus.constants import *

from .. import ROOT, Icon, Footer, StyleType, FormatVar

#NOTE This widget is still being worked on. Expect issues for missing features!
# - Store style as a diffrent varaible for exporting

class FormatText(Frame):
    def __init__(self,master:Tk,format=None, variable:FormatVar=None, controls:bool=True, fg:str=None, bg:str=None, width:int=None, height:int=None, insertbackground:str=None, selectbackground:str=None, selectforeground:str=None, button_bg:str=None, button_fg:str=None, button_activebackground:str=None, button_activeforeground:str=None, button_disabledforeground:str=None, border_width:int=None, border_color:str=None):
        
        self.variable = FormatVar()
        self.fullscreen=False
        self._color='red'

        # Variables
        self.state = NORMAL
        self.format = 'html'
        self.fg = 'black'
        self.bg = 'white'
        self.width = 50
        self.height = 20
        self.insertbackground = 'black'
        self.selectbackground = 'blue'
        self.selectforeground = 'white'
        self.border_width = 1
        self.border_color = 'white'
        self.button_bg = '#f0f0f0'
        self.button_fg = 'black'
        self.button_activebackground = '#f0f0f0'
        self.button_activeforeground = 'black'
        self.button_disabledforeground = 'gray'

        self._fg_style = self.fg
        self._bg_style = self.bg
        
        super().__init__(master, width=self.width, height=self.height)

        # Bold Italic Underlined Strikethrough Blockquote [Paragrapgh, h1,h2,h3,h4,h5,h6, pre] Left Center Right Size Color UnorderedList OrderedList HorizontalLine InsertLink InsertImage
        self.toolbar = Frame(self, bg=self.bg)
        self.toolbar.grid(row=0, column=0, sticky=EW)
        
        self._text = Text(self, bg=self.bg, fg=self.fg, borderwidth=self.border_width, insertbackground=self.insertbackground, selectbackground=self.selectbackground, selectforeground=self.selectforeground)
        self._text.grid(row=1,column=0, sticky='nesw')

        # Binds
        self.bind('<Control-b>', lambda e: self._style(StyleType.BOLD))
        self.bind('<Control-i>', lambda e: self._style(StyleType.ITALIC))
        self.bind('<Control-u>', lambda e: self._style(StyleType.UNDERLINED))

        # Bind cursor movements
        self.bind('<Button-1>', self._update_controls)
        self.bind('<Up>', self._update_controls)
        self.bind('<Down>', self._update_controls)
        self.bind('<Left>', self._update_controls)
        self.bind('<Right>', self._update_controls)
        self.bind('<Home>', self._update_controls)
        self.bind('<End>', self._update_controls)

        # Responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.configure(
            fg=fg,
            bg=bg,
            width=width,
            height=height,
            insertbackground=insertbackground,
            border_width=border_width,
            border_color=border_color,
            selectbackground=selectbackground,
            selectforeground=selectforeground,

            format=format,
            controls=controls,
            variable=variable,
            button_bg=button_bg,
            button_fg=button_fg,
            button_activebackground = button_activebackground,
            button_activeforeground = button_activeforeground,
            button_disabledforeground=button_disabledforeground
        )

    def update(self):
        # Text -> FormatVar
        def text_to_var(e:Event):
            v = self._text.get(0.0, 'end-1c')
            self.variable.set(v)

        self._text.bind('<KeyRelease>', text_to_var)

    def _controls(self):
        # ICONS
        self.ALIGN_LEFT = Icon(ALIGN_LEFT, color=self.button_fg)
        self.ALIGN_CENTER = Icon(ALIGN_CENTER, color=self.button_fg)
        self.ALIGN_RIGHT = Icon(ALIGN_RIGHT, color=self.button_fg)
        self.CODE = Icon(CODE, color=self.button_fg)
        self.EXIT_FULLSCREEN = Icon(EXIT_FULLSCREEN, color=self.button_fg)
        self.BLOCKQUOTE = Icon(BLOCKQUOTE, color=self.button_fg)
        self.BOLD = Icon(BOLD, color=self.button_fg)
        self.CLEAR_FORMAT = Icon(CLEAR_FORMAT, color=self.button_fg)
        self.ITALIC = Icon(ITALIC, color=self.button_fg)
        self.ORDERED_LIST = Icon(ORDERED_LIST, color=self.button_fg)
        self.UNORDERED_LIST = Icon(UNORDERED_LIST, color=self.button_fg)
        self.FOREGROUND_COLOR = Icon(FOREGROUND_COLOR, color=self.fg)
        self.BACKGROUND_COLOR = Icon(BACKGROUND_COLOR, color=self.bg)
        self.UNDERLINED = Icon(UNDERLINED, color=self.button_fg)
        self.FULLSCREEN = Icon(FULLSCREEN, color=self.button_fg)
        self.INSERT_IMAGE = Icon(INSERT_IMAGE, color=self.button_fg)
        self.INSERT_LINK = Icon(INSERT_LINK, color=self.button_fg)
        self.UNLINK = Icon(UNLINK, color=self.button_fg)

        btn = {'fg':self.button_fg, 'bg':self.button_bg, 'activebackground':self.button_activebackground, 'activeforeground':self.button_activeforeground, 'disabledforeground': self.button_disabledforeground}

        self.bold_btn = Button(self.toolbar,image=self.BOLD,command=lambda: self._style(StyleType.BOLD), **btn)
        self.italic_btn = Button(self.toolbar,image=self.ITALIC,command=lambda: self._style(StyleType.ITALIC), **btn)
        self.underlined_btn = Button(self.toolbar,image=self.UNDERLINED,command=lambda: self._style(StyleType.UNDERLINED), **btn)
        self.strikethrough_btn = Button(self.toolbar,text='strikethrough',command=lambda: self._style(StyleType.STRIKETHROUGH), **btn)
        self.blockquote_btn = Button(self.toolbar,image=self.BLOCKQUOTE,command=lambda: self._style(StyleType.BLOCKQUOTE), **btn)
        # Type
        self.align_left_btn = Button(self.toolbar,image=self.ALIGN_LEFT,command=lambda: self._style(StyleType.ALIGN_LEFT),  **btn)
        self.align_center_btn = Button(self.toolbar,image=self.ALIGN_CENTER,command=lambda: self._style(StyleType.ALIGN_RIGHT),  **btn)
        self.align_right_btn = Button(self.toolbar,image=self.ALIGN_RIGHT,command=lambda: self._style(StyleType.ALIGN_RIGHT),  **btn)
        # Size
        self.fg_color_btn = Button(self.toolbar,image=self.FOREGROUND_COLOR,command=lambda: self._style(StyleType.FOREGROUND_COLOR, color=self._fg_style),  **btn)
        self.fg_color_btn.bind('<Button-3>', lambda e: self._changeColor('fg'))
        
        self.bg_color_btn = Button(self.toolbar,image=self.BACKGROUND_COLOR,command=lambda: self._style(StyleType.BACKGROUND_COLOR, color=self._bg_style),  **btn)
        self.bg_color_btn.bind('<Button-3>', lambda e: self._changeColor('bg'))

        self.unordered_list_btn = Button(self.toolbar,image=self.UNORDERED_LIST,command=lambda: self._style(StyleType.UNORDERED_LIST),  **btn)
        self.ordered_list_btn = Button(self.toolbar,image=self.ORDERED_LIST,command=lambda: self._style(StyleType.ORDERED_LIST),  **btn)
        self.insert_link_btn = Button(self.toolbar,image=self.INSERT_LINK,command=lambda: self._style(StyleType.INSERT_LINK),  **btn)
        self.insert_image_btn = Button(self.toolbar,image=self.INSERT_IMAGE,command=lambda: self._style(StyleType.INSERT_IMAGE),  **btn)
        
        self.fullscreen_btn = Button(self.toolbar,image=self.FULLSCREEN,command=lambda: self._fullscreen(), **btn)

        # Geo
        self.bold_btn.grid(row=0,column=0)
        self.italic_btn.grid(row=0,column=1)
        self.underlined_btn.grid(row=0,column=2)
        self.strikethrough_btn.grid(row=0,column=3)
        self.blockquote_btn.grid(row=0,column=4)

        self.align_left_btn.grid(row=0,column=6)
        self.align_center_btn.grid(row=0,column=7)
        self.align_right_btn.grid(row=0,column=8)

        self.fg_color_btn.grid(row=0,column=10)
        self.bg_color_btn.grid(row=0,column=11)
        self.unordered_list_btn.grid(row=0,column=12)
        self.ordered_list_btn.grid(row=0,column=13)
        self.insert_link_btn.grid(row=0,column=14)
        self.insert_image_btn.grid(row=0,column=15)
        self.fullscreen_btn.grid(row=0,column=16,sticky=E)

    def update_style(self, name=None, value=None, style=None):
        """update the style"""
        # remove all tags
        self._text.tag_delete('all')
        self.variable.apply_style(self._text)

    def _changeColor(self,type:str):
        new_color = colorchooser.askcolor(self._color)
        if new_color[1]!=None:
            c = new_color[1]

            if type == 'fg':
                self._fg_style = c
                self.FOREGROUND_COLOR.configure(color=c)
                self.fg_color_btn.configure(image=self.FOREGROUND_COLOR)
            elif type == 'bg':
                self._bg_style = c
                self.BACKGROUND_COLOR.configure(color=c)
                self.bg_color_btn.configure(image=self.BACKGROUND_COLOR)

    def _fullscreen(self):
        def _confirm():
            print('WORKED')
            self._fullscreen()

        if self.fullscreen==True:
            # close
            self.configure(state=NORMAL)
            self.fullscreen_btn.configure(image=self.FULLSCREEN)
            self.fullscreen=False
            self.fullWindow.destroy()
        else:
            # full
            self.configure(state=DISABLED)
            self.fullscreen_btn.configure(image=self.EXIT_FULLSCREEN)
            self.fullscreen=True

            self.fullWindow = Toplevel(self.master)
            self.fullWindow.title('Fullscreen')
            self.fullWindow.protocol('WM_DELETE_WINDOW', self._fullscreen)

            Button(self.fullWindow, text='WORKED').grid(row=0,column=0)

            foot = Footer(self.fullWindow)
            foot.add_button('Save',_confirm)
            foot.add_button('Cancel',self._fullscreen)

    def _update_controls(self, e:Event=None):
        """Update the controls when the user moves the cursor"""
        if self.controls:
            index  = self._text.index(INSERT)
            styles = self.variable.get_style(float(index))
            # print('++ STYLE ++', index)

            # Reset State
            self.bold_btn.configure(state=NORMAL)
            self.italic_btn.configure(state=NORMAL)
            self.underlined_btn.configure(state=NORMAL)
            self.strikethrough_btn.configure(state=NORMAL)
            self.blockquote_btn.configure(state=NORMAL)
            self.align_left_btn.configure(state=NORMAL)
            self.align_center_btn.configure(state=NORMAL)
            self.align_right_btn.configure(state=NORMAL)
            self.unordered_list_btn.configure(state=NORMAL)
            self.ordered_list_btn.configure(state=NORMAL)
            self.insert_link_btn.configure(state=NORMAL)
            self.insert_image_btn.configure(state=NORMAL)

            # Disable
            for s in styles:
                if s.type == StyleType.BOLD: self.bold_btn.configure(state=NORMAL)
                elif s.type == StyleType.ITALIC: self.italic_btn.configure(state=NORMAL)
                elif s.type == StyleType.UNDERLINED: self.underlined_btn.configure(state=NORMAL)
                elif s.type == StyleType.STRIKETHROUGH: self.strikethrough_btn.configure(state=NORMAL)
                elif s.type == StyleType.BLOCKQUOTE: self.blockquote_btn.configure(state=NORMAL)
                elif s.type == StyleType.ALIGN_LEFT: self.align_left_btn.configure(state=NORMAL)
                elif s.type == StyleType.ALIGN_CENTER: self.align_center_btn.configure(state=NORMAL)
                elif s.type == StyleType.ALIGN_RIGHT: self.align_right_btn.configure(state=NORMAL)
                elif s.type == StyleType.UNORDERED_LIST: self.unordered_list_btn.configure(state=NORMAL)
                elif s.type == StyleType.ORDERED_LIST: self.ordered_list_btn.configure(state=NORMAL)
                elif s.type == StyleType.INSERT_LINK: self.insert_link_btn.configure(state=NORMAL)
                elif s.type == StyleType.INSERT_IMAGE: self.insert_image_btn.configure(state=NORMAL)

    def _style(self, format:StyleType, **kw):
        try:
            first = self._text.index(SEL_FIRST)
            last = self._text.index(SEL_LAST)
            self.variable.add_style(float(first), float(last), format, **kw)
            self.update_style()
        except TclError:
            pass

    # Default

    def configure(self, **kw):
        if 'variable' in kw and kw['variable']!=None:
            self.variable = kw['variable']
            self._text.delete(0.0, END)
            self._text.insert(0.0, self.variable.get(0.0, END))

        if 'border_width' in kw and kw['border_width']!=None:
            self.border_width = kw['border_width']
            self._text.configure(borderwidth=self.border_width)

        if 'border_color' in kw and kw['border_color']!=None: self.border_color = kw['border_color']
        if 'button_fg' in kw and kw['button_fg']!=None: self.bordebutton_fgr_color = kw['button_fg']
        if 'button_bg' in kw and kw['button_bg']!=None: self.button_bg = kw['button_bg']
        if 'button_activebackground' in kw and kw['button_activebackground']!=None: self.button_activebackground = kw['button_activebackground']
        if 'button_activeforeground' in kw and kw['button_activeforeground']!=None: self.button_activeforeground = kw['button_activeforeground']
        if 'button_disabledforeground' in kw and kw['button_disabledforeground']!=None: self.button_disabledforeground = kw['button_disabledforeground']

        if 'state' in kw and kw['state']!=None:
            self.state = kw['state']
            self._text.configure(state=self.state)
            
        if 'format' in kw and kw['format']!=None: self.format = kw['format']
        if 'controls' in kw and kw['controls']!=None:
            self.controls = kw['controls']
            if self.controls: self._controls()
        if 'bg' in kw and kw['bg']!=None:
            self.bg = kw['bg']
            self._text.configure(bg=self.bg)
        if 'fg' in kw and kw['fg']!=None:
            self.fg = kw['fg']
            self._text.configure(fg=self.fg)
        if 'insertbackground' in kw and kw['insertbackground']!=None:
            self.insertbackground = kw['insertbackground']
            self._text.configure(insertbackground=self.insertbackground)
        if 'selectbackground' in kw and kw['selectbackground']!=None:
            self.selectbackground = kw['selectbackground']
            self._text.configure(selectbackground=self.selectbackground)
        if 'selectforeground' in kw and kw['selectforeground']!=None:
            self.selectbackground = kw['selectforeground']
            self._text.configure(selectforeground=self.selectforeground)
        if 'width' in kw and kw['width']!=None:
            self.width = kw['width']
            super().configure(width=self.width)
        if 'height' in kw and kw['height']!=None:
            self.height = kw['height']
            super().configure(height=self.height)
        
        self.update()
        
    config = configure

    def bind(self, sequence:str, func, add:bool=False):
        """Bind to this widget at event SEQUENCE a call to function FUNC."""
        self._text.bind(sequence, func, add)
        
    def unbind(self, sequence:str, funcid:str=None):
        """Unbind for this widget for event SEQUENCE the function identified with FUNCID."""
        self._text.unbind(sequence, funcid)
    
    # FormatVar
    def insert(self, index1:float, chars:str): self.variable.insert(index1, chars)
    def get(self, index1:float, index2:float): self.variable.get(index1, index2)
    def delete(self, index1:float, index2:float): self.variable.delete(index1, index2)