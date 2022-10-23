from tkinter import ACTIVE, DISABLED, E, NORMAL, W, Tk, Button

from .. import KEYBOARD_ARROW_LEFT, KEYBOARD_ARROW_RIGHT, Icon, Picture

RUNNING = 'running'
IDLE = 'idle'
STOP = 'stop'

#NOTE This widget is still being worked on. Expect issues for missing features!
class Slideshow(Picture):
    def __init__(self, master:Tk, images:list=None, buttons:bool=None, button:str=None, activecolor:str=None, disabledcolor:str=None, width:int=None, height:int=None, state:str=None, fg:str=None, bg:str=None):
        """Create a slideshow of images."""
        super().__init__(master)
        self._index = 0
        self._max = 0
        self.time = 0
        self.loop_state = IDLE
        self.buttons = True
        self.button = 'black'
        self.activecolor = 'white'
        self.disabledcolor = 'gray'
        self.state = NORMAL

        
        self.LEFT = Icon(KEYBOARD_ARROW_LEFT, (45,45), self.button)
        self.RIGHT = Icon(KEYBOARD_ARROW_RIGHT, (45, 45), self.button)
        
        self.LEFT_ACTIVE = Icon(KEYBOARD_ARROW_LEFT, (45,45), self.activecolor)
        self.RIGHT_ACTIVE = Icon(KEYBOARD_ARROW_RIGHT, (45, 45), self.activecolor)
        
        self.LEFT_DISABLED = Icon(KEYBOARD_ARROW_LEFT, (45,45), self.disabledcolor)
        self.RIGHT_DISABLED = Icon(KEYBOARD_ARROW_RIGHT, (45, 45), self.disabledcolor)

        self.images = []

        self.configure(
            images=images,
            buttons=buttons,

            width=width,
            height=height,
            fg=fg,
            bg=bg
        )

    def next(self):
        """Show the next picture"""
        if self._index >= self._max-1: self._index=0
        else: self._index+=1
        self._update()

    def previous(self):
        """Show the previous picture"""
        if self._index <= 0: self._index=self._max-1
        else: self._index-=1
        self._update()

    def _update(self):
        """Show the picture"""
        try: super().configure(image=self.images[self._index])
        except IndexError: print('INDEX ERROR')

    def _update_buttons(self):
        """Update the buttons"""
        if self.buttons==True:
            if self.state == NORMAL:
                self.itemconfigure('L_BTN', image=self.LEFT)
                self.itemconfigure('R_BTN', image=self.RIGHT)
            elif self.state == ACTIVE:
                self.itemconfigure('L_BTN', image=self.LEFT_ACTIVE)
                self.itemconfigure('R_BTN', image=self.RIGHT_ACTIVE)
            elif self.state == DISABLED:
                self.itemconfigure('L_BTN', image=self.LEFT_DISABLED)
                self.itemconfigure('R_BTN', image=self.RIGHT_DISABLED)

    def _active_button(self, type):
        self.state = ACTIVE
        self._update_buttons()
        if type == 'L':
            self.previous()
        elif type == 'R':
            self.next()

    def _normal_button(self):
        self.state = NORMAL
        self._update_buttons()

    def _create_buttons(self):
        self.delete('BUTTONS')
        
        if self.buttons==True:
            self.create_image(5, self.height/2, image=self.LEFT, anchor=W, tags=['BUTTONS', 'L_BTN'])
            self.create_image(self.width, self.height/2, image=self.RIGHT, anchor=E, tags=['BUTTONS', 'R_BTN'])

            if self.state != DISABLED:
                self.tag_bind('L_BTN', '<Button-1>', lambda e: self._active_button('L'))
                self.tag_bind('R_BTN', '<Button-1>', lambda e: self._active_button('R'))
                
                self.tag_bind('L_BTN', '<ButtonRelease>', lambda e: self._normal_button())
                self.tag_bind('R_BTN', '<ButtonRelease>', lambda e: self._normal_button())
            else:
                self.tag_unbind('L_BTN', '<Button-1>')
                self.tag_unbind('R_BTN', '<Button-1>')

            self._update_buttons()

    def configure(self, **kw):
        if 'images' in kw:
            self.images = kw['images']
            self._max = len(kw['images'])
            self._update()


        if 'fg' in kw and kw['fg']!=None: super().configure(fg=kw['fg'])
        if 'bg' in kw and kw['bg']!=None: super().configure(bg=kw['bg'])
        if 'width' in kw and kw['width']!=None: super().configure(width=kw['width'])
        if 'height' in kw and kw['height']!=None: super().configure(height=kw['height'])
        if 'state' in kw and kw['stae']!=None:  self.state = kw['state']

        if 'buttons' in kw and kw['buttons']!=None:
            self.buttons = kw['buttons']
            self._create_buttons()


        if 'button' in kw and kw['button']!=None:
            self.button = kw['button']
            self.LEFT.configure(color=self.button)
            self.RIGHT.configure(color=self.button)
            
        if 'activecolor' in kw and kw['activecolor']!=None:
            self.activecolor = kw['activecolor']
            self.LEFT_ACTIVE.configure(color=self.activecolor)
            self.RIGHT_ACTIVE.configure(color=self.activecolor)
            
        if 'disabledcolor' in kw and kw['disabledcolor']!=None:
            self.disabledcolor = kw['disabledcolor']
            self.LEFT_DISABLED.configure(color=self.disabledcolor)
            self.RIGHT_DISABLED.configure(color=self.disabledcolor)

        if 'state' in kw and kw['state']!=None:
            self.state = kw['state']
            self._update_buttons()

    config = configure

    # Auto loop
    def _next(self):
        """internal function"""
        self.loop_state = IDLE
        self.next()
        self._loop()

    def _loop(self):
        """internal function"""
        if self.loop_state==IDLE: 
            self.after(self.time, self._next)
            self.loop_state = RUNNING

    def start(self, seconds:float=10):
        """Flips  through all the images"""
        if seconds > 0:
            self.time = int(seconds*1000)
            self.loop_state = IDLE
            self._loop()
        else:
            raise ValueError('Time must be more than 0')

    def stop(self):
        """Stops flipping through all the images."""
        self.loop_state = STOP
