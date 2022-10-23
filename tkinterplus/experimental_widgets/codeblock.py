from tkinter import END, INSERT, SEL_FIRST, SEL_LAST, Text, Tk, Menu
import re
import json
import yaml

from ..widgets.context_menu import ContextMenu

#NOTE This widget is still being worked on. Expect issues for missing features!
class CodeBlock(Text):
    def __init__(self,master:Tk,language:str=None,**kw):
        self.master = master
        self.lang=language
        self.has_formats=False
        self.formats = {}
        self.formatsindex=0
        self.selectedindex=0
        Text.__init__(self,master,**kw)
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

        # self.bind('<KeyPress>', self.test)
        self.bind('<KeyRelease>', self.closePairs)
        self.bind('<Alt-F>', lambda e: self.format(self.lang, 1.0, END))

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
