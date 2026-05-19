import os
import accentcolordetect
from dotenv import load_dotenv

__version__ = "1.0.3"

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # Hide pygame message
load_dotenv()  # load .env file that has the github personal access token: GITHUB_TOKEN = 'YOUR_TOKEN'
COLOR = accentcolordetect.accent()
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
ASSET_PATH = os.path.join(ROOT_PATH, "assets")


class TkinterPlusError(Exception):
    pass


from .constants import *

# from .tests.experimental.format import FormatVar, StyleType
from .textmate import *
from .util import *
from .icon import *
from .animations import *

# Language
lang = Language("en_US")
lang.add_directory(os.path.join(ROOT_PATH, "assets", "lang"))

# Import widgets
from .widgets import *

# Import Windows
from .commondialog import Dialog
from .windows import *
