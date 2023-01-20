"""NOTE This widget is still being worked on. Expect issues for missing features!"""
# Animations for Tkinter
# baised on the jquery API https://api.jquery.com/category/effects/
from . import easing, TkinterPlusError, Ease
from colour import Color
import tkinter

#TODO swing = circularEaseInOut

SLOW = 600
FAST = 200

# .animate(arg1=1, arg2=2)
# x2 stepcommand(now:int, fx:Tween) - A function to be called for each animated property of each animated element. This function provides an opportunity to modify the Tween object to change the value of the property before it is set.
# x1 progresscommand(animation:Animation, progress:int, ms:int) - A function to be called after each step of the animation, only once per animated element regardless of the number of animated properties
# x1 donecommand() - A function that is called once the animation on an element is complete.

def _color(color: str):
    """Make sure the color is an actual color"""
    match str(color).lower():
        case 'systembuttonface': return '#f0f0f0'
        case 'systembuttontext': return 'black'
        case _: return color

class Tween():
    def __init__(self, widget, prop):
        self.widget = None
        self.prop = None

        self.configure(
            widget = widget,
            prop=prop
        )

    def configure(self, **kw):
        if 'widget' in kw and kw['widget']: self.widget = kw['widget']
        if 'prop' in kw and kw['prop']: self.prop = kw['prop']

    def run(self):
        pass

    config = configure

