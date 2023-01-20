import json
import os
import builtins
from PIL import Image
from PIL.Image import Resampling

class Sprite():
    def __init__(self, row:int, column:int, name:str=None, fp:str=None):
        self.row = int(row)
        self.column = int(column)
        self.name = str(name)
        self.fp = str(fp)
        if name==None: self.name = os.path.basename(self.fp)

class SpriteSheet():
    def __init__(self, size:tuple, max_columns:int=None):
        self.size = size
        self.spritesheet = None
        self.width = 0
        self.height = 0
        self.row = 0 # Total
        self.column = 0
        self.sprites = []

        self.max_columns = 16
        if max_columns!=None: self.max_columns = max_columns
        # Open slot position
        self._row = 0
        self._column = 0

    def open(self, fp:str, formats=None):
        """Open an existing spritesheet"""
        self.spritesheet = Image.open(fp, formats=formats)
        
        metadata = fp+'.meta'
        if os.path.exists(metadata) and os.path.isfile(metadata):
            with builtins.open(metadata) as file:
                data = json.load(file)
                if 'textures' in data:
                    for sprite in data['textures']:
                        row = data['textures'][sprite][0]
                        column = data['textures'][sprite][1]
                        self.sprites.append(Sprite(row, column, sprite))

        # Should check which slots have a sprite for adding new sprites.
        self._update()
        return self

    def new(self):
        """Create a new spritesheet"""
        self.spritesheet = Image.new('RGBA', self.size, color='#ff0000')
        self._update()
        return self

    def _update(self):
        self.width = self.spritesheet.width
        self.height = self.spritesheet.height
        self.row = int(self.height / self.size[1])
        self.column = int(self.width / self.size[0])

    def resize(self, row:int, column:int):
        """Resize the spritesheet to fit more spites"""

        x = self.size[0] * column
        y = self.size[1] * row

        if x==0: x=self.width
        if y==0: y=self.height

        temp = self.spritesheet
        self.spritesheet = Image.new('RGBA', (x, y))
        self.spritesheet.paste(temp, (0,0))
        del temp
        self._update()

    def show(self):
        """Show the spritesheet"""
        self.spritesheet.show()
        return self

    def add_sprite(self, fp:str, name:str=None, formats=None):
        """Add an image sprite to the spritesheet"""
        temp = Image.open(fp, formats=formats).resize(self.size, Resampling.NEAREST)
        x = self.size[0] * self._column
        y = self.size[1] * self._row
        self.spritesheet.paste(temp, (x, y))
        if self._column >= self.max_columns-1:
            self._column = 0
            self._row +=1
            self.resize(self.row+1, self.max_columns)
        else:
            self._column+=1
            self.resize(self.row, self.max_columns)
        result = Sprite(self._row+1, self._column, name, fp)
        self.sprites.append(result)
        return result

    def save(self, fp, format=None):
        data = {
            "width": self.size[1],
            "height": self.size[1],
            "textures": {}
            }

        for sprite in self.sprites:
            data['textures'][sprite.name] = [sprite.row, sprite.column]

        with builtins.open(fp+'.meta', 'w') as e: e.write(json.dumps(data))
        return self.spritesheet.save(fp, format)

    def get_sprite(self, row:int, column:int):
        """Get a sprite from the spritesheet using the sprite position."""
        if row<=self.row and row>0 and column<=self.column and column>0:
            x = self.size[0] * (column - 1)
            y = self.size[1] * (row - 1)
            return self.spritesheet.resize(self.size, Resampling.NEAREST, (x, y, x+self.size[0],y+self.size[1]))
        else:
            raise ValueError("sprite can\'t exceed original spritesheet size")

    def get_sprite_name(self, name:str):
        """Get a sprite from the spritesheet using the sprite name"""
        for sprite in self.sprites:
            if sprite.name == name:
                return self.get_sprite(sprite.row, sprite.column)
        raise ValueError("'%s' could not be found!"%name)

def open(fp, size, formats=None, max_columns=None): return SpriteSheet(size, max_columns).open(fp, formats)
def new(size, max_columns=None): return SpriteSheet(size, max_columns).new()
