import tkinter
import locale
import os
import json
import logging
import requests
import base64
import hashlib
from PIL import Image, ImageTk
from . import GRID, PACK, PLACE, FILLED, OUTLINED, ROUNDED, SHARP, TWOTONE, ROOT, Asset
from enum import Enum
import easing_functions
import numpy

def winfo_geometry_manager(master: tkinter.Tk=None):
    """Retruns with the geoemtry type [GRID, PACK, PLACE, None]"""
    if master is None: master = tkinter._get_temp_root()
    if len(master.grid_slaves()) >= 1: return GRID
    if len(master.pack_slaves()) >= 1: return PACK
    if len(master.place_slaves()) >= 1: return PLACE
    return None

class Ease(Enum):
    LINEAR = 'Linear'
    BOUNCE_IN = 'BounceIn'
    BOUNCE_OUT = 'BounceOut'
    BOUNCE_IN_OUT = 'BounceInOut'
    SINE_IN = 'SineIn'
    SINE_OUT = 'SineOut'
    SINE_IN_OUT = 'SineInOut'
    CIRCULAR_IN = 'CircularEaseIn'
    CIRCULAR_OUT = 'CircularEaseOut'
    CIRCULAR_IN_OUT = 'CircularEaseInOut'
    QUAD_IN = 'QuadEaseIn'
    QUAD_OUT = 'QuadEaseOut'
    QUAD_IN_OUT = 'QuadEaseInOut'
    CUBIC_IN = 'CubicEaseIn'
    CUBIC_OUT = 'CubicEaseOut'
    CUBIC_IN_OUT = 'CubicEaseInOut'
    QUARTIC_IN = 'QuarticEaseIn'
    QUARTIC_OUT = 'QuarticEaseOut'
    QUARTIC_IN_OUT = 'QuarticEaseInOut'
    QUINTIC_IN = 'QuinticEaseIn'
    QUINTIC_OUT = 'QuinticEaseOut'
    QUINTIC_IN_OUT = 'QuinticEaseInOut'
    EXPONENTIAL_IN = 'ExponentialEaseIn'
    EXPONENTIAL_OUT = 'ExponentialEaseOut'
    EXPONENTIAL_IN_OUT = 'ExponentialEaseInOut'
    ELASTIC_IN = 'ElasticEaseIn'
    ELASTIC_OUT = 'ElasticEaseOut'
    ELASTIC_IN_OUT = 'ElasticEaseInOut'
    BACK_IN = 'BackEaseIn'
    BACK_OUT = 'BackEaseOut'
    BACK_IN_OUT = 'BackEaseInOut'

def easing(ease: Ease, start: int, end: int):
    if not isinstance(ease, Ease): raise TypeError(f'{ease} should be Easing not {ease.__class__.__name__}')
    f = None
    match ease:
        case Ease.LINEAR: f = easing_functions.LinearInOut(start, end, end)
        case Ease.BOUNCE_IN: f = easing_functions.BounceEaseIn(start, end, end)
        case Ease.BOUNCE_OUT: f = easing_functions.BounceEaseOut(start, end-1, end)
        case Ease.BOUNCE_IN_OUT: f = easing_functions.BounceEaseInOut(start, end-1, end)
        case Ease.SINE_IN: f = easing_functions.SineEaseIn(start, end+1, end)
        case Ease.SINE_OUT: f = easing_functions.SineEaseOut(start, end-1, end)
        case Ease.SINE_IN_OUT: f = easing_functions.SineEaseInOut(start, end-1, end)
        case Ease.CIRCULAR_IN: f = easing_functions.CircularEaseIn(start, end+6, end)
        case Ease.CIRCULAR_OUT: f = easing_functions.CircularEaseOut(start, end-1, end)
        case Ease.CIRCULAR_IN_OUT: f = easing_functions.CircularEaseInOut(start, end-1, end)
        case Ease.QUAD_IN: f = easing_functions.QuadEaseIn(start, end+1, end)
        case Ease.QUAD_OUT: f = easing_functions.QuadEaseOut(start, end-1, end)
        case Ease.QUAD_IN_OUT: f = easing_functions.QuadEaseInOut(start, end-1, end)
        case Ease.CUBIC_IN: f = easing_functions.CubicEaseIn(start, end+2, end)
        case Ease.CUBIC_OUT: f = easing_functions.CubicEaseOut(start, end-1, end)
        case Ease.CUBIC_IN_OUT: f = easing_functions.CubicEaseInOut(start, end-1, end)
        case Ease.QUARTIC_IN: f = easing_functions.QuarticEaseIn(start, end+3, end)
        case Ease.QUARTIC_OUT: f = easing_functions.QuarticEaseOut(start, end-1, end)
        case Ease.QUARTIC_IN_OUT: f = easing_functions.QuarticEaseInOut(start, end-1, end)
        case Ease.QUINTIC_IN: f = easing_functions.QuinticEaseIn(start, end+5, end)
        case Ease.QUINTIC_OUT: f = easing_functions.QuinticEaseOut(start, end-1, end)
        case Ease.QUINTIC_IN_OUT: f = easing_functions.QuinticEaseInOut(start, end-1, end)
        case Ease.EXPONENTIAL_IN: f = easing_functions.ExponentialEaseIn(start, end+7, end)
        case Ease.EXPONENTIAL_OUT: f = easing_functions.ExponentialEaseOut(start, end-1, end)
        case Ease.EXPONENTIAL_IN_OUT: f = easing_functions.ExponentialEaseInOut(start, end-1, end)
        case Ease.ELASTIC_IN: f = easing_functions.ElasticEaseIn(start, end, end)
        case Ease.ELASTIC_OUT: f = easing_functions.ElasticEaseOut(start, end-1, end)
        case Ease.ELASTIC_IN_OUT: f = easing_functions.ElasticEaseInOut(start, end-1, end)
        case Ease.BACK_IN: f = easing_functions.BackEaseIn(start, end+9, end)
        case Ease.BACK_OUT: f = easing_functions.BackEaseOut(start, end-1, end)
        case Ease.BACK_IN_OUT: f = easing_functions.BackEaseInOut(start, end-1, end)
        case _: raise NotImplementedError(f'"{ease}" is not a valid easing function')
    x = numpy.arange(start, end, 1, dtype=int)
    return list(map(round,  map(f, x)))