class fx():
    def __init__(self, anim, widget:tkinter.Widget, TagOrId:str=None, duration:int=400, queue:bool=None, easing:str=None, stepcommand=None, progresscommand=None, donecommand=None, name:str=None, options:dict={}):
        self.anim = anim
        self.widget = widget
        self.end = options
        self.options = options # Should get removed END is used instead
        self.start = {}
        self.duration = 400
        self.name = 'fx'
        self.easing = Ease.LINEAR
        self.donecommand = None
        self.step = None
        self.TagOrId = None
        self.queue = True
        self.locked = False

        ## Valid props, all others should be private __ARG
        # start
        # end
        # widget (elem)
        # prop

        self.configure(
            TagOrId=TagOrId,
            queue=queue,
            easing=easing,
            stepcommand=stepcommand,
            progresscommand=progresscommand,
            donecommand=donecommand,
            name=name,
            duration=duration
        )

    def configure(self, **kw):
        if self.locked==False:
            if 'duration' in kw and kw['duration']!=None: self.duration = kw['duration']
            if 'TagOrId' in kw and kw['TagOrId']!=None: self.TagOrId = kw['TagOrId']
            if 'queue' in kw and kw['queue']!=None: self.queue = kw['queue']
            if 'easing' in kw and kw['easing']!=None: self.easing = kw['easing']
            if 'stepcommand' in kw and kw['stepcommand']!=None: self.stepcommand = kw['stepcommand']
            if 'progresscommand' in kw and kw['progresscommand']!=None: self.progresscommand = kw['progresscommand']
            if 'donecommand' in kw and kw['donecommand']!=None: self.donecommand = kw['donecommand']
            if 'name' in kw and kw['name']!=None: self.name = kw['name']
        else:
            raise TkinterPlusError('Cannot configure the FX while its running!')
    config = configure

    def done(self):
        """When the animation is donecommand"""
        self.locked = False
        if self.queue:
            self.anim.running = None
            self.anim.dequeue()
        if self.donecommand!=None:
            self.donecommand(self.anim)

    def _number(self, option:str, start:int, end:int, callback):
        _start = start
        _end = end
        if _start > _end:
            _t = _start
            _start = _end
            _end = _t
        time = self.duration / (_start + _end)
        t = 0
        for i in easing(self.easing, _start, _end):
            kw = {}
            kw[option] = i+1
            # self.widget.after(round(t), lambda kw=kw: self.widget.configure(**kw))
            self.widget.after(round(t), lambda kw=kw: callback(**kw))
            

            if i+1 == _end: self.widget.after(round(t)+1, self.done)
            t+=time

    def _color(self, option:str, start:str, end:str, callback):
        frames = round(self.duration / 10)
        colors = list(Color(_color(start)).range_to(Color(_color(end)), frames))
        time = self.duration / len(colors)
        t = 0
        cnt = 0
        for c in colors:
            kw = {}
            kw[option] = c
            # self.widget.after(round(t), lambda kw=kw: self.widget.configure(**kw))
            self.widget.after(round(t), lambda kw=kw: callback(**kw))

            if cnt+1 == frames: self.widget.after(round(t)+1, self.done)
            cnt+=1
            t+=time

    def _special(self, option:str, start:int, end:int, callback):
        """Special version of the self._number for dealing with .place()"""
        _start = start
        _end = end
        if _start > _end:
            _t = _start
            _start = _end
            _end = _t
        time = self.duration / (_start + _end)
        t = 0
        for i in easing(self.easing, _start, _end):
            kw = {'x': self.widget.winfo_x(), 'y': self.widget.winfo_y()}
            kw[option] = i+1
            # self.widget.after(round(t), lambda kw=kw: self.widget.place(**kw))
            self.widget.after(round(t), lambda kw=kw: callback(kw))
            if i+1 == _end: self.widget.after(round(t)+1, self.done)
            t+=time

    def _widget_number(self, option:str, start:int, end:int):
        self._number(option, start, end, self.widget.configure)

    def _widget_color(self, option:str, start:str, end:str):
        self._color(option, start, end, self.widget.configure)

    def _widget_special(self, option:str, start:int, end:int):
        self._special(option, start, end, self.widget.place)

    def __run_widget(self):
        for o in self.options:
            number = [
                'bd',
                'border',
                'borderwidth',
                'height',
                'highlightthickness',
                'padx',
                'pady',
                'width',
                'wraplength'
            ]
            color = [
                'activebackground',
                'activeforeground',
                'background ',
                'bg',
                'disabledforeground',
                'fg',
                'foreground',
                'highlightbackground',
                'highlightcolor'
            ]
            special = [
                'x',
                'y'
            ]
            if o in number: self._widget_number(o, int(str(self.start.get(o))), int(str(self.end.get(o))))
            elif o in color: self._widget_color(o, self.start.get(o), self.end.get(o))
            elif o in special: self._widget_special(o, self.start.get(o), self.end.get(o))
            else: print('Unknown option "%s"'%o)
        return self

    def _item_number(self, option:str, start:int, end:int):
        self._number(option, start, end, self.widget.configure)

    def _item_color(self, option:str, start:str, end:str):
        self._color(option, start, end, self.widget.configure)

    def _item_special(self, option:str, start:int, end:int):
        self._special(option, start, end, lambda kw, tag=self.TagOrId: self.widget.moveto(tag, **kw))

    def __run_item(self):
        for o in self.options:
            number = []
            color = [
                'fill',
                'activefill'
            ]
            special = [
                'x',
                'y',
                'width',
                'height'
            ]
            tween = None
            if o in number: tween = Tween('item_number', int(str(self.start.get(o))), int(str(self.end.get(o))))
            elif o in color: self._item_color(o, self.start.get(o), self.end.get(o))
            elif o in special: 
                print(self.start, self.end)
                self._item_special(o, self.start.get(o), self.end.get(o))
            else: print('Unknown option "%s"'%o)

            if self.stepcommand != None: self.stepcommand(o, tween)

            # if o in number: self._item_number(o, int(str(self.start.get(o))), int(str(self.end.get(o))))
            # elif o in color: self._item_color(o, self.start.get(o), self.end.get(o))
            # elif o in special: 
            #     print(self.start, self.end)
            #     self._item_special(o, self.start.get(o), self.end.get(o))
            # else: print('Unknown option "%s"'%o)
        return self

    def run(self):
        """Run the fx"""
        self.locked = True
        
        if self.progresscommand !=None: self.progresscommand(self.anim, self.anim.__progress, self.anim.__remainingms)

        if self.TagOrId == None: return self.__run_widget()
        else: return self.__run_item()
        # self.progresscommand()

def opacity_color(opacity:str, color1:str, color2:str):  
    """
    color1 - The widget color

    color2 - The master (bg) color
    """  
    _color = Color(_color(color2))
    colors = list(_color.range_to(Color(_color(color1)), 100))
    count = 0
    for c in colors:
        if count > (opacity*100): return c
        count +=1
    return c

# TODO:
# clear_queue
# delay
# dequeue
# finish
# queue
# stop
# fade_in # Needs more work
# fade_out # Needs more work

