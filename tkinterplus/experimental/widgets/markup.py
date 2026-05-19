# TODO
# -
from typing import Self
from tkinter.font import Font
import tkinter
import bs4
import os
import emoji
import webbrowser

import markdown

from ... import ROOT_PATH, parseCSS, Selector, simpledialog

__all__ = ["Format", "Markdown", "BBCode", "reStructuredText", "element", "Markup"]


class Format:
    def __init__(self):
        pass

    def parse(self) -> str:
        raise NotImplementedError()


class Markdown(Format):
    def __init__(self):
        """
        Configureable markdown format for Markup.
        """
        super().__init__()
        # Basic
        self.headings = True
        self.paragraphs = True
        self.line_breaks = True
        self.bold = True
        self.italic = True
        self.blockquotes = True
        self.ordered_lists = True
        self.unordered_lists = True
        self.code = True
        self.horizontal_rules = True
        self.links = True
        self.images = True
        # Extended
        self.tables = False
        self.fenced_code_blocks = False
        self.syntax_highlighting = False
        self.footnotes = False
        self.heading_ids = False
        self.definition_lists = False
        self.strikethrough = False
        self.task_lists = False
        self.emojis = False
        self.highlight = False
        self.subscript = False
        self.superscript = False
        self.automatic_url_linking = False
        self.disabling_url_linking = False
        self.html = False

        # Additional
        self.spoilers = False
        self.underline = False
        self.abbreviation = False
        self.abbreviation = False

    def extras(self) -> list[str]:
        extras = []
        if self.fenced_code_blocks:
            extras.append("fenced-code-blocks")
        if self.footnotes:
            extras.append("footnotes")
        if self.heading_ids:
            extras.append("header-ids")
        if self.spoilers:
            extras.append("spoiler")
        if self.strikethrough:
            extras.append("strike")
        if self.tables:
            extras.append("tables")
        if self.task_lists:
            extras.append("task_list")

        return extras

    @property
    def flavor(self):
        return getattr(self, "_flavor", None)

    @flavor.setter
    def flavor(self, value: str):
        # markdown flavors from: https://www.markdownguide.org/tools
        # TODO: needs to be re-worked to use spefic characters per option
        match value.lower():
            case "discord":
                self.headings = True
                self.paragraphs = False
                self.line_breaks = False
                self.bold = True
                self.italic = True
                self.blockquotes = True
                self.ordered_lists = False
                self.unordered_lists = True
                self.code = True
                self.horizontal_rules = False
                self.links = True
                self.images = False
                self.tables = False
                self.fenced_code_blocks = True
                self.syntax_highlighting = True
                self.footnotes = False
                self.heading_ids = False
                self.definition_lists = False
                self.strikethrough = True
                self.task_lists = False
                self.emojis = True
                self.highlight = False
                self.subscript = False
                self.superscript = False
                self.automatic_url_linking = True
                self.disabling_url_linking = True
                self.html = False
                self.spoilers = True
                self.underline = True
                self.abbreviation = False

            case "github":
                self.headings = True
                self.paragraphs = True
                self.line_breaks = True
                self.bold = True
                self.italic = True
                self.blockquotes = True
                self.ordered_lists = True
                self.unordered_lists = True
                self.code = True
                self.horizontal_rules = True
                self.links = True
                self.images = True
                self.tables = True
                self.fenced_code_blocks = True
                self.syntax_highlighting = True
                self.footnotes = True
                self.heading_ids = True
                self.definition_lists = True
                self.strikethrough = True
                self.task_lists = True
                self.emojis = False
                self.highlight = False
                self.subscript = False
                self.superscript = False
                self.automatic_url_linking = True
                self.disabling_url_linking = True
                self.html = True
                self.spoilers = False
                self.underline = False
                self.abbreviation = True

            case "jekyll":
                self.headings = True
                self.paragraphs = True
                self.line_breaks = True
                self.bold = True
                self.italic = True
                self.blockquotes = True
                self.ordered_lists = True
                self.unordered_lists = True
                self.code = True
                self.horizontal_rules = True
                self.links = True
                self.images = True
                self.tables = True
                self.fenced_code_blocks = True
                self.syntax_highlighting = True
                self.footnotes = True
                self.heading_ids = True
                self.definition_lists = True
                self.strikethrough = True
                self.task_lists = True
                self.emojis = False
                self.highlight = False
                self.subscript = False
                self.superscript = False
                self.automatic_url_linking = True
                self.disabling_url_linking = True
                self.html = True
                self.spoilers = False
                self.underline = False
                self.abbreviation = True

            case "notion":
                self.headings = True
                self.paragraphs = True
                self.line_breaks = True
                self.bold = True
                self.italic = True
                self.blockquotes = True
                self.ordered_lists = True
                self.unordered_lists = True
                self.code = True
                self.horizontal_rules = True
                self.links = True
                self.images = True
                self.tables = True
                self.fenced_code_blocks = True
                self.syntax_highlighting = True
                self.footnotes = False
                self.heading_ids = False
                self.definition_lists = False
                self.strikethrough = True
                self.task_lists = True
                self.emojis = True
                self.highlight = False
                self.subscript = False
                self.superscript = False
                self.automatic_url_linking = True
                self.disabling_url_linking = False
                self.html = False
                self.spoilers = False
                self.underline = False
                self.abbreviation = False

            case "reddit":
                self.headings = True
                self.paragraphs = True
                self.line_breaks = True
                self.bold = True
                self.italic = True
                self.blockquotes = True
                self.ordered_lists = True
                self.unordered_lists = True
                self.code = True
                self.horizontal_rules = True
                self.links = True
                self.images = False
                self.tables = True
                self.fenced_code_blocks = True
                self.syntax_highlighting = False
                self.footnotes = False
                self.heading_ids = False
                self.definition_lists = False
                self.strikethrough = True
                self.task_lists = False
                self.emojis = False
                self.highlight = False
                self.subscript = False
                self.superscript = True
                self.automatic_url_linking = True
                self.disabling_url_linking = True
                self.html = False
                self.spoilers = True
                self.underline = False
                self.abbreviation = False

            case "squarespace":
                self.headings = True
                self.paragraphs = True
                self.line_breaks = True
                self.bold = True
                self.italic = True
                self.blockquotes = True
                self.ordered_lists = True
                self.unordered_lists = True
                self.code = True
                self.horizontal_rules = True
                self.links = True
                self.images = True
                self.tables = True
                self.fenced_code_blocks = True
                self.syntax_highlighting = False
                self.footnotes = False
                self.heading_ids = False
                self.definition_lists = False
                self.strikethrough = True
                self.task_lists = False
                self.emojis = True
                self.highlight = False
                self.subscript = False
                self.superscript = False
                self.automatic_url_linking = True
                self.disabling_url_linking = True
                self.html = True
                self.spoilers = False
                self.underline = False
                self.abbreviation = False

            case "trello":
                self.headings = True
                self.paragraphs = True
                self.line_breaks = True
                self.bold = True
                self.italic = True
                self.blockquotes = True
                self.ordered_lists = True
                self.unordered_lists = True
                self.code = True
                self.horizontal_rules = True
                self.links = True
                self.images = True
                self.tables = False
                self.fenced_code_blocks = True
                self.syntax_highlighting = False
                self.footnotes = False
                self.heading_ids = False
                self.definition_lists = False
                self.strikethrough = True
                self.task_lists = False
                self.emojis = False
                self.highlight = False
                self.subscript = False
                self.superscript = False
                self.automatic_url_linking = True
                self.disabling_url_linking = True
                self.html = False
                self.spoilers = False
                self.underline = False
                self.abbreviation = False

            case "vscode":
                self.headings = True
                self.paragraphs = True
                self.line_breaks = True
                self.bold = True
                self.italic = True
                self.blockquotes = True
                self.ordered_lists = True
                self.unordered_lists = True
                self.code = True
                self.horizontal_rules = True
                self.links = True
                self.images = True
                self.tables = True
                self.fenced_code_blocks = True
                self.syntax_highlighting = True
                self.footnotes = False
                self.heading_ids = False
                self.definition_lists = False
                self.strikethrough = True
                self.task_lists = False
                self.emojis = False
                self.highlight = False
                self.subscript = False
                self.superscript = False
                self.automatic_url_linking = True
                self.disabling_url_linking = True
                self.html = True
                self.spoilers = False
                self.underline = False
                self.abbreviation = False

            case _:
                raise KeyError(f"Unknown markdown flavor '{value}'")

        setattr(self, "_flavor", value)

    def parse(self, string: str) -> str:  # TODO: Should use args
        return markdown.markdown(string, extras=self.extras())