class Language():
    def __init__(self, default_language_code:str=None):
        """Translate text from a language JSON file"""
        self.default_code = default_language_code
        self.code, self._ = locale.getdefaultlocale()
        self.langs = {}
        self.variables = []

    def add_directory(self, path:str):
        """Add a directory of files"""
        for file in os.listdir(path): self.add_file(os.path.join(path, file))

    def add_file(self, fp:str):
        with open(fp, 'r') as file:
            try:
                data = json.load(file)
                code = os.path.basename(fp).replace('.json', '').casefold()

                if code in self.langs: # Merge data
                    for key in data: self.langs[code][key] = data[key]
                else: self.langs[code] = data # Set data
            except json.decoder.JSONDecodeError as err:
                logging.debug('Failed to load langauge JSON "%s": %s', fp, err)
        
    def code_exists(self, language_code:str):
        """Test if the language code exists"""
        if language_code.casefold() in self.langs: return True
        else: return False
    
    def translate(self, key:str):
        """Translate the text using the provided translation file."""
        code = self.code.casefold()
        default_code = self.default_code.casefold()
        if self.code_exists(code):
            if key in self.langs[code]: return self.langs[code][key]
            else: return key
        elif self.code_exists(default_code):
            if key in self.langs[default_code]: return self.langs[default_code][key]
            else: return key
        else: return key

    def _on_set(self):
        for variable in self.variables:
            variable[0].set(self.translate(variable[1]))

    def bind_variable(self, textvariable:tkinter.StringVar, key:str):
        """bind to textvariable"""
        textvariable.set(self.translate(key))
        self.variables.append((textvariable, key))

    def set(self, language_code:str):
        """Update the language code"""
        self.code = language_code
        self._on_set()

class Icon():
    def __init__(self, file:str, size:tuple=None, color:str=None):
        """
        Load icon
        
        Parameters
        ---
        `name` - The name of the icon. Use Icon class to get a list of aviable icons.

        `size` - The size of the icon. Uses native size by default.

        `color` - The color of the icon. Uses native color by defauit.
        """
        self.size = None
        self.color = None
        self.file = None
        self.image = None
        self.photo = None
        self.children = []

        self.configure(
            redraw=False,
            file=file,
            size=size,
            color=color
        )
    
    def update(self, redraw:bool=False):
        if self.image!=None: self.photo = ImageTk.PhotoImage(self.image)
        if redraw:
            for c in self.children: c.configure(image=self.photo)

    def configure(self, redraw=True, **kw):
        if 'file' in kw and kw['file']!=None:
            if isinstance(kw['file'], Asset): self.file = os.path.join(ROOT, 'assets', 'icons', kw['file']._value_)
            else: self.file = kw['file']
            self.image = Image.open(self.file).convert('RGBA')

        if 'color' in kw and kw['color']!=None:
            self.color = kw['color']
            if self.image!=None:
                mask = self.image.copy()
                pixels = mask.load() # create the pixel map
                for i in range(mask.size[0]):
                    for j in range(mask.size[1]):
                        if pixels[i,j] != (0, 0, 0, 0): pixels[i,j] = (0, 0, 0, 0) # 128 Replace filled with black
                        else: pixels[i,j] = (255, 255, 255) # Replace transparent with white                            
                overlay = Image.new('RGBA',self.image.size, self.color)
                self.image = Image.composite(self.image,overlay,mask).convert('RGBA')

        if 'size' in kw and kw['size']!=None:
            if isinstance(kw['size'], int): self.size = (kw['size'], kw['size'])
            else: self.size = kw['size']
            if self.image!=None: self.image = self.image.resize(self.size, Image.NEAREST)
        
        self.update(redraw)
    config = configure

    def show(self, title:str=None):
        """Displays this image. This method is mainly intended for debugging purposes."""
        if self.image!=None: self.image.show(title)
        return self

    def bind_widget(self, widget:tkinter.Tk):
        """Bind icon to widget to update the image. `widget.configure(image=update_image)`"""
        self.children.append(widget)
        return self

    def unbind_widget(self, widget:tkinter.Tk):
        """Unbind icon from this widget."""
        try: self.children.remove(widget)
        except ValueError: pass
        return self
    
    def __repr__(self):
        return self.photo

    def __str__(self):
        return str(self.photo)

