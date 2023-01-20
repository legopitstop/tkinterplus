"""NOTE This widget is still being worked on. Expect issues for missing features!"""
import tkinter
import winsound
import platform
from tkinter.messagebox import INFO, WARNING, ERROR, QUESTION, OK, YESNO, YESNOCANCEL, OKCANCEL, CANCEL, YES, RETRY, RETRYCANCEL, NO
from . import Asset, Icon
from .modaldialog import ModalDialog

def playsound(widget, sound:str):
    plat = platform.system()
    if plat=='Windows': winsound.PlaySound(sound, winsound.SND_ASYNC)
    else: widget.bell() # Use default bell if platform is not supported

class Message(ModalDialog):
    def __init__(self, **options):
        super().__init__(**options)
        self.frame._info = None

    def body(self):
        if self.options.get('icon') == 'info':
            self.frame._img = Icon(Asset.TK_INFO)
            playsound(self.frame, 'SystemQuestion')

        elif self.options.get('icon') == 'warning':
            self.frame._img = Icon(Asset.TK_WARNING)
            playsound(self.frame, 'SystemExclamation')

        elif self.options.get('icon') == 'error':
            self.frame._img = Icon(Asset.TK_ERROR)
            playsound(self.frame, 'SystemHand')

        elif self.options.get('icon') == 'question':
            self.frame._img = Icon(Asset.TK_QUESTION)
            playsound(self.frame, 'SystemQuestion')

        elif self.options.get('icon') != None:
            self.frame._img = Icon(self.options.get('icon'))
            self.frame.bell()

        self.icon = tkinter.Label(self.frame, image=self.frame._img, compound=tkinter.LEFT, width=45, height=45, bg='white')
        self.icon.grid(row=0,column=0, padx=(15, 0), sticky=tkinter.W)

        self.msg = tkinter.Label(self.frame, text=self.options.get('message'), bg='white', justify=tkinter.LEFT, wraplength=445, anchor=tkinter.W)
        self.msg.grid(row=0,column=1, sticky=tkinter.EW)

        self.frame.grid_columnconfigure(1, weight=1)

        btn_options = {}
        if self.options.get('type') == OK:
            self.footer.add_button(text='OK', command=self.modal.destroy, **btn_options)
        elif self.options.get('type') == OKCANCEL:
            self.footer.add_button(text='OK', command=self.modal.destroy, **btn_options)
            self.footer.add_button(text='Cancel', command=self.modal.destroy, **btn_options)
        elif self.options.get('type') == YESNO:
            self.footer.add_button(text='Yes', command=self.modal.destroy, **btn_options)
            self.footer.add_button(text='No', commnad=self.modal.destroy, **btn_options)
        elif self.options.get('type') == YESNOCANCEL:
            self.footer.add_button(text='Yes', command=self.modal.destroy, **btn_options)
            self.footer.add_button(text='No', command=self.modal.destroy, **btn_options)
            self.footer.add_button(text='Cancel', command=self.modal.destroy, **btn_options)
        elif self.options.get('type') == RETRYCANCEL:
            self.footer.add_button(text='Retry', command=self.modal.destroy, **btn_options)
            self.footer.add_button(text='Cancel', command=self.modal.destroy, **btn_options)
        

def _show(title=None, message=None, _icon=None, _type=None, **options):
    if _icon and "icon" not in options:
        options["icon"] = _icon
    if _type and "type" not in options:
        options["type"] = _type
    if title:
        options["title"] = title
    if message:
        options["message"] = message
    res = Message(**options).body()
    # In some Tcl installations, yes/no is converted into a boolean.
    if isinstance(res, bool):
        if res:
            return YES
        return NO
    # In others we get a Tcl_Obj.
    return str(res)


def showinfo(title=None, message=None, **options):
    "Show an info message"
    return _show(title, message, INFO, OK, **options)


def showwarning(title=None, message=None, **options):
    "Show a warning message"
    return _show(title, message, WARNING, OK, **options)


def showerror(title=None, message=None, **options):
    "Show an error message"
    return _show(title, message, ERROR, OK, **options)


def askquestion(title=None, message=None, **options):
    "Ask a question"
    return _show(title, message, QUESTION, YESNO, **options)


def askokcancel(title=None, message=None, **options):
    "Ask if operation should proceed; return true if the answer is ok"
    s = _show(title, message, QUESTION, OKCANCEL, **options)
    return s == OK


def askyesno(title=None, message=None, **options):
    "Ask a question; return true if the answer is yes"
    s = _show(title, message, QUESTION, YESNO, **options)
    return s == YES


def askyesnocancel(title=None, message=None, **options):
    "Ask a question; return true if the answer is yes, None if cancelled."
    s = _show(title, message, QUESTION, YESNOCANCEL, **options)
    # s might be a Tcl index object, so convert it to a string
    s = str(s)
    if s == CANCEL:
        return None
    return s == YES


def askretrycancel(title=None, message=None, **options):
    "Ask if operation should be retried; return true if the answer is yes"
    s = _show(title, message, WARNING, RETRYCANCEL, **options)
    return s == RETRY
