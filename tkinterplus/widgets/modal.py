from tkinter import CENTER, DISABLED, NORMAL, W, EW, NS, Misc, Tk, StringVar, Frame, Label, Event, Menu
from tkinter.font import Font
from PIL import Image, ImageTk
from _tkinter import TclError
import tkinter
import pyautogui
import re

from .. import TK_CLOSE, TK_ICON, Icon

class Geometry():
    def __init__(self, newGeometry:str=None):
        self.newGeometry = None
        self.width = 1
        self.height = 1
        self.x = CENTER
        self.y = CENTER
        self.configure(newGeometry=newGeometry)

    def configure(self, **kw):
        if 'newGeometry' in kw and kw['newGeometry']!=None:
            if re.match(r'^(\d*x\d*|\+\d*\+\d*|\d*x\d*\+\d*\+\d*)$', kw['newGeometry']):
                self.newGeometry = str(kw['newGeometry'])

                s = self.newGeometry.strip().split('x')
                if len(s) == 2: self.configure(width=s[0], height=re.sub(r'\+.*', '', s[1]))

                p = self.newGeometry.strip().split('+')
                if len(p) == 3: self.configure(x=p[1], y=p[2])
            else: raise TclError('bad geometry specifier "%s"'%kw['newGeometry'])
            
        if 'width' in kw and kw['width']!=None: self.width = int(kw['width'])
        if 'height' in kw and kw['height']!=None: self.height = int(kw['height'])
        if 'minwidth' in kw and kw['minwidth']!=None: self.minwidth = int(kw['minwidth'])
        if 'minheight' in kw and kw['minheight']!=None: self.minheight = int(kw['minheight'])
        if 'maxwidth' in kw and kw['maxwidth']!=None: self.maxwidth = int(kw['maxwidth'])
        if 'maxheight' in kw and kw['maxheight']!=None: self.maxheight = int(kw['maxheight'])
        if 'x' in kw and kw['x']!=None: self.x = int(kw['x'])
        if 'y' in kw and kw['y']!=None: self.y = int(kw['y'])

    def __str__(self):
        return '%sx%s+%s+%s'%(self.width, self.height, self.x, self.y)