# If script is unable to download the icon (no internet, in offline mode or another issue) it should use the default "Missing" icon.
# https://github.com/google/material-design-icons/tree/master/png
# https://api.github.com/repos/google/material-design-icons/git/blobs/19656ebfc488945f2be3ac953f28c7d2c89350fa
# If rate limited use a placeholder icon

class MaterialIconError(Exception): pass

#TODO Use "async" like class that will use the default icon until it finiches downloading the icon.
class MaterialIcon(Icon):
    def __init__(self, name:str, style:str=None, size:tuple=None, color:str=None, cache_path:str=None, default:Icon=None, auth=None):
        """
        Download and use google's material icons.

        Browse for any icon: https://fonts.google.com/icons?selected=Material+Icons
        
        **NOTE**: You may want to add authentication to prevent Github from rate limiting this IP. https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
        """
        super().__init__(file=Asset.TK_MISSING, size=size, color=color)

        self.name = Asset.TK_ICON
        self.style = FILLED
        self.auth = os.getenv('GITHUB_TOKEN') # Get token from .env file
        self.default = Icon(Asset.TK_MISSING)
        self.cache_path = os.path.join(os.getcwd(), '.cache')

        self.configure(
            redraw=False,
            name=name,
            style=style,
            cache_path=cache_path,
            default=default,
            auth=auth
        )

    def get(self, url:str):
        if self.auth!=None:
            headers = {
                'Authorization': 'Bearer '+self.auth
            }
            res = requests.get(url, headers=headers).json()
        else: res = requests.get(url).json()
        # Error should be printed to console but should not break the entire script. Use the default icon if error.
        if 'message' in res: raise MaterialIconError(res['message']+ ' Documentation: ' + res['documentation_url'])
        return res

    def exists(self):
        """Checks if the icon is already cached"""
        path = os.path.join(self.cache_path, self.hash_name())
        if os.path.exists(path) and os.path.isfile(path): return path
        return None

    def hash_name(self):
        #TODO Name should also include the style
        return hashlib.sha1(str(self.name+'_'+self.style).encode('utf-8')).hexdigest()

    def fetch_icon(self):
        if self.exists()==None:
            repo = self.get('https://api.github.com/repos/google/material-design-icons/git/trees/26bf62e3918daebf134ef32b74b822953bb19015')
            for ti in repo['tree']:
                cats = self.get(ti['url'])
                for c in cats['tree']:
                    if c['path'] == self.name:
                        styles = self.get(c['url'])
                        if self.style == FILLED: url = styles['tree'][0]['url']
                        elif self.style == OUTLINED: url = styles['tree'][1]['url']
                        elif self.style == ROUNDED: url = styles['tree'][2]['url']
                        elif self.style == SHARP: url = styles['tree'][3]['url']
                        elif self.style == TWOTONE: url = styles['tree'][4]['url']
                        else: raise MaterialIconError('icon style must be [filled, outlined, rounded, sharp, two_tone] but got "%s"'%self.style)

                        res = self.get(url)['tree'][3]['url']
                        res2 = self.get(res)['tree'][0]['url']
                        blob = self.get(res2)['tree'][0]['url']
                        img = self.get(blob)['content']
                        # https://api.github.com/repos/google/material-design-icons/git/blobs/19656ebfc488945f2be3ac953f28c7d2c89350fa

                        os.makedirs(self.cache_path, exist_ok=True)
                        filename = self.hash_name()
                        with open(os.path.join(self.cache_path, filename), 'wb') as f:
                            f.write(base64.b64decode(img))

                        return os.path.join(self.cache_path, filename)
            raise MaterialIconError('icon "%s" could not be found!'%self.name)
        else: return self.exists()

    def configure(self, redraw=True, **kw):
        if 'auth' in kw and kw['auth']!=None: self.auth = kw['auth']
        if 'file' in kw and kw['file']!=None: del kw['file']
        if 'style' in kw and kw['style']!=None: self.style = kw['style']
        if 'default' in kw and kw['default']!=None:
            if isinstance(kw['default'], Icon): self.default = kw['default']
            else: raise MaterialIconError('Default icon should be Icon and not %s'%(type(kw['default'])))
        if 'cache_path' in kw and kw['cache_path']!=None: self.cache_path = kw['cache_path']
        if 'name' in kw and kw['name']!=None:
            self.name = kw['name']
            path = self.fetch_icon()
            super().configure(file=path, size=self.size)
        super().configure(redraw, **kw)

    config = configure