class Animation():
    def __init__(self, widget:tkinter.Widget, TagOrId:str=None):
        """
        Universal tkinter animations for Widgets, and Canvas items

        Arguments
        ---        
        `widget` - The widget to bind the animation to.

        `TagOrId` - The tkinter.Canvas item tag or id. WIDGET must be the canvas.
        """
        self.widget = None
        self.TagOrId = None
        self.visable = True
        self._queue = []
        self.running = None # queue is running
        self.__progress = 0
        self.__remainingms = 0

        self.configure(
            widget=widget,
            TagOrId=TagOrId
        )

    def configure(self, **kw):
        if 'widget' in kw and kw['widget']!=None:
            self.widget:tkinter.Widget = kw['widget']
            self.widget.update_idletasks()
            self.x = self.widget.winfo_x()
            self.y = self.widget.winfo_y()
            self.width = self.widget.winfo_width()
            self.height = self.widget.winfo_height()
            self.color = self.widget['bg']

        if 'TagOrId' in kw and kw['TagOrId']!=None:
            if isinstance(self.widget, tkinter.Canvas): self.TagOrId = kw['TagOrId']
            else:
                raise TkinterPlusError('WIDGET must be tkinter.Canvas to use TAGORID but got "%s"'%self.widget.__class__.__name__)
    config = configure

    # Basics

    def hide(self, duration:int=0, easing:Ease=Ease.LINEAR, stepcommand=None, progresscommand=None, donecommand=None):
        """
        Hide the matched widgets.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        """
        self.widget.place_forget() # Save values before hiding
        self.visable = False
        if donecommand!=None: donecommand(self)
        return self

    def show(self, duration:int=0, easing:Ease=Ease.LINEAR, stepcommand=None, progresscommand=None, donecommand=None):
        """Display the matched widgets.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        """
        self.widget.place(x=self.x, y=self.y)
        self.visable = True
        if donecommand!=None: donecommand(self)
        return self

    def toggle(self, duration:int=0, easing:Ease=Ease.LINEAR, stepcommand=None, progresscommand=None, donecommand=None):
        """Display or hide the matched widgets.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        """
        if self.visable: self.hide(duration, easing, donecommand)
        else: self.show(duration, easing, donecommand)
        return self

    # Custom

    def animate(self, duration:int=400, easing:Ease=Ease.LINEAR, queue:bool=True, stepcommand=None, progresscommand=None, donecommand=None, **properties):
        """Perform a custom animation of a set of CSS properties.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        """
        item = fx(self, self.widget, self.TagOrId, queue=queue, duration=duration, easing=easing, stepcommand=stepcommand, progresscommand=progresscommand, donecommand=donecommand, options=properties) # parse properties
        if self.TagOrId == None: # Widget
            for prop in properties:
                match prop:
                    case 'x': item.start[prop] = self.widget.winfo_x()
                    case 'y': item.start[prop] = self.widget.winfo_y()
                    case _: item.start[prop] = self.widget.cget(prop) # Save default properties
        else: # Canvas Item
            for prop in properties:
                match prop:
                    case 'x':
                        x0, y0, x1, y1 = self.widget.bbox(self.TagOrId)
                        item.start[prop] = x0
                    case 'y': 
                        x0, y0, x1, y1 = self.widget.bbox(self.TagOrId)
                        item.start[prop] = y0
                    case _:
                        item.start[prop] = self.widget.itemcget(self.TagOrId, prop)

        # Apply to queue or run
        if queue:
            self._queue.append(item)
            self.dequeue() # Start
        else: item.run()
        return self
        
    def clear_queue(self, name:str='fx'):
        """Remove from the queue all iteduration  that have not yet been run.
        
        Arguments
        ---
        `name` - A string containing the name of the queue. Defaults to fx, the standard effects queue.
        """
        for i in self._queue:
            if i.running == False: del i

    def delay(self, duration:int, name:str='fx'):
        """Set a timer to delay execution of subsequent iteduration  in the queue.
        
        Arguments
        ---
        `duration ` - An integer indicating the number of milliseconds to delay execution of the next item in the queue.

        `name` - A string containing the name of the queue. Defaults to fx, the standard effects queue.
        """
        pass

    def dequeue(self, name:str='fx'):
        """Execute the next function on the queue for the matched widgets.
        
        Arguments
        ---
        `name` - A string containing the name of the queue. Defaults to fx, the standard effects queue.
        """
        if self.running == None and len(self._queue) >= 1:
            i=0
            for fx in self._queue:
                if fx.name == name:
                    self.running = fx
                    del self._queue[i]
                    return self.running.run()
                i+=1

    def finish(self, queue:str='fx'):
        """Stop the currently-running animation, remove all queued animations, and donecommand all animations for the matched widgets.
        
        Arguments
        ---
        `queue` - The name of the queue in which to stop animations.
        """

    def queue(self, name:str='fx'):
        """Show or manipulate the queue of functions to be executed on the matched widgets.
        
        Arguments
        ---
        `name` - A string containing the name of the queue. Defaults to fx, the standard effects queue.
        """
        pass

    def stop(self, name:str='fx', stop_queue:bool=False, jump_to_end:bool=False):
        """Stop the currently-running animation on the matched widgets.
        
        Arguments
        ---
        `stop_queue` - A Boolean indicating whether to remove queued animation as well. Defaults to false.

        `jump_to_end ` - A Boolean indicating whether to donecommand the current animation immediately. Defaults to false.
        """
        pass

    # Fading
    # TODO: default: show()
    def fade_in(self, duration:int=400, easing:Ease=Ease.LINEAR, queue:bool=True, stepcommand=None, progresscommand=None, donecommand=None):
        """Display the matched widgets by fading them to opaque.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        
        `queue` - A Boolean indicating whether to place the animation in the effects queue. If false, the animation will begin immediately.
        """
        self.animate(duration, easing, donecommand, opacity=1.0)

    # TODO: deafult: hide()
    def fade_out(self, duration:int=400, easing:Ease=Ease.LINEAR, queue:bool=True, stepcommand=None, progresscommand=None, donecommand=None):
        """Hide the matched widgets by fading them to transparent.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        
        `queue` - A Boolean indicating whether to place the animation in the effects queue. If false, the animation will begin immediately.
        """
        return self

    def fade_to(self, opacity:float, duration:int=400, easing:Ease=Ease.LINEAR, stepcommand=None, progresscommand=None, donecommand=None):
        """Adjust the opacity of the matched widgets.
        
        Arguments
        ---
        `opacity` - A number between 0 and 1 denoting the target opacity.

        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        """
        return self

    def fade_toggle(self, duration:int=400, easing:Ease=Ease.LINEAR, queue:bool=True, stepcommand=None, progresscommand=None, donecommand=None):
        """Display or hide the matched widgets by animating their opacity.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        
        `queue` - A Boolean indicating whether to place the animation in the effects queue. If false, the animation will begin immediately.
        """
        if self.visable: self.fade_out(duration, easing, queue, donecommand)
        else: self.fade_in(duration, easing, queue, donecommand)
        return self

    # Sliding
    def slide_down(self, duration:int=400, easing:Ease=Ease.LINEAR, queue:bool=True, stepcommand=None, progresscommand=None, donecommand=None):
        """Display the matched widgets with a sliding motion.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        
        `queue` - A Boolean indicating whether to place the animation in the effects queue. If false, the animation will begin immediately.
        """
        self.animate(duration=duration, easing=easing, donecommand=donecommand, y=100)
        return self

    # TODO: default: hide()
    def slide_up(self, duration:int=400, easing:Ease=Ease.LINEAR, queue:bool=True, stepcommand=None, progresscommand=None, donecommand=None):
        """Hide the matched widgets with a sliding motion.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        
        `queue` - A Boolean indicating whether to place the animation in the effects queue. If false, the animation will begin immediately.
        """
        if donecommand==None: donecommand = lambda e: self.hide()
        self.animate(duration=duration, easing=easing, donecommand=donecommand, y=100)
        return self

    def slide_toggle(self, duration:int=400, easing:Ease=Ease.LINEAR, queue:bool=True, stepcommand=None, progresscommand=None, donecommand=None):
        """Display or hide the matched widgets with a sliding motion.
        
        Arguments
        ---
        `duration ` - A string or number determining how long the animation will run.

        `easing ` - A string indicating which easing function to use for the transition.

        `donecommand` - A function to call once the animation is donecommand, called once per matched element.
        
        `queue` - A Boolean indicating whether to place the animation in the effects queue. If false, the animation will begin immediately.
        """
        if self.visable: self.slide_down(duration, easing, queue, donecommand)
        else: self.slide_up(duration, easing, queue, donecommand)
        return self