from tkinter import END, INSERT, SEL_FIRST, SEL_LAST, Text, Tk, Menu, Event
import re
import json
import yaml
import os

from ... import ROOT, ContextMenu

#NOTE This widget is still being worked on. Expect issues for missing features!

class Language():
    def __init__(self, ext, id:str, aliases:list=None, extensions:list=None, filenames:list=None, mimetypes:list=None, configuration:str=None, filenamePatterns:list=None, firstLine:str=None):
        self.ext = ext
        self.id = id
        self.aliases = []
        self.extensions = []
        self.filenames = []
        self.mimetypes = []
        self.configuration = None
        self.filenamePatterns = []
        self.firstLine = None

        self.configure(
            aliases=aliases,
            extensions=extensions,
            filenames=filenames,
            mimetypes=mimetypes,
            configuration=configuration,
            filenamePatterns=filenamePatterns,
            firstLine=firstLine
        )

    def configure(self, **kw):
        if 'aliases' in kw and kw['aliases']!=None: self.aliases = kw['aliases']
        if 'extensions' in kw and kw['extensions']!=None: self.extensions = kw['extensions']
        if 'filenames' in kw and kw['filenames']!=None: self.filenames = kw['filenames']
        if 'mimetypes' in kw and kw['mimetypes']!=None: self.mimetypes = kw['mimetypes']
        if 'filenamePatterns' in kw and kw['filenamePatterns']!=None: self.filenamePatterns = kw['filenamePatterns']
        if 'firstLine' in kw and kw['firstLine']!=None: self.firstLine = kw['firstLine']
        if 'configuration' in kw and kw['configuration']!=None:
            with open(self.ext.path(kw['configuration']), 'r') as r: self.configuration = json.load(r)
        
class Grammar():
    def __init__(self, ext, language:str=None, scopeName:str=None, path:str=None, tokenTypes:dict=None, embeddedLanguages:dict=None, balancedBracketScopes:list=None, injectTo:list=None, unbalancedBracketScopes:list=None):
        self.ext = ext
        self.language = None
        self.scopeName = None
        self.path = None
        self.tokenTypes = {}
        self.embeddedLanguages = {}
        self.balancedBracketScopes = []
        self.injectTo = []
        self.unbalancedBracketScopes = []

        self.configure(
            language=language,
            scopeName=scopeName,
            path=path,
            tokenTypes=tokenTypes,
            embeddedLanguages=embeddedLanguages,
            balancedBracketScopes=balancedBracketScopes,
            injectTo=injectTo,
            unbalancedBracketScopes=unbalancedBracketScopes
        )

    def configure(self, **kw):
        if 'language' in kw and kw['language']!=None: self.language = kw['language']
        if 'scopeName' in kw and kw['scopeName']!=None: self.scopeName = kw['scopeName']
        if 'path' in kw and kw['path']!=None: self.path = kw['path']
        if 'tokenTypes' in kw and kw['tokenTypes']!=None: self.tokenTypes = kw['tokenTypes']
        if 'embeddedLanguages' in kw and kw['embeddedLanguages']!=None: self.embeddedLanguages = kw['embeddedLanguages']
        if 'balancedBracketScopes' in kw and kw['balancedBracketScopes']!=None: self.balancedBracketScopes = kw['balancedBracketScopes']
        if 'injectTo' in kw and kw['injectTo']!=None: self.injectTo = kw['injectTo']
        if 'unbalancedBracketScopes' in kw and kw['unbalancedBracketScopes']!=None: self.unbalancedBracketScopes = kw['unbalancedBracketScopes']

class Extension():
    def __init__(self, name:str):
        self.name = name
        self.languages = []
        self.grammars = []
        self._path = None

    def load(self, path):
        """Loads the extension"""
        try:
            self._path = path
            with open(os.path.join(path, 'package.json'), 'r') as r:
                pack = json.load(r)
                if 'contributes' in pack:
                    if 'languages' in pack['contributes']:
                        for lang in pack['contributes']['languages']:
                            self.languages.append(Language(self, **lang))

                    if 'grammars' in pack['contributes']:
                        for gram in pack['contributes']['grammars']:
                            self.grammars.append(Grammar(self, **gram))

            return (False, None)
        except Exception as err: return (True, err)

    def get_language(self, id:str):
        """Returns with the language"""
        for lang in self.languages:
            if lang.id == id: return lang
            for alias in lang.aliases:
                if alias == id: return lang
        return None

    def get_grammar(self, language:str):
        """Returns with the grammar"""
        for gram in self.grammars:
            if gram.language == language: return gram
        return None

    def path(self, path:str):
        if path.startswith('.'): return os.path.join(self._path, path)
        return os.path.join(path)

