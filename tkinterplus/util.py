from tkinter import StringVar
from PIL import Image, ImageTk
import locale
import os
import json
import logging

from . import ROOT, TK_ICON

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

    def bind_variable(self, textvariable:StringVar, key:str):
        """bind to textvariable"""
        textvariable.set(self.translate(key))
        self.variables.append((textvariable, key))

    def set(self, language_code:str):
        """Update the language code"""
        self.code = language_code
        self._on_set()

# TODO Should download the icon to ".cache" to be used. This way all icons don't need to be included in the package and means 
# if this script gets converted to .exe you won't need to include all the icon files.

# If script is unable to download the icon (no internet, in offline mode or another issue) it should use the default "Missing" icon.

# filename in .cache should be a sha1 of the origional filename.
class Icon():
    def __init__(self, name:str, size:tuple=None, color:str=None):
        """
        Load icon
        
        Parameters
        ---
        `name` - The name of the icon. Use Icon class to get a list of aviable icons.

        `size` - The size of the icon. Uses native size by default.

        `color` - The color of the icon. Uses native color by defauit.
        """
        self.name = TK_ICON
        self.size = None
        self.color = None
        self.file = None
        self.image = None
        self.photo = None

        self.configure(
            name=name,
            size=size,
            color=color
        )
    
    def update(self):
        if self.image!=None: self.photo = ImageTk.PhotoImage(self.image)

    def configure(self, **kw):
        if 'name' in kw and kw['name']!=None:
            self.file = os.path.join(ROOT, 'assets', 'icons', str(kw['name']))
            self.name = kw['name']
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
            self.size = kw['size']
            if self.image!=None: self.image = self.image.resize(self.size, Image.NEAREST)
        
        self.update()
    config = configure

    def show(self, title:str=None):
        """Displays this image. This method is mainly intended for debugging purposes."""
        if self.image!=None: self.image.show(title)
        return self
    
    def __repr__(self):
        return self.photo

    def __str__(self):
        return str(self.photo)
