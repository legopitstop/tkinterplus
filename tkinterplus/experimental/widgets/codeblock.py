# TODO
# -

from typing import Self
import tkinter
import re
import json
import yaml
import os
import glob

from ... import TEXTMATE_RULES, get_language, TmLanguage

__all__ = ["CodeBlock"]


# C:\Users\1589l\AppData\Local\Programs\Microsoft VS Code\resources\app
class CodeBlock(tkinter.Text):
    def __init__(
        self,
        master: tkinter.Tk,
        language: str = None,
        bg="#1F1F1F",
        fg="#CCCCCC",
        bd=0,
        highlightthickness=0,
        insertbackground="#CCCCCC",
        **kw
    ):
        """Construct a codeblock widget with the parent MASTER."""
        tkinter.Text.__init__(self, master, tabstyle="tabular", tabs=5)
        self.master = master
        self.language_file = None
        self.language = None
        self.configure(
            language=language,
            bg=bg,
            fg=fg,
            bd=bd,
            highlightthickness=highlightthickness,
            insertbackground=insertbackground,
            **kw
        )
        self.bind("<KeyRelease>", lambda e: self.update())

    def configure(self, **kw) -> Self:
        if "language" in kw:
            self.language_file = get_language(kw["language"])
            with open(self.language_file) as fd:
                self.language = TmLanguage.model_validate(json.load(fd))
            del kw["language"]
        super().configure(**kw)
        return self

    def update(self) -> None:
        self._update_rules()
        self._update_syntax()
        super().update()

    def _update_syntax(self) -> None:
        self.language.render(self)

    def _update_rules(self) -> None:
        global TEXTMATE_RULES
        for rule in TEXTMATE_RULES:
            rule.update(self)

    def insert(self, index: int, chars: str, *args) -> None:
        super().insert(index, chars, *args)
        self.update()