class BBCode(Format):
    def __init__(self):
        super().__init__()
        raise NotImplementedError()


class reStructuredText(Format):
    def __init__(self):
        super().__init__()
        raise NotImplementedError()


# A Message widget that will render formatted text (coloring, bold, italic, images, etc)
# Default format is in HTML
class element:
    def __init__(self, parent, name: str, innerHTML: bs4.NavigableString, e: bs4.Tag):
        self.parent = parent
        self.stylesheet = parent.stylesheet
        self.name = name
        self.width = 0
        self.height = 0
        self.x = parent.x
        self.y = parent.y
        self.innerHTML = str(innerHTML)
        self.attrs = e.attrs
        self.id = None

        self.style = self.stylesheet.get(self.selector)
        match self.style.get("display"):
            case "block":
                self.width = len(self.innerHTML)
                self.height = self.style.get("font-size")
                parent.y += self.height + 1

            case _:  # TODO: figure out how it should place the items?
                self.width = len(self.innerHTML)
                self.height = self.style.get("font-size")
                parent.y += self.height + 1

    @property
    def font(self):
        size = self.style.get("font-size")
        font_weight = self.style.get("font-weight")
        font_style = self.style.get("font-style")
        text_decor = self.style.get("text-decoration")

        weight = "normal"
        if font_weight == "bold":
            weight = "bold"

        slant = "roman"
        if font_style == "italic":
            slant = "italic"

        underline = False
        overstrike = False
        if text_decor == "underline":
            underline = True
        elif text_decor == "line-through":
            overstrike = True

        res = Font(
            size=size,
            weight=weight,
            slant=slant,
            underline=underline,
            overstrike=overstrike,
        )

        print(self.name, self.style)
        return res

    @property
    def selector(self):
        sel = Selector(None)
        sel.tag = self.name
        sel.id = self.attrs.get("id")
        sel.cls = self.attrs.get("class")
        sel.link = self.attrs.get("href")
        return sel

    def render(self, canvas: tkinter.Canvas) -> None:
        display = self.style.get("display")
        fill = self.style.get("color")
        match display:  # none, inline, block, inline-block, list-item, table, table-row-group, table-cell, table-footer-group, table-header-group, table-row,
            case "block":
                self.id = canvas.create_text(
                    self.x,
                    self.y,
                    text=self.innerHTML,
                    anchor="nw",
                    font=self.font,
                    fill=fill,
                )
            case "none":
                pass
            case "inline" | _:
                self.id = canvas.create_text(
                    self.x,
                    self.y,
                    text=self.innerHTML,
                    anchor="nw",
                    font=self.font,
                    fill=fill,
                )

        # Functional Tags
        if self.name == "a":
            url = self.attrs.get("href")
            if url is not None:
                canvas.tag_bind(
                    self.id,
                    "<Button-1>",
                    lambda e: simpledialog.askopenurl("Open Website", url),
                )

    def __str__(self) -> str:
        return f'{self.name}(innerHTML="{self.innerHTML}")'


class Markup(tkinter.Frame):
    def __init__(self, master, format: Format = None, **kw):
        """Construct a richmessage widget with the parent MASTER."""
        super().__init__(master)
        self._variable = tkinter.StringVar()
        self.format = None
        self._last_id = 0

        self.stylesheet = parseCSS().from_file(
            os.path.join(ROOT_PATH, "assets", "styles", "default.css")
        )
        self.elements = []

        self.canvas = tkinter.Canvas(self, borderwidth=0, highlightthickness=0)
        self.canvas.pack(expand=1, fill="both")
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.x = 10
        self.y = 10

        self.configure(format=format, **kw)

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value: Format | None):
        if value == None:
            self._format = None
        elif isinstance(value, Format):
            self._format = value
        else:
            raise TypeError(
                f"Expected Format or None but got {value.__class__.__name__} instead."
            )

    def configure(self, **kw) -> Self:
        if "format" in kw and kw["format"] != None:
            self.format = kw.pop("format")
        self.canvas.configure(**kw)
        return self

    config = configure

    def render(self) -> None:
        self.canvas.delete("all")
        for e in self.elements:
            e.render(self.canvas)

    def parse(self, string: str) -> None:
        def _parse(elements):
            for e in elements:
                if isinstance(e, bs4.element.Tag):
                    _parse(e)
                elif isinstance(e, bs4.element.NavigableString):
                    ele = None
                    match elements.name:
                        case "[document]":
                            pass
                        case _:
                            ele = element(self, elements.name, e, elements)
                    if ele != None:
                        self.elements.append(ele)

                else:
                    print(f'unknown element "{e.__class__.__name__}"')
                self._last_id += 1

        if self.format is not None:
            string = self.format.parse(str(string))
        self.html = str(string)
        print(self.html)

        elements = bs4.BeautifulSoup(self.html, "html.parser")
        _parse(elements)

    def load_file(self, fp: str) -> Self:
        with open(fp, "r") as r:
            self.set(r.read())
        return self

    def set(self, value: str) -> Self:
        self.parse(value)
        self.render()
        self._variable.set(value)
        return self

    def get(self) -> str:
        return self._variable.get()
