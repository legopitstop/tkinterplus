from pydantic import BaseModel
from typing import Self
import tkinter
import json
import glob
import re

from . import ASSET_PATH


class TmRule(BaseModel):
    scope: str
    config: dict
    children: list = []

    def bind(self, widget: tkinter.Text):
        widget.tag_configure(self.scope, **self.config)
        self.children.append(widget)

    def unbind(self, widget: tkinter.Text):
        widget.tag_delete(self.scope)
        self.children.remove(widget)

    def update(self, widget: tkinter.Text):
        if self.scope in widget.tag_names():
            self.unbind(widget)
        self.bind(widget)


class TmMatch(BaseModel):
    span: tuple
    scope: str


class TmPattern(BaseModel):
    comment: str = None
    include: str = None
    match: str = None
    name: str = None

    def render(self, root, content: str) -> list[TmMatch]:
        tags = []
        if self.match:
            # Exit if match failed
            res = re.match(self.match, content)
            if res:
                tags.extend(res)

        if self.include:
            ref = root.repository[self.include[1:]]
            if not ref:
                print(f'repository "{ self.include }" not found')
            tags.extend(ref.render(root, content))

        return tags


def find_matching_parentheses(begin, end, text):
    stack = []
    result = []
    i = 0

    while i < len(text):
        char = text[i]

        if re.match(begin, char):
            stack.append(i)

        elif re.match(end, char) and stack:
            start = stack.pop()
            if (
                not stack
            ):  # Only capture when the stack is empty (indicating a complete set of parentheses)
                result.append((start, i))

        i += 1

    return result


class TmRepository(BaseModel):
    name: str = None
    begin: str = None
    match: str = None
    beginCaptures: dict[str, Self] = {}
    end: str = None
    endCaptures: dict[str, Self] = {}
    captures: dict[str, Self] = {}
    patterns: list[TmPattern] = []

    def render(self, root, content: str) -> list[TmMatch]:
        tags = []
        if self.match:
            matches = [
                TmMatch(span=x.span(), scope=self.name)
                for x in re.finditer(self.match, content)
            ]
            tags.extend(matches)

        if self.begin and self.end:
            matches = find_matching_parentheses(self.begin, self.end, content)
            for start, end in matches:
                tags.append(TmMatch(span=(start, end + 1), scope=self.name))

                if self.beginCaptures:
                    for k, bc in self.beginCaptures.items():
                        tags.append(TmMatch(span=(start, start + 1), scope=bc.name))

                if self.endCaptures:
                    for k, ec in self.endCaptures.items():
                        tags.append(TmMatch(span=(end, end + 1), scope=ec.name))

        if self.patterns:
            for pattern in self.patterns:
                res = pattern.render(root, content)
                if res:
                    tags.extend(res)
        return tags


# Add source.abc to all
class TmLanguage(BaseModel):
    scopeName: str
    fileTypes: list[str] = []
    patterns: list[TmPattern] = []
    repository: dict[str, TmRepository] = {}
    version: str = None

    def render(self, widget: tkinter.Text) -> None:
        content = widget.get(0.0, "end")
        tags: list[TmMatch] = []
        if self.patterns:
            for pattern in self.patterns:
                tags.extend(pattern.render(self, content))

        print(tags)
        for tag in tags:
            index1 = pos_to_linechar(content, tag.span[0])
            index2 = pos_to_linechar(content, tag.span[1])
            widget.tag_add(tag.scope, index1, index2)


CUSTOM_LANGUAGES = 0
LANGUAGES = {}
TEXTMATE_RULES = [
    TmRule(scope="keyword.letter", config={"foreground": "#569CD6"}),
    TmRule(scope="punctuation.paren.open", config={"foreground": "green"}),
    TmRule(scope="punctuation.paren.close", config={"foreground": "green"}),
    # TmRule(scope='expression.group', config={'foreground': 'red'}),
]


def pos_to_linechar(text, pos):
    if pos < 0 or pos > len(text):
        raise ValueError("Position is out of bounds")

    line = 1
    char_in_line = 0

    for i in range(pos):
        if text[i] == "\n":
            line += 1
            char_in_line = 0
        else:
            char_in_line += 1

    return f"{line}.{char_in_line}"


def get_all_languages() -> dict:
    global CUSTOM_LANGUAGES
    global LANGUAGES
    if len(LANGUAGES) <= CUSTOM_LANGUAGES:
        for file in glob.glob(ASSET_PATH + "/syntaxes/*.json"):
            add_language(file)
    return LANGUAGES


def get_language(extension: str) -> str | None:
    return get_all_languages().get(extension)


def add_language(fp: str) -> bool:
    global CUSTOM_LANGUAGES
    global LANGUAGES
    with open(fp, "r", encoding="utf-8") as fd:
        res = json.load(fd)
        if "fileTypes" not in res:
            return False
        for ext in res["fileTypes"]:
            LANGUAGES[ext] = fp
            CUSTOM_LANGUAGES += 1
        return True
