import tkinter
from PIL import Image, ImageTk

class OwlImage():
    def __init__(self, id:int, image:Image, text:str=None):
        self.id = id
        self.image = None
        self.text = None

        print(image.__class__.__name__)
        self.configure(
            image=image,
            text=text
        )
    def photo(self, width:int=None, height:int=None):
        """Returns the PhotoImage for tkinter"""
        print(width, height)
        _temp = self.image.resize((width, height))
        self.__photo = ImageTk.PhotoImage(_temp)
        return self.__photo

    def configure(self, **kw):
        if 'image' in kw and kw['image']!=None: self.image = kw['image']
        if 'text' in kw and kw['text']!=None: self.text = kw['text']

class OwlCarousel(tkinter.Frame):
    def __init__(self, master:tkinter.Tk, bg:str=None, fg:str=None, nav:bool=None, dots:bool=None, items:int=None, loop:bool=None, navText:tuple=None, autoplay: bool=None, autoplayTimeout:int=None):
        super().__init__(master)
        self.nav = True
        self.dots = True
        self.items = 1
        self.loop = True
        self.navText = ('<', '>')
        self.autoplay = False
        self.autoplayTimeout = 3000
        self.bg = '#f0f0f0'
        self.fg ='black'

        self.images = []

        # Widgets
        self.canvas = tkinter.Canvas(self, bg=self.bg)
        self.canvas.create_line(0,0, 100,100, fill='red')
        self.canvas.pack(expand=1, fill=tkinter.BOTH)

        self.configure(
            nav=nav,
            dots=dots,
            items=items,
            loop=loop,
            navText=navText,
            autoplay=autoplay,
            autoplayTimeout=autoplayTimeout,
            bg=bg,
            fg=fg
        )

    # unique methods

    def add_image(self, image:Image, text:str=None):
        """Add a new image to carousel"""
        img = OwlImage(len(self.images), image, text)
        self.images.append(img)
        return img
    
    def remove_image(self, index:int):
        """Remove image from carousel"""
        if isinstance(index, OwlImage): return self.images.pop(index.id)
        else: return self.images.pop(index)

    def insert_image(self, index:int, image:Image, text:str=None):
        """insert image to carousel"""
        img = OwlImage(index, image, text)
        self.images.insert(index, img)
        return img

    def get_image(self, index:int):
        """Get the OwlImage from the index"""
        return self.images[index]

    def render(self):
        w = 500
        h = 500
        self.canvas.create_image(0,0, anchor=tkinter.NW, image=self.images[0].photo(width=w, height=h))

        if self.nav:
            print('render nav')

        if self.dots:
            print('render dots')

    # tkinter methods

    def configure(self, **kw):
        if 'nav' in kw and kw['nav']!=None: self.nav = kw['nav']
        if 'dots' in kw and kw['dots']!=None: self.dots = kw['dots']
        if 'items' in kw and kw['items']!=None: self.items = kw['items']
        if 'loop' in kw and kw['loop']!=None: self.loop = kw['loop']
        if 'navText' in kw and kw['navText']!=None: self.navText = kw['navText']
        if 'autoplay' in kw and kw['autoplay']!=None: self.autoplay = kw['autoplay']
        if 'autoplayTimeout' in kw and kw['autoplayTimeout']!=None: self.autoplayTimeout = kw['autoplayTimeout']
        
        if 'bg' in kw and kw['bg']!=None:
            self.bg = kw['bg']
            self.canvas.configure(bg=self.bg)

        if 'fg' in kw and kw['fg']!=None:
            self.fg = kw['fg']

    def pack_configure(self, **kw):
        self.render()
        return super().pack_configure(**kw)
    pack = pack_configure

    def grid_configure(self, **kw):
        self.render()
        return super().grid_configure(**kw)
    grid = grid_configure

    def place_configure(self, **kw):
        self.render()
        return super().place_configure(**kw)
    place = place_configure


    config = configure