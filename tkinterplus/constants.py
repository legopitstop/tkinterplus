from enum import Enum

# Icons
class Asset(Enum):
    TK_CLOSE='tk_close.png'
    TK_CLOSE_ACTIVE='tk_close_active.png'
    TK_CLOSE_HOVER='tk_close_hover.png'
    TK_MAXIMIZE='tk_maximize.png'
    TK_MINIMIZE='tk_minimize.png'
    TK_ERROR='tk_error.png'
    TK_ICON='tk_icon.ico'
    TK_INFO='tk_info.png'
    TK_MISSING='tk_missing.png'
    TK_PLUME='tk_plume.png'
    TK_QUESTION='tk_question.png'
    TK_WARNING='tk_warning.png'
    DARWIN_CLOSE='darwin_close.png'
    DARWIN_CLOSE_ACTIVE='darwin_close_active.png'
    DARWIN_CLOSE_HOVER='darwin_close_hover.png'
    DARWIN_MAXIMIZE='darwin_maximize.png'
    DARWIN_MAXIMIZE_ACTIVE='darwin_maximize_active.png'
    DARWIN_MAXIMIZE_HOVER='darwin_maximize_hover.png'
    DARWIN_MINIMIZE='darwin_minimize.png'
    DARWIN_MINIMIZE_ACTIVE='darwin_minimize_active.png'
    DARWIN_MINIMIZE_HOVER='darwin_minimize_hover.png'
    LINUX_CLOSE='linux_close.png'
    LINUX_MAXIMIZE='linux_maximize.png'
    LINUX_MINIMIZE='linux_minimize.png'

# Context Type
REDO='redo'
UNDO='undo'
CUT='cut'
COPY='copy'
PASTE='paste'
DELETE='delete'
SELECT_ALL='select_all'

# Input Types
COLOR='color'
TEXT='text'
PASSWORD='password'
NUMBER ='number'
FILE='file'
DIRECTORY='directory'

# MaterailIcons styles
FILLED = 'filled'
OUTLINED = 'outlined'
ROUNDED = 'rounded'
SHARP = 'sharp'
TWOTONE = 'twotone'

# winfo_geometry_manager
GRID = 'grid'
PACK = 'pack'
PLACE = 'place'