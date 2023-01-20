"""NOTE This widget is still being worked on. Expect issues for missing features!"""
import tkinter
import tkinter

from . import Footer, Modal

class ModalDialog():
    def __init__(self, **options):
        self.master = options.get('parent')
        self.options = options

        if self.master is None:
            self.master = tkinter._get_temp_root() # When 'parent' is None use root

        # update instance options
        for k, v in options.items():
            self.options[k] = v

        self.modal = Modal(self.master, bg_color='white')
        self.modal.title(self.options.get('title'))
        self.modal.protocol('WM_DELETE_WINDOW', self.modal.destroy)

        self.frame = tkinter.Frame(self.modal, bg='white')
        self.frame.grid(row=0,column=0, ipadx=15, ipady=15, sticky='nesw')

        self.footer = Footer(self.modal)
        self.modal.grid_columnconfigure(0, weight=1)
        self.modal.show()