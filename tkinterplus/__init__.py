import os

ROOT = os.path.dirname(os.path.realpath(__file__))

from .constants import *
from .format import FormatVar, StyleType
from .util import Language, Icon

# Language
lang = Language('en_US')
lang.add_directory(os.path.join(ROOT, 'assets', 'lang'))

#! Important
from .experimental_widgets.tooltip import Tooltip

# Import widgets
from .widgets.picture import Picture
from .widgets.context_menu import ContextMenu, ContextMenuType
from .widgets.footer import Footer
from .widgets.form import Form
from .widgets.input import Input
from .widgets.scrolledframe import ScrolledFrame
from .widgets.modal import Modal
from .widgets.accordion import Accordion

# Import Experimental widgets
from .experimental_widgets.audio import Audio
from .experimental_widgets.codeblock import CodeBlock
from .experimental_widgets.formattext import FormatText
from .experimental_widgets.paragraph import Paragraph
from .experimental_widgets.slideshow import Slideshow
from .experimental_widgets.tabs import Tabs
from .experimental_widgets.canvas3d import Canvas3D

# Import Windows
from .windows.askenum import AskEnum
from .windows.config import Config
from .windows.showprogress import ShowProgress
from .windows.texteditor import TextEditor