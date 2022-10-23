from re import L
from tkinter import CENTER, END, LEFT, RIGHT, StringVar, Text, Variable
from tkinter.font import Font
from enum import Enum
import uuid

class StyleType(Enum):
    BOLD = 'bold'
    UNDERLINED='underlined'
    ALIGN_LEFT = 'align_left'
    ALIGN_RIGHT = 'align_right'
    ALIGN_CENTER = 'align_center'
    FOREGROUND_COLOR = 'foreground_color'
    BACKGROUND_COLOR = 'background_color'
    STRIKETHROUGH = 'strikethrough'
    INSERT_LINK = 'insert_link'
    ITALIC = 'italic'
    BLOCKQUOTE = 'blockquote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'
    INSERT_IMAGE = 'insert_image'
    NONE = 'none'

# This is a class like str but also includes styledata

class FormatVar():
    def __init__(self, master=None, value=None, name=None):
        """A Combination of StringVar + Text widget allowing you to create styled text"""
        self.variable = StringVar(master, name)
        self.lines = []
        self.styles = []
        self.traces = []

        # max row col
        self.end = (0, 0)

        self.configure(value=value)

    def _call(self, mode:str):
        """Call the trace"""
        for t in self.traces:
            if t['mode'] == mode: t['callback']('FormatVar.name', self.variable.get(), self.styles)

    def _in_range(self, n:float, start:float, end:float):
        return start <= n <= end if end >= start else end <= n <= start

    def _str_lns(self, lines:list):
        out = ''
        i = 0
        for l in lines:
            if i ==0: out+=l
            else: out+='\n'+l
            i+=1
        return out

    def _end(self):
        """Calc the end"""
        y = len(self.lines)
        x = len(self.lines[-1])
        end = float('%d.%d'%(y, x))
        return end

    def add_style(self, index1:float, index2:float, type:StyleType, name:str=None, **kw):
        """Add styling to value"""
        style = Style(self, type=type, index1=index1, index2=index2, name=name, **kw)
        self.styles.insert(0, style)
        self._call('write')
        return style

    def get_style(self, index:float):
        """Returns with the areas style type"""
        s = []
        for style in self.styles:
            if style.index1 == END: i1 = self._end()
            else: i1 = style.index1
            if style.index2 == END: i2 = self._end()
            else: i2 = style.index2
            if self._in_range(index, i1, i2):
                s.append(style)
        self._call('read')
        return s

    def remove_style_name(self, name:str):
        """Remove styling that has the name"""
        pass

    def remove_style(self, index1:float, index2:float):
        """Remove styleing from the index1 to index2"""
        pass

    def apply_style(self, widget:Text):
        """Apply the styling to the text widget"""
        if isinstance(widget, Text):
            print('apply style')
            for s in self.styles:
                s.apply_style(widget)
        else: raise TypeError('"widget" must be a tkinter.Text widget')

    def configure(self, **kw):
        if 'value' in kw and kw['value']!=None:
            self.variable.set(kw['value'])
            self.lines = str(self.variable.get()).split('\n')
            self.end = self._end()
            self._call('write')

    def floatify(self, y:int, x:int):
        if y < 0: y=0
        if x < 0: x=0
        return float('%d.%d'%(int(y), int(x)))

    def index(self, value:float):
        """Returns a tuple (Y, X)"""
        if value==END: value = self._end()
        elif isinstance(value, str):
            print('FormatVar.index() String eval not implemented yet!', value)
            # Example: 'end-1c' (takes the end and subtracts 1 character)
            value = float(eval(value.replace('end', str(self._end()))))

        if isinstance(value, float): # Only except a float
            y, x = str(value).split('.')
            return int(y), int(x)
        else: raise TypeError('Index value must be of type float')

    def delete(self, index1:float, index2:float):
        y1, x1 = self.index(index1)
        y2, x2 = self.index(index2)
        i1 = self.floatify(y1, x1)
        i2 = self.floatify(y2, x2)

        self.remove_style(index1, index2) # remove styling as this text will be removed

        if y1 == y2:
            ln = self.lines[y1-1]
            v = ln[0:x1:] + ln[x2+1::]
            if v!='': self.lines[y1-1] = v
            else: self.lines.pop(y1-1)
        else:
            if i1 < i2: 
                fl = y2 - y1
                lines = []
                for l in range(fl):
                    if l==0:
                        mx = len(self.lines[y1-1])-1
                        self.delete(i1, self.floatify(y1, mx))
                    else: lines.append(self.lines[l])
                v = self.get(self.floatify(y2, 0), i2)
                lines.append(v)
            else: raise ValueError('index2 must be more than index1')
        
        self.configure(value=self._str_lns(self.lines)) # Update the value

    def insert(self, index1:float, chars:str):
        y, x = self.index(index1)
        
        if x ==0: first = ''
        else: first = self.get(0.0, self.floatify(y, x-1))

        if len(self.lines)>0:
            mx = len(self.lines[y])
            if x >= mx: last = ''
            else: last = self.get(self.floatify(y, x), self.floatify(y, mx))
            self.lines[y] = first + str(chars) + last
        else: self.lines.insert(0, str(chars))

        self.configure(value=self._str_lns(self.lines))

    def get(self, index1:float, index2:float, _callback:bool=True):
        y1, x1 = self.index(index1)
        y2, x2 = self.index(index2)
        i1 = self.floatify(y1, x1)
        i2 = self.floatify(y2, x2)

        if _callback: self._call('read')
        if y1 == y2:
            ln = self.lines[y1-1]
            return ln[x1:x2+1]
        else:
            if i1 < i2: 
                fl = y2 - y1
                lines = []
                for l in range(fl):
                    if l==0:
                        mx = len(self.lines[y1-1])-1
                        v = self.get(i1, self.floatify(y1, mx), False)
                        lines.append(v)
                    else: lines.append(self.lines[l])
                v = self.get(self.floatify(y2, 0), i2, False)
                lines.append(v)
                return self._str_lns(lines)
            else: raise ValueError('index2 must be more than index1')

    def set(self, value:str):
        """Set the values of the variable"""
        self.configure(value=value)
        return self

    def trace_add(self, mode:str, callback):
        if mode=='read' or mode=='write': self.traces.append({'mode': mode, 'callback': callback})
        else: raise ValueError('Value must be ["read", "write"]')

    def trace_remove(self, mode:str, cbname:str=None): self.variable.trace_remove(mode, cbname)
    def get_all(self): return self.get(0.0, END)