class CodeBlock(Text):
    def __init__(self, master:Tk, language:str=None, **kw):
        """Construct a codeblock widget with the parent MASTER."""
        self.master = master
        self.has_formats=False
        self.formats = {}
        self.formatsindex=0
        self.selectedindex=0
        self.load_extensions = True

        self.language:Language = None
        self.grammar:Grammar = None
        Text.__init__(self, master, tabstyle='tabular', tabs=5, **kw)
        self.autoClosingPairs = [
            {
                "open": "{",
                "close": "}",
                "notIn": [
                    "string",
                    "comment"
                ]
            },
            {
                "open": "[",
                "close": "]",
                "notIn": [
                    "string",
                    "comment"
                ]
            },
            {
                "open": "(",
                "close": ")",
                "notIn": [
                    "string",
                    "comment"
                ]
            },
            {
                "open": "\"",
                "close": "\"",
                "notIn": [
                    "string",
                    "comment"
                ]
            },
            {
                "open": "'",
                "close": "'",
                "notIn": [
                    "string",
                    "comment"
                ]
            }
        ]

        self.extensions = []

        # self.bind('<KeyPress>', self.test)
        self.bind('<KeyRelease>', self._lang_configuration)
        self.bind('<Alt-F>', lambda e: self.format(self.language, 1.0, END))

        self.load_extension(os.path.join(ROOT, 'assets', 'extensions'))
        self.set_language(language)

    def set_language(self, name:str):
        for ext in self.extensions:
            lang = ext.get_language(id=name)
            if lang!=None:
                self.language = lang
                self.grammar = ext.get_grammar(lang.id)
                return lang
        print('not found')
        return None

    def load_extension(self, path:str):
        if os.path.isdir(path):
            for name in os.listdir(path):
                ext = Extension(name)
                err, msg = ext.load(os.path.join(path, name))
                if err==False: self.extensions.append(ext)
                else: print('Failed to load extension "%s": %s'%(name, msg))

    def _lang_configuration(self, e:Event):
        c = self.language.configuration
        if c!=None:
            if 'autoClosingPairs' in c:
                for pair in c['autoClosingPairs']:
                    if pair['open'] == e.char:
                        self.insert(INSERT,pair['close'])
                        
                        # Move Cursor back one
                        pos = self.index(INSERT)
                        row = re.sub(r'\..*','',pos)
                        column = re.sub(r'.*\.','',pos)
                        self.mark_set("insert", '%s.%s'%(row,int(column)-1))

            # newline
            if 'indentationRules' in c and e.keysym == 'Return':
                print('newline')


    def closePairs(self,e):
        for pair in self.autoClosingPairs:
            if 'open' in pair:
                if e.char == pair['open']:
                    if 'close' in pair:
                        passed=True
                        self.insert(INSERT,pair['close'])
                        pos = self.index(INSERT)
                        row = re.sub(r'\..*','',pos)
                        column = re.sub(r'.*\.','',pos)

                        if 'notIn' in pair:
                            for notIn in pair['notIn']:
                                if notIn=='comment':
                                    print('COMMENT')
                                    print(row)
                                elif notIn=='string':
                                    print('STRING')
                        if passed:
                            self.mark_set("insert", '%s.%s'%(row,int(column)-1))
                    else:
                        print('Missing required property "close"')

    def format(self,fp_or_name,index1,index2):
        input = self.get(index1, index2)
        if fp_or_name=='json':
            try:
                obj = json.loads(input)
                out = json.dumps(obj,indent=4)
                self.replace(index1, index2, out)
            except json.decoder.JSONDecodeError: pass
        elif fp_or_name=='json-min':
            try:
                obj = json.loads(input)
                out = json.dumps(obj)
                self.replace(index1, index2, out)
            except json.decoder.JSONDecodeError: pass
        
        elif fp_or_name=='yaml':
            obj = yaml.load(input,yaml.FullLoader)
            out = yaml.dump(obj)
            self.replace(index1, index2, out)
        
        else:
            print('CUSTOM',fp_or_name,input)

    def contextMenu(self):
        def is_selected():
            """Checks if the user has text selected"""
            try: return self.selection_get()
            except: return None

        def show():
            # Custom formats
            if self.has_formats:
                if self.formatsindex!=0:
                    menu.delete(self.formatsindex)
                    formats.delete(0,END)
                
                menu.insert_cascade(1,label='Format Document With...',menu=formats)
                self.formatsindex=1

                for format in self.formats:
                    formats.add_command(label=format, command=lambda fp=self.formats[format]: self.format(fp,1.0,END))

            # Format selection if text is selected
            sel = is_selected()
            if sel!=None:
                if self.selectedindex!=0: menu.delete(self.selectedindex)
                else: self.selectedindex = self.formatsindex+1

                menu.insert_command(self.selectedindex, label='Format Selection', command=lambda: self.format(self.lang, SEL_FIRST, SEL_LAST))
            else:
                if self.selectedindex!=0:
                    menu.delete(self.selectedindex)
                    self.selectedindex=0

        menu = ContextMenu(self,showcommand=show)
        formats = Menu(tearoff=False)
        menu.add_command(label='Format Document',command=lambda: self.format(self.lang, 1.0,END))

        menu.add_separator()
        menu.add_command(label='Cut', type=ContextMenu.CUT)
        menu.add_command(label='Copy',type=ContextMenu.COPY)
        menu.add_command(label='Paste',type=ContextMenu.PASTE)
        return menu

    def add_format(self,label:str,fp_or_name:str):
        self.has_formats=True
        self.formats[label]=fp_or_name

    def _update_syntax(self):
        if self.language!=None and self.grammar!=None:
            print(self.language)

    def insert(self, index: int, chars: str, *args):
        # format
        if self.language!=None: self._update_syntax()
        super().insert(index, chars, *args)