class Modal(Misc):
    def __init__(self, master:Tk=None, bg_color:str=None, titlebar_bg_color:str=None, titlebar_fg_color:str=None, delete_window_state=None, hitbox:bool=None):
        # Arguments
        if master is None: master = tkinter._get_temp_root()
        self.visable = False
        self.master = master
        self.bg_color = '#f0f0f0'
        self.titlebar_bg_color = 'white'
        self.titlebar_fg_color = 'black'
        self.delete_window_state = NORMAL
        self.hitbox = True
        self.geo = Geometry()

        self._master_last_width = 0
        self._master_last_height = 0

        self._protocol = {'WM_DELETE_WINDOW': self.hide}
        self._show_commands = []
        self._hide_commands = []
        self._titlevar = StringVar()
        self._container = Frame(master, highlightbackground='black', highlightthickness=1)
        # Icons
        self._CLOSE = Icon(name=TK_CLOSE, color='black')
        self._CLOSE_FOCUS = Icon(name=TK_CLOSE, color='white')
        self._ICON = Icon(name=TK_ICON, size=(20, 20))

        # Widgets
        self._title = None
        self._icon = None
        self._close = None
        self._titlebar = None
        self.frame = Frame(self._container, width=200, height=200, bg=self.bg_color)
        self.frame.grid(row=1,column=0,sticky='nesw')

        self._container.grid_columnconfigure(0, weight=1)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.bind_all('<Escape>', lambda e: self.hide())

        # Default
        self.wm_title('tk')
        self.wm_overrideredirect(False)

        self.configure(
            bg_color=bg_color,
            titlebar_bg_color=titlebar_bg_color,
            titlebar_fg_color=titlebar_fg_color,
            hitbox=hitbox,
            delete_window_state=delete_window_state
        )

        # Arguments for tk
        self.children = self.frame.children
        self.tk = self.frame.tk
        self._w = self.frame._w

    def _get_pos(self, e:Event):
        self.focus_set()
        x0 = self._title.winfo_x() - 28
        y0 = self._title.winfo_y()
        self._x = e.x + x0
        self._y = e.y + y0

        # Change cursor
        cursor = self._container.cget('cursor')
        if cursor!='': self._container.configure(cursor='')

    def _close_btn(self):
        if self.delete_window_state!=DISABLED:
            self._close.configure(bg='#f1707a')

    def _on_close(self, e:Event):
        self._on_leave(e)
        self._protocol['WM_DELETE_WINDOW']()

    def _on_enter(self, e:Event):
        if self.delete_window_state!=DISABLED:
            self._close.configure(bg='#e81123',image=self._CLOSE_FOCUS)
            self._close.bind('<ButtonRelease-1>', self._on_close)

    def _on_leave(self, e:Event):
        if self.delete_window_state!=DISABLED:
            self._close.configure(bg=self.titlebar_bg_color, image=self._CLOSE)
            self._close.unbind('<ButtonRelease-1>')

    def _on_move(self, e:Event):
        """Move the window"""
        x0 = self._container.winfo_x()
        y0 = self._container.winfo_y()
        x = x0 + e.x - self._x
        y = y0 + e.y - self._y
        self.moveto(x, y)

    def _center(self):
        """Return the x and y to place the modal so its in the center of the screen"""
        x=0
        y=0
        if self.winfo_width() <= self.master.winfo_width():
            x0 = self.master.winfo_width() / 2
            x1 = self.winfo_width() / 2
            x = round(x0-x1)

        if self.winfo_height() <= self.master.winfo_height():
            y0 = self.master.winfo_height() / 2
            y1 = self.winfo_height() / 2
            y = round(y0-y1)
        return x, y

    def _move_to_titlebar(self):
        """Move the mouse to the titlebar"""
        self._container.configure(cursor='size') # This may not work on MacOS
        x = self.master.winfo_x() + self._container.winfo_x() + self._titlebar.winfo_width() / 2
        y = self.master.winfo_y() + self._container.winfo_y() + 30 + self._titlebar.winfo_height() / 2
        pyautogui.moveTo(x, y)

    def _menu(self):
        x = self.master.winfo_x() + self._container.winfo_x() + 9
        y = self.master.winfo_y() + self._container.winfo_y() + 60
        menu = Menu(self.frame, tearoff=False)
        menu.add_command(label='Move', command=self._move_to_titlebar)
        menu.add_command(label='Close', font=Font(weight='bold', size=10), command=self._protocol['WM_DELETE_WINDOW'])
        menu.tk_popup(x, y)
        menu.grab_release()

    def _check_hitbox(self, x:int=None, y:int=None, error:bool=False):
        """Checks if the coords are in bounds"""
        result = [x, y]
        if self.hitbox:
            if x!=None:
                x0 = x + self._container.winfo_width()
                if x0!=None and self.master.winfo_width() <= x0:result[0] = None # right
                if x!=None and x <0:result[0] = None # left

            if y!=None:
                y0 = y + self._container.winfo_height()
                if y0!=None and self.master.winfo_height() <= y0:result[1] = None # down
                if y!=None and y <0:result[1] = None # up
        if error:
            if result[0]==None or result[1]==None: raise TclError('out of bounds')

        return result

    def _on_configure(self, e:Event):
        """When the master widget has been configured. Used to trigger on_resize"""
        if e.width!=self._master_last_width:
            self._master_last_width = e.width
            self._on_resize_master(e)
        elif e.height!=self._master_last_height:
            self._master_last_height = e.height
            self._on_resize_master(e)

    def _on_resize_master(self, e:Event):
        """When the master widget has been resized""" # When window gets resized and modal is out of bounds it should stick to that side.
        # X, Y = self._check_hitbox(self.geo.x, self.geo.y)
        # if X==None:
        #     print('STICK left right')
        #     x = self.winfo_x() + self.winfo_width()
        #     self.moveto(x=x)
        # if Y==None:
        #     print('STICK up down')
        #     y = self.winfo_y() + self.winfo_height()
        #     self.moveto(y=y)
        pass

    def moveto(self, x:int=None, y:int=None, error:bool=False):
        """Move the modal to a diffrent place. `int` the pos on the screen. `CENTER` center on the screen. `None` keep in the same pos."""
        cx, cy = self._center()
        if x==CENTER: x = cx
        elif x!=None: x = x
        if y==CENTER: y = cy
        elif y!=None: y = y

        X, Y = self._check_hitbox(x, y, error)
        self.geo.configure(x=X, y=Y) # Save to configure
        self._container.place_configure(x=X, y=Y)

    def update(self):
        """Update with widgets properties"""
        self.frame.update()
        width = self.frame.winfo_width()
        height = self.frame.winfo_height()
        self.geo.configure(width=width, height=height)

    def show(self):
        """Shows the modal"""
        if self.visable==False:
            self.update() 
            # if self.geo.x==None and self.geo.y==None: self.moveto(x=CENTER, y=CENTER)
            # else: self.moveto(x=self.geo.x, y=self.geo.y, error=True)
            self.moveto(x=self.geo.x, y=self.geo.y, error=True)
            self.focus_set()
            self.visable = True
            self.master.bind('<Configure>', self._on_configure)
            for cmd in self._show_commands: cmd(Event())
        return self

    def hide(self):
        """Closes the modal"""
        if self.visable:
            self.master.unbind('<Configure>')
            self._container.lower()
            self._container.place_forget()
            self.visable = False
            for cmd in self._hide_commands: cmd(Event())
        return self
    
    def configure(self, **kw):
        if 'hitbox' in kw and kw['hitbox']!=None: self.hitbox = kw['hitbox']
        if 'bg_color' in kw and kw['bg_color']!=None:
            self.bg_color = kw['bg_color']
            self.frame.configure(bg=self.bg_color)
        if 'titlebar_bg_color' in kw and kw['titlebar_bg_color']!=None:
            self.titlebar_bg_color = kw['titlebar_bg_color']
            self._titlebar.configure(bg=self.titlebar_bg_color)
            self._title.configure(bg=self.titlebar_bg_color)
            self._close.configure(bg=self.titlebar_bg_color)
        if 'titlebar_fg_color' in kw and kw['titlebar_fg_color']!=None:
            self.titlebar_fg_color = kw['titlebar_fg_color']
            self._title.configure(fg=self.titlebar_fg_color)
        if 'delete_window_state' in kw and kw['delete_window_state']!=None:
            self.delete_window_state = kw['delete_window_state']
            if self._close!=None: self._close.configure(state=self.delete_window_state)
        if 'cursor' in kw and kw['cursor']!=None: self.master.configure(cursor=kw['cursor'])    
    config = configure
        
    # Default window
    def winfo_height(self): return self.geo.height
    def winfo_width(self): return self.geo.width
    def winfo_x(self): return self.geo.x
    def winfo_y(self): return self.geo.y

    def bind(self, sequence:str, func, add:bool=False):
        """Bind to this widget at event SEQUENCE a call to function FUNC."""
        if sequence == '<Show>':
            if add: self._show_commands.append(func)
            else: self._show_commands = [func]
        elif sequence == '<Hide>':
            if add: self._hide_commands.append(func)
            else: self._hide_commands = [func]
        else: self.frame.bind(sequence, func, add)
    
    def unbind(self, sequence:str, funcid:str=None):
        """Unbind for this widget for event SEQUENCE the function identified with FUNCID."""
        if sequence == '<Show>':
            if funcid!=None: self._show_commands.remove(funcid)
            else: self._show_commands = []
        elif sequence == '<Hide>':
            if funcid!=None: self._hide_commands.remove(funcid)
            else: self._hide_commands = []
        self.frame.unbind(sequence, funcid)

    def wm_maxsize(self, width:int, height:int):
        """Set max WIDTH and HEIGHT for this widget. If the window is gridded the values are given in grid units. Return the current values if None is given."""
        print('wm_maxsize')
    maxsize = wm_maxsize

    def wm_minsize(self, width:int, height:int):
        """Set min WIDTH and HEIGHT for this widget. If the window is gridded the values are given in grid units. Return the current values if None is given."""
        print('wm_minsize')
    minsize = wm_minsize

    def wm_geometry(self, newGeometry:str=None):
        """Set geometry to NEWGEOMETRY of the form =widthxheight+x+y. Return current value if None is given."""
        if newGeometry!=None:
            self.geo.configure(newGeometry=newGeometry)
            self.frame.configure(width=self.geo.width, height=self.geo.height)
            # self.moveto(x=self.geo.x, y=self.geo.y) TODO

        else: return self.geo
    geometry = wm_geometry
    
    def wm_iconbitmap(self, bitmap:str):
        """Set bitmap for the iconified widget to BITMAP. Return the bitmap if None is given."""
        img = Image.open(bitmap)
        self._photo = ImageTk.PhotoImage(img)
        self._icon.configure(image=self._photo)
        return self
    iconbitmap = wm_iconbitmap

    def wm_protocol(self, name:str, func):
        """Bind function FUNC to command NAME for this widget. Return the function bound to NAME if None is given. NAME could be e.g. "WM_SAVE_YOURSELF" or "WM_DELETE_WINDOW"."""
        self._protocol[name] = func
    protocol = wm_protocol

    def wm_title(self, string:str):
        """Set the title of this widget."""
        self._titlevar.set(str(string))
        return self
    title = wm_title

    def focus_set(self):
        self._container.tkraise()
    focus = focus_set

    def wm_overrideredirect(self, boolean=None):
        if boolean==True: self._titlebar.destroy()
        elif boolean==False:
            self._titlebar = Frame(self._container, height=30, bg=self.titlebar_bg_color)
            # ICON
            self._icon = Label(self._titlebar, image=self._ICON, width=10, height=10, bg=self.titlebar_bg_color)
            self._icon.bind('<Button-1>', lambda e: self._menu())
            self._icon.grid(row=0,column=0,sticky=W, padx=(8,6), pady=(6,8))

            self._title = Label(self._titlebar, textvariable=self._titlevar, anchor=W, bg=self.titlebar_bg_color)
            self._title.bind('<Button-1>', self._get_pos)
            self._title.bind('<Button1-Motion>', self._on_move)
            self._title.grid(row=0,column=1, sticky=EW)

            # CLOSE
            self._close = Label(self._titlebar, image=self._CLOSE, width=19, height=19, bg=self.titlebar_bg_color)
            self._close.bind('<ButtonPress-1>', lambda e: self._close_btn())
            self._close.bind('<Enter>', self._on_enter)
            self._close.bind('<Leave>', self._on_leave)
            self._close.grid(row=0, column=2, sticky=NS)

            self._titlebar.grid(row=0,column=0, sticky=EW)
            self._titlebar.grid_columnconfigure(1, weight=1)
    overrideredirect = wm_overrideredirect

    def destroy(self):
        """Destroy this and all descendant widgets."""
        self._container.destroy()