class Style():
    def __init__(self, variable:FormatVar, type:StyleType, index1:float, index2: float, name:str=None, color:str=None):
        self.variable = variable
        self.type = StyleType.NONE
        self.index1 = 0.0
        self.index2 = 0.0
        self.name = uuid.uuid4().hex

        self.color = 'white'

        self.configure(
            type=type,
            index1=index1,
            index2=index2,
            name=name,
            color=color
        )

    def configure(self, **kw):
        if 'name' in kw and kw['name']!=None: self.name = kw['name']
        if 'index1' in kw and kw['index1']!=None: self.index1 = kw['index1']
        if 'index2' in kw and kw['index2']!=None: self.index2 = kw['index2']
        if 'type' in kw and kw['type']!=None: self.type = kw['type']

        # Type specific
        if 'color' in kw and kw['color']!=None: self.color = kw['color']
    config = configure

    def apply_style(self, widget:Text):
        """Apply the style tag to the widget"""
        if isinstance(widget, Text):
            widget.tag_add(self.name, self.index1, self.index2)
            if self.type==StyleType.BOLD: widget.tag_configure(self.name, font=Font(weight='bold'))
            elif self.type==StyleType.UNDERLINED: widget.tag_config(self.name, font=Font(underline=True))
            elif self.type==StyleType.ALIGN_LEFT: widget.tag_configure(self.name, justify=LEFT)
            elif self.type==StyleType.ALIGN_CENTER: widget.tag_configure(self.name, justify=CENTER)
            elif self.type==StyleType.ALIGN_RIGHT: widget.tag_configure(self.name, justify=RIGHT)
            elif self.type==StyleType.STRIKETHROUGH: widget.tag_configure(self.name, font=Font(overstrike=True))
            elif self.type==StyleType.ITALIC: widget.tag_configure(self.name, font=Font(slant='italic'))
            elif self.type==StyleType.FOREGROUND_COLOR: widget.tag_configure(self.name, foreground=self.color)
            elif self.type==StyleType.BACKGROUND_COLOR: widget.tag_configure(self.name, background=self.color)
            else:
                print('Unknown styleType "%s"', self.type)

        else: raise TypeError('"widget" must be a tkinter.Text widget')

if __name__ == '__main__':
    from tkinter import Tk
    root = Tk()

    t = FormatVar()
    t.set('Hello\nWorld')
    # t.add_style(1.0, END, StyleType.BOLD)
    # t.delete(1.0, 1.4)
    print('"%s"'%t.get(1.0, END))

    root.mainloop()