from tkinter import StringVar
import os
from dotenv import load_dotenv

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' # Hide pygame message
load_dotenv() # load .env file that has the github personal access token: GITHUB_TOKEN = 'YOUR_TOKEN'
ROOT = os.path.dirname(os.path.realpath(__file__))
class TkinterPlusError(Exception): pass

from .constants import *
from .format import FormatVar, StyleType
from .util import easing, Ease, Language, Icon, MaterialIcon, MaterialIconError
from .animations import FAST, SLOW, Animation

# Language
lang = Language('en_US')
lang.add_directory(os.path.join(ROOT, 'assets', 'lang'))

# Import widgets
from .widgets.basewidgetplus import BaseWidgetPlus
from .widgets.picture import Picture
from .widgets.context_menu import ContextMenu
from .widgets.footer import Footer
from .widgets.form import Form
from .widgets.input import Input
from .widgets.scrolledframe import ScrolledFrame
from .windows.modal import Modal
from .widgets.accordion import Accordion
from .widgets.bindbutton import BindButton

# Import Windows
from .windows.askenum import AskEnum
from .windows.config import Config
from .windows.showprogress import ShowProgress
from .windows.texteditor import TextEditor

