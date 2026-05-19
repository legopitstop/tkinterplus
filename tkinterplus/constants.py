from enum import Enum


# util
class Ease(Enum):
    LINEAR = "Linear"
    BOUNCE_IN = "BounceIn"
    BOUNCE_OUT = "BounceOut"
    BOUNCE_IN_OUT = "BounceInOut"
    SINE_IN = "SineIn"
    SINE_OUT = "SineOut"
    SINE_IN_OUT = "SineInOut"
    CIRCULAR_IN = "CircularEaseIn"
    CIRCULAR_OUT = "CircularEaseOut"
    CIRCULAR_IN_OUT = "CircularEaseInOut"
    QUAD_IN = "QuadEaseIn"
    QUAD_OUT = "QuadEaseOut"
    QUAD_IN_OUT = "QuadEaseInOut"
    CUBIC_IN = "CubicEaseIn"
    CUBIC_OUT = "CubicEaseOut"
    CUBIC_IN_OUT = "CubicEaseInOut"
    QUARTIC_IN = "QuarticEaseIn"
    QUARTIC_OUT = "QuarticEaseOut"
    QUARTIC_IN_OUT = "QuarticEaseInOut"
    QUINTIC_IN = "QuinticEaseIn"
    QUINTIC_OUT = "QuinticEaseOut"
    QUINTIC_IN_OUT = "QuinticEaseInOut"
    EXPONENTIAL_IN = "ExponentialEaseIn"
    EXPONENTIAL_OUT = "ExponentialEaseOut"
    EXPONENTIAL_IN_OUT = "ExponentialEaseInOut"
    ELASTIC_IN = "ElasticEaseIn"
    ELASTIC_OUT = "ElasticEaseOut"
    ELASTIC_IN_OUT = "ElasticEaseInOut"
    BACK_IN = "BackEaseIn"
    BACK_OUT = "BackEaseOut"
    BACK_IN_OUT = "BackEaseInOut"


# Icons
class Asset(Enum):
    TK_CLOSE = "tk_close.png"
    TK_CLOSE_ACTIVE = "tk_close_active.png"
    TK_CLOSE_HOVER = "tk_close_hover.png"
    TK_MAXIMIZE = "tk_maximize.png"
    TK_MINIMIZE = "tk_minimize.png"
    TK_ERROR = "tk_error.png"
    TK_ICON = "tk_icon.ico"
    TK_INFO = "tk_info.png"
    TK_PLUME = "tk_plume.png"
    TK_QUESTION = "tk_question.png"
    TK_WARNING = "tk_warning.png"
    MISSING = "missing.png"
    DARWIN_CLOSE = "darwin_close.png"
    DARWIN_CLOSE_ACTIVE = "darwin_close_active.png"
    DARWIN_CLOSE_HOVER = "darwin_close_hover.png"
    DARWIN_MAXIMIZE = "darwin_maximize.png"
    DARWIN_MAXIMIZE_ACTIVE = "darwin_maximize_active.png"
    DARWIN_MAXIMIZE_HOVER = "darwin_maximize_hover.png"
    DARWIN_MINIMIZE = "darwin_minimize.png"
    DARWIN_MINIMIZE_ACTIVE = "darwin_minimize_active.png"
    DARWIN_MINIMIZE_HOVER = "darwin_minimize_hover.png"
    LINUX_CLOSE = "linux_close.png"
    LINUX_MAXIMIZE = "linux_maximize.png"
    LINUX_MINIMIZE = "linux_minimize.png"


# Child Commands - developer_tools
CONTAINER = "container"
CANVAS = "canvas"
LISTBOX = "listbox"
TEXT = "text"
NOTEBOOK = "notebook"
TREEVIEW = "treeview"
MENU = "menu"
OPTION_MENU = "option_menu"

# Delete Child Commands - developer_tools
CANVAS_ITEM = "canvas_item"
LISTBOX_ITEM = "listbox_item"
TEXT_TAG = "text_tag"
TREEVIEW_ITEM = "treeview_item"
MENU_ITEM = "menu_item"
OPTION_MENU_VALUE = "option_menu_value"

# Context Type - context_menu
REDO = "redo"
UNDO = "undo"
CUT = "cut"
COPY = "copy"
PASTE = "paste"
DELETE = "delete"
SELECT_ALL = "select_all"

# Entry Types - entrytypes
COLOR = "color"
SHORT = "short"
TEXT = "text"
PASSWORD = "password"
NUMBER = "number"
FILE = "file"
DIRECTORY = "directory"
INTEGER = "integer"
FILES = "files"
KEYBIND = "keybind"
FLOAT = "float"
CHECKBOX = "checkbox"
EMAIL = "email"
TEL = "tel"
URL = "url"
ENUM = "enum"
DATE = "date"
DATETIME = "datetime"
MONTH = "month"
TIME = "time"
WEEK = "week"
RADIO = "radio"
RANGE = "range"

# MaterailIcons styles
FILLED = "filled"
OUTLINED = "outlined"
ROUNDED = "rounded"
SHARP = "sharp"
TWOTONE = "twotone"

# winfo_geometry_manager
GRID = "grid"
PACK = "pack"
PLACE = "place"


# Canvas
# Camera
ORTHOGRAPHIC = 1
PERSPECTIVE = 2

# Material side
FRONT_SIDE = 1
BACK_SIDE = 2
DOUBLE_SIDE = 3

# Material blending mode
NO_BLENDING = 1
NORMAL_BLENDING = 2
ADDITIVE_BLENDING = 3
SUBTRACT_BLENDING = 4
MULTIPLY_BLENDING = 5
CUSTOM_BLENDING = 6

# Material depth mode
NEVER_DEPTH = 1
ALWAYS_DEPTH = 2
EQUAL_DEPTH = 3
LESS_DEPTH = 4
LESS_EQUAL_DEPTH = 5
GREATER_EQUAL_DEPTH = 6
GREATER_DEPTH = 7
NOT_EQUAL_DEPTH = 8

# Material text combine op
MULTIPLY_OPERATION = 1
MIX_OPERATION = 2
ADD_OPERATION = 3

# Material stencil functions
NEVER_STENCIL_FUNC = 1
LESS_STENCIL_FUNC = 2
EQUAL_STENCIL_FUNC = 3
LESS_EQUAL_STENCIL_FUNC = 4
GREATER_STENCIL_FUNC = 5
NOT_EQUAL_STENCIL_FUNC = 6
GREATER_EQUAL_STENCIL_FUNC = 7
ALWAYS_STENCIL_FUNC = 8

# Material stencil op
ZERO_STENCIL_OP = 1
KEEP_STENCIL_OP = 2
REPLACE_STENCIL_OP = 3
INCREASEMENT_STENCIL_OP = 4
DECREASEMENT_STENCIL_OP = 5
INCREASEMENT_WRAP_STENCIL_OP = 6
DECREASEMENT_WRAP_STENCIL_OP = 7
INVERT_STENCIL_OP = 8

# Material map type
TANGENT_SPACE_NORMAL_MAP = 1
OBJECT_SPACE_NORMAL_MAP = 2

# Texture mapping mods
UV_WRAPPING = 1
CUBE_REFLECTION_WRAPPING = 2
CUBE_REFRACTION_WRAPPING = 3
EQUIRECTANGULAR_REFLECTION_MAPPING = 4
EQUIRECTANGULAR_REFRACTION_MAPPING = 5
CUBE_UV_REFLECTION_MAPPING = 6
CLAMP_TO_EDGE_WRAPPING = 7

# Texture wrapping mods
UV_MAPPING = 1
CUBE_REFLECTION_MAPPING = 2
CUBE_REFRACTION_MAPPING = 3

# Texture magnification filters
NEAREST_FILTER = 1
LINEAR_FILTER = 2
NEAREST_MIPMAP_NEAREST_FILTER = 3
NEAREST_MIPMAP_LINEAR_FILTER = 4
LINEAR_MIPMAP_NEAREST_FILTER = 5
LINEAR_MIPMAP_LINEAR_FILTER = 6


# Texture formats
ALPHA_FORMAT = 1
RED_FORMAT = 2
RED_INTEGER_FORMAT = 3
RG_FORMAT = 4
RG_INTEGER_FORMAT = 5
RGBA_FORMAT = 6
RGBA_INTEGER_FORMAT = 7
LUMINACE_FORMAT = 8
LUMINACE_ALPHA_FORMAT = 9
DEPTH_FORMAT = 10
DEPTH_STENCIL_FORMAT = 11

# Texture encoding
LINEAR_ENCODING = 1
SRGB_ENCODING = 2
BASIC_DEPTH_PACKING = 2
RGBA_DEPTH_PACKING = 3
