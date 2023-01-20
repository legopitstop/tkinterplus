from math import cos, pi, radians, sin
from tkinter import SE, Canvas, Event, PhotoImage, Tk, Widget
import numpy
from PIL import Image, ImageTk

import pyautogui
# from tktooltip import ToolTip
from typing_extensions import TypeAlias

# Look into using graphic API engines
# - DirectX
# - OpenGL

# TODO
# - Fix 'location' should be xyz instead of xzy
# - Add pivot `origin` att. by default it will find the middle of the model.
# - Render method for texture placement on rectangles. opaque|cutout|blend (Use minetest as an example)

rx = lambda v, angle : (v[0],(cos(radians(angle))*v[1]) + ((-sin(radians(angle)))*v[2]),(sin(radians(angle))*v[1]) + ((cos(radians(angle)))*v[2]))
ry = lambda v, angle : (((cos(radians(angle)))*v[0]) + ((-sin(radians(angle)))*v[1]), v[2],((sin(radians(angle)))*v[0]) + ((cos(radians(angle)))*v[1]))
rz = lambda v, angle : (((cos(radians(angle)))*v[0]) + ((-sin(radians(angle)))*v[1]),((sin(radians(angle)))*v[0]) + ((cos(radians(angle)))*v[1]), v[2])

_Color: TypeAlias = str  # typically '#rrggbb', '#rgb' or color names.

class _create():
    def __init__(self,itemType,*cords:tuple,**kw):
        """Defines the item"""
        self.cords=cords
        self.itemType = itemType
        self.kw = kw

class CanvasError(Exception): pass

#TODO
# - Make it also work for regular 2D canvas?
class Animation():
    def __init__(self):
        """Create a key-frame animation for the canvas item"""
        pass

# TEMP
class Asset():
    def __init__(self, color:str=None, image:str=None):
        """The asset for the face"""
        self.color = color
        self.iamge = image

class Vec3():
    def __init__(self,x,y,z):
        """Defines 3 coordnates for the 3D space"""
        self.x=x
        self.y=y
        self.z=z
    def __enter__(self):
        return (self.x, self.y, self.z)

class Vec6():
    def __init__(self,x1,y1,z1, x2,y2,z2):
        """Describes 6 coordnates (2 sets of 3) for the 3D space"""
        self.x1=x1
        self.y1=y1
        self.z1=z1
        self.x2=x2
        self.y2=y2
        self.z2=z2
    def __enter__(self):
        return (self.x1,self.y1,self.z1, self.x2,self.y2,self.z2)

#NOTE This widget is still being worked on. Expect issues for missing features!
class Canvas3D(Widget):
    def __init__(self,master:Tk, cnf={}, **kw):
        """Construct a canvas3D widget with the parent MASTER."""
        self.master = master
        self.gizmo = None
        self.canvas = Canvas(master,cnf,**kw)
        self.location = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.origin = [0, 0, 0] #TODO Center where it rotates around
        self.items=[]

        self.width = 0
        self.height = 0
        self.color= 'white'
        self.EdgeThickness=1

        self.old_loc = [0,0,0]
        self.old_rot = [0,0,0]

        # _mouse_direction
        self.mouse_pos = None

    def find_coeffs(self,pa, pb):
        """For textures"""
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

        A = numpy.matrix(matrix, dtype=float)
        B = numpy.array(pb).reshape(8)

        res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
        return numpy.array(res).reshape(8)

    def bind_rotation(self, x1='<x>', y1='<y>', z1='<z>', x2='<X>', y2='<Y>', z2='<Z>'):
        """sequences for each rotation axis"""
        if x1!=None: self.canvas.bind_all(x1, lambda e: self._rotateEvent('x', e))
        if y1!=None: self.canvas.bind_all(y1, lambda e: self._rotateEvent('y', e))
        if z1!=None: self.canvas.bind_all(z1, lambda e: self._rotateEvent('z', e))
        if x2!=None: self.canvas.bind_all(x2, lambda e: self._rotateEvent('-x', e))
        if y2!=None: self.canvas.bind_all(y2, lambda e: self._rotateEvent('-y', e))
        if z2!=None: self.canvas.bind_all(z2, lambda e: self._rotateEvent('-z', e))

    def bind_movement(self, x1='<Right>', y1='<Up>', z1='<MouseWheel>', x2='<Left>', y2='<Down>', z2=None):
        """sequences for each movement axis"""
        if x1!=None: self.canvas.bind_all(x1, lambda e: self._moveEvent('x',e))
        if y1!=None: self.canvas.bind_all(y1, lambda e: self._moveEvent('y',e))
        if z1!=None: self.canvas.bind_all(z1, lambda e: self._moveEvent('z',e))
        if x2!=None: self.canvas.bind_all(x2, lambda e: self._moveEvent('-x',e))
        if y2!=None: self.canvas.bind_all(y2, lambda e: self._moveEvent('-y',e))
        if z2!=None: self.canvas.bind_all(z2, lambda e: self._moveEvent('-z',e))

    def controls(self, type:str=None, **kw):
        """Bind the default controls to the canvas."""
        self.bind_movement()
        self.bind_rotation()

    # def orbit_gizmo(self,x:_Color='red',y:_Color='green',z:_Color='blue', selectX:_Color='darkred',selectY:_Color='darkgreen',selectZ:_Color='darkblue',hoverColor:_Color=None,**kw):
    #     """Adds a thing in the bottom right of the canvas used to control the rotation of the canvas"""
    #     self.gizmo = OrbitGizmo(self.canvas, x,y,z,selectX,selectY,selectZ,hoverColor,**kw)
    #     self.gizmo.update(self.rotation)

    def _rotateEvent(self,axis, e:Event):
        self.delete("all")
        if axis=='x': self.rotation[0]+=5
        if axis=='y': self.rotation[2]+=5
        if axis=='z': self.rotation[1]+=5
        if axis=='-x': self.rotation[0]-=5
        if axis=='-y': self.rotation[2]-=5
        if axis=='-z': self.rotation[1]-=5
        self._draw()

    def _moveEvent(self,axis, e:Event):
        self.delete("all")
        if axis=='x': self.location[0]+=0.5
        if axis=='y': self.location[2]+=0.5
        if axis=='z':
            if e.type=='38': # Custom behavior for <MouseWheel>
                if e.delta > 1:self.location[1]-=0.5
                else: self.location[1]+=0.5
            else: self.location[1]+=0.5
        if axis=='-x': self.location[0]-=0.5
        if axis=='-y': self.location[2]-=0.5
        if axis=='-z':
            if e.type=='38': # Custom behavior for <MouseWheel>
                if e.delta > 1:self.location[1]-=0.5
                else: self.location[1]+=0.5
            else: self.location[1]-=0.5
        self._draw()

    def delete(self,*args):
        """Delete items identified by all tag or ids contained in ARGS."""
        self.canvas.delete(*args)

    # Create items

    # oval -> ovoid
    # rectangle -> cuboid

    def create_arc(self,vec1:Vec3,vec2:Vec3,**kw):
        """
        BROKEN
        Create arc shaped region with coordinates vec1, vec2, vec3, vec4.
        """
        c = _create('arc', vec1,vec2,**kw)
        self.items.append(c)
        return c

    def create_bitmap(self,vec1:Vec3,vec2:Vec3, bitmap):
        """
        BROKEN            
        Create bitmap with coordinates x1,y1.
        """
        c = _create('bitmap', vec1, vec2, bitmap=bitmap)
        self.items.append(c)
        return c

    def create_image(self,vec1:Vec3, vec2:Vec3, image):
        """Create image item with coordinates vec1, vec2."""
        c = _create('image', vec1,vec2, image=image)
        self.items.append(c)
        return c

    def create_line(self,vec1:Vec3,vec2:Vec3,**kw):
        """Create line with coordinates vec1, vec2."""
        c = _create('line', vec1, vec2, **kw)
        self.items.append(c)
        return c

    def create_oval(self,vec1:Vec3,vec2:Vec3,**kw):
        """Create oval with coordinates vec1,vec2."""
        c = _create('oval', vec1, vec2,**kw)
        self.items.append(c)
        return c

    def create_polygon(self, *vec:Vec3,**kw):
        """
        BROKEN
        Create polygon with coordinates vec.
        """
        c = _create('polygon',*vec,**kw)
        self.items.append(c)
        return c

    def _get_faces(self, faces):
        """Returns with each side of the face in a tuple (north, south, east, west, top, bottom)"""
        max_index = len(faces)
        if max_index <= 6:
            f = []
            for i in range(7):
                try: f.append(faces[i])
                except IndexError: f.append(faces[max_index-1])
            return f[0], f[1], f[2], f[3], f[4], f[5]
        else: raise CanvasError('Too many faces. expected 1-6')

    def create_rectangle(self,vec1:Vec3,vec2:Vec3,assets:tuple=None,**kw):
        """Create rectangle with coordinates vec1, and vec2."""
        if assets!=None:  ASSET = self._get_faces(assets)
        else: ASSET = (None, None, None, None, None, None)
        self.create_face((vec2[0], vec2[1], vec2[2]), (vec2[0], vec2[1], vec1[2]), (vec1[0], vec2[1], vec2[2]), (vec1[0], vec2[1], vec1[2]), asset=ASSET[5], **kw) # BOTTOM
        self.create_face((vec2[0], vec1[1], vec2[2]), (vec2[0], vec1[1], vec1[2]), (vec1[0], vec1[1], vec2[2]), (vec1[0], vec1[1], vec1[2]), asset=ASSET[4], **kw) # TOP
        self.create_face((vec1[0], vec2[1], vec2[2]), (vec1[0], vec2[1], vec1[2]), (vec1[0], vec1[1], vec2[2]), (vec1[0], vec1[1], vec1[2]), asset=ASSET[3], **kw) # WEST
        self.create_face((vec2[0], vec2[1], vec2[2]), (vec2[0], vec2[1], vec1[2]), (vec2[0], vec1[1], vec2[2]), (vec2[0], vec1[1], vec1[2]), asset=ASSET[2], **kw) # EAST
        self.create_face((vec2[0], vec2[1], vec2[2]), (vec1[0], vec2[1], vec2[2]), (vec2[0], vec1[1], vec2[2]), (vec1[0], vec1[1], vec2[2]), asset=ASSET[1], **kw) # SOUTH
        self.create_face((vec2[0], vec2[1], vec1[2]), (vec1[0], vec2[1], vec1[2]), (vec2[0], vec1[1], vec1[2]), (vec1[0], vec1[1], vec1[2]), asset=ASSET[0], **kw) # NORTH

    def create_text(self,vec1:Vec3,text,**kw):
        """Create text with coordinates vec1, vec2."""
        c = _create('text', vec1,vec1,text=text,**kw)
        self.items.append(c)
        return c

    def create_window(self, vec1:Vec3,window,**kw):
        """Create window with coordinates vec1, vec2."""
        c = _create('window', vec1, vec1, window=window,**kw)
        self.items.append(c)
        return c

    def create_face(self,v1:Vec3,v2:Vec3, v3:Vec3,v4:Vec3,**kw):
        """
        Create face with coordinates v1,v2,v3,v4. image is the PhotoImage to fill the face with.
        """
        print(kw['asset'])
        del kw['asset'] # This should fill the face with this.

        self.create_line((v2[0], v2[1], v2[2]), (v1[0], v1[1], v1[2]), **kw)
        self.create_line((v1[0], v1[1], v1[2]), (v3[0], v3[1], v3[2]), **kw)
        self.create_line((v3[0], v3[1], v3[2]), (v4[0], v4[1], v4[2]), **kw)
        self.create_line((v4[0], v4[1], v4[2]), (v2[0], v2[1], v2[2]), **kw)

    def draw(self):
        """Updates the canvas with new drawing"""
        self.master.update()
        self._draw()
    
    def _draw(self):
        if self.gizmo!=None:
            self.gizmo.update(self.rotation)

        self.width = int(self.canvas.winfo_width())
        self.height = int(self.canvas.winfo_height())
        u=int(self.width/16)
        fl=0.15
        def xcor(x, y):
            try:
                if (x<0): return (self.width/2)-(x/(y*fl))*(-1*u)
                else: return (self.width/2)+(x/(y*fl))*u
            except(ZeroDivisionError):return 0
        def ycor(z, y):
            try:
                if (z<0): return (self.height/2)-(z/(y*fl))*u
                else: return (self.height/2)+(z/(y*fl))*(-1*u)
            except(ZeroDivisionError):return 0

        add = lambda x, y:tuple(map(lambda a, b:a+b, x, y))

        for item in self.items:
            item:_create = item # TEMP used for attbutes
            vr = list(map(lambda v:(add(self.location, rz(ry(rx(v[0], self.rotation[0]), self.rotation[1]), self.rotation[2])), add(self.location, rz(ry(rx(v[1], self.rotation[0]), self.rotation[1]), self.rotation[2]))),[item.cords]))
            index=0
            for l in vr:
                x1 = xcor(l[0][0], l[0][1])
                y1 = ycor(l[0][2], l[0][1])
                x2 = xcor(l[1][0], l[1][1])
                y2 = ycor(l[1][2], l[1][1])
                if item.itemType=='line': self.canvas.create_line(x1,y1,x2,y2, **item.kw)
                elif item.itemType=='oval': self.canvas.create_oval(x1,y1,x2,y2, **item.kw)
                elif item.itemType=='arc': self.canvas.create_arc(x1,y1,x2,y2, **item.kw)
                elif item.itemType=='polygon': self.canvas.create_polygon(x1,y1,x2,y2, **item.kw)
                elif item.itemType=='text': self.canvas.create_text(x1,y2, **item.kw)
                elif item.itemType=='window': self.canvas.create_window(x1,y2, **item.kw)
                elif item.itemType=='image':
                    # Add image kw to src
                    if 'image' in item.kw:
                        item.src = item.kw['image']
                        del item.kw['image']

                    # Modify image then apply to canvas
                    if item.src!=None:
                        img = Image.open(item.src)
                        # TopL = [0,0]
                        # TopR = [256,0]
                        # BottomL = [0,256]
                        # BottomR = [256,256]
                        
                        TopL = [x1,y1]
                        TopR = [1024,y1]
                        BottomL = [x1,1024]
                        BottomR = [1024,1024]

                        x3 = xcor(-l[1][0], -l[1][1])
                        y3 = ycor(l[0][2], l[0][1])
                        
                        x4 = xcor(-l[0][0], -l[0][1])
                        y4 = ycor(l[1][2], l[1][1])

                        # Each vertices
                        vertex1 = (x1,y1,x1,y1)
                        vertex2 = (x2,y2,x2,y2)
                        vertex3 = (x3,y3,x3,y3)
                        vertex4 = (x4,y4,x4,y4)

                        self.canvas.create_oval(vertex1, width=5, outline='red')
                        self.canvas.create_oval(vertex2, width=5, outline='red')
                        self.canvas.create_oval(vertex3, width=5, outline='blue')
                        self.canvas.create_oval(vertex4, width=5, outline='green')

                        coeffs = self.find_coeffs(
                            [(TopL[0], TopL[1]), (TopR[0], TopR[1]), (BottomR[0], BottomR[1]), (BottomL[0], BottomL[1])],
                            [(0,0), (256, 0), (256, 256), (0, 256)])
                        new_img=img.transform((256, 256), Image.PERSPECTIVE, coeffs,Image.BICUBIC)

                        self._img = ImageTk.PhotoImage(image=new_img)

                        self.canvas.create_image(x1,y1, image=self._img,**item.kw)

                    else: raise CanvasError('Missing image!')
                else: raise CanvasError('Invalid type: %s'%item.itemType)
                index+=1
    
    def get_items(self):
        """Returns a list of all the created items"""
        return self.items

    def show_origin(self):
        """Places a dot where the rotation origin is"""
        self.create_oval(self.origin,self.origin, outline='#fff', activeoutline='#aaa',width=10,tags='tkorigin')
        # self.tag_bind('tkorigin', '<Button-1>', lambda e: print('WORKED'))
        self.old_x=0
        self.old_y=0

        def on_move(e:Event):
            # dir = self._mouse_direction(e)
            x, y, xs, ys = self.canvas.coords('tkorigin')
            # print(x, y)
            # posX = x - e.x
            # posY = y - e.y

            self.canvas.move('tkorigin', e.x-x, e.y-y)
            print(e.x, e.y)

            # self.canvas.create_oval(e.x,e.y, e.x,e.y,width=10, outline='red')

            # self.location[0] += posX
            # self.location[2] += posY
            # self._draw()


        # self.tag_bind('tkorigin', '<B1-Motion>', on_move)
        self.bind('<B1-Motion>', on_move)

    # Regular Widget functions
    def move(self, *args): # location
        """Move an item TAGORID given in ARGS."""
        pass

    def rotate(self, *args): # rotation
        """Rotate an item TAGORID given in ARGS."""
        pass

    def grid_configure(self, cnf={}, **kw):
        """Position a widget in the parent widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this
                      widget stick to the cell boundary
        """
        self.canvas.grid_configure(cnf, **kw)

    def pack_configure(self, cnf={}, **kw):
        """Pack a widget in the parent widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to
                                  given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if parent size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
        """
        self.canvas.grid_configure(cnf, **kw)

    def place_configure(self, cnf={}, **kw):
        """Place a widget in the parent widget. Use as options:
        in=master - master relative to which the widget is placed
        in_=master - see 'in' option description
        x=amount - locate anchor of this widget at position x of master
        y=amount - locate anchor of this widget at position y of master
        relx=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to width of master (1.0 is right edge)
        rely=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to height of master (1.0 is bottom edge)
        anchor=NSEW (or subset) - position anchor according to given direction
        width=amount - width of this widget in pixel
        height=amount - height of this widget in pixel
        relwidth=amount - width of this widget between 0.0 and 1.0
                          relative to width of master (1.0 is the same width
                          as the master)
        relheight=amount - height of this widget between 0.0 and 1.0
                           relative to height of master (1.0 is the same
                           height as the master)
        bordermode="inside" or "outside" - whether to take border width of
                                           master widget into account
        """
        self.canvas.place_configure(cnf, **kw)
      
    def configure(self,cnf=None,**kw):
        """Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method keys.
        """
        return self.canvas.configure(cnf,**kw)
    
    def bind(self,sequence=None,func=None,add=None):
        """Bind to this widget at event SEQUENCE a call to function FUNC.

        SEQUENCE is a string of concatenated event
        patterns. An event pattern is of the form
        <MODIFIER-MODIFIER-TYPE-DETAIL> where MODIFIER is one
        of Control, Mod2, M2, Shift, Mod3, M3, Lock, Mod4, M4,
        Button1, B1, Mod5, M5 Button2, B2, Meta, M, Button3,
        B3, Alt, Button4, B4, Double, Button5, B5 Triple,
        Mod1, M1. TYPE is one of Activate, Enter, Map,
        ButtonPress, Button, Expose, Motion, ButtonRelease
        FocusIn, MouseWheel, Circulate, FocusOut, Property,
        Colormap, Gravity Reparent, Configure, KeyPress, Key,
        Unmap, Deactivate, KeyRelease Visibility, Destroy,
        Leave and DETAIL is the button number for ButtonPress,
        ButtonRelease and DETAIL is the Keysym for KeyPress and
        KeyRelease. Examples are
        <Control-Button-1> for pressing Control and mouse button 1 or
        <Alt-A> for pressing A and the Alt key (KeyPress can be omitted).
        An event pattern can also be a virtual event of the form
        <<AString>> where AString can be arbitrary. This
        event can be generated by event_generate.
        If events are concatenated they must appear shortly
        after each other.

        FUNC will be called if the event sequence occurs with an
        instance of Event as argument. If the return value of FUNC is
        "break" no further bound function is invoked.

        An additional boolean parameter ADD specifies whether FUNC will
        be called additionally to the other bound function or whether
        it will replace the previous function.

        Bind will return an identifier to allow deletion of the bound function with
        unbind without memory leak.

        If FUNC or SEQUENCE is omitted the bound function or list
        of bound events are returned."""
        return self.canvas.bind(sequence,func,add)
    
    def tag_bind(self, tagOrId, sequence=None, func=None, add=None):
        """Bind to all items with TAGORID at event SEQUENCE a call to function FUNC.

        An additional boolean parameter ADD specifies whether FUNC will be
        called additionally to the other bound function or whether it will
        replace the previous function. See bind for the return value."""
        return self.canvas.tag_bind(tagOrId, sequence, func, add)

    def tag_unbind(self, tagOrId, sequence, funcid=None):
        """Unbind for all items with TAGORID for event SEQUENCE  the
        function identified with FUNCID."""
        self.canvas.tag_unbind(tagOrId, sequence, funcid)
    
    def tag_lower(self, *args):
        """Lower an item TAGORID given in ARGS
        (optional below another item)."""
        self.canvas.tag_lower(*args)
    
    def tag_raise(self,*args):
        """Raise an item TAGORID given in ARGS
        (optional above another item)."""
        self.canvas.tag_raise(*args)

    def itemconfigure(self, tagOrId, cnf=None, **kw):
        """Configure resources of an item TAGORID.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method without arguments.
        """
        return self.canvas.itemconfigure(tagOrId, cnf, **kw)
    
    def after(self, ms, func=None, *args):
        """Call function once after given time.

        MS specifies the time in milliseconds. FUNC gives the
        function which shall be called. Additional parameters
        are given as parameters to the function call.  Return
        identifier to cancel scheduling with after_cancel."""
        return self.canvas.after(ms, func, *args)

    def raycast(self,recursive:int=100):
        """A simple raycast function. Returns a vec that contains the coords that the user is looking at."""
        # .find_withtag('current') gets the item under cursor
        # my_canvas.find_overlapping()
        for i in range(recursive):
            # Keep moving forward until it hits an item.
            pass
        return [None, None, None]

    # Atlas
    lift = tkraise = tag_raise
    lower = tag_lower
    grid = grid_configure
    pack = pack_configure
    place = place_configure
    config = configure
    itemconfig = itemconfigure

class Skybox():
    def __init__(self, canvas:Canvas3D, north:PhotoImage, east:PhotoImage, south:PhotoImage, west:PhotoImage, up:PhotoImage, down:PhotoImage):
        """Create a skybox for the canvas3D"""
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.up = up
        self.down = down
        self.rotation = [0,0,0]

class OrbitGizmo(Widget):
    def __init__(self,master:Canvas3D,x:_Color='red',y:_Color='green',z:_Color='blue', selectX:_Color='darkred',selectY:_Color='darkgreen',selectZ:_Color='darkblue',hoverColor:_Color=None,**kw):
        """Create a "Thing" in the bottom right corner of the canvas that shows the X, Y, Z rotation"""
        # Defaults
        self.color = master.canvas.cget('bg')

        # Variables
        self.hoverColor=hoverColor
        self.mouseX = 0
        self.mouseY = 0

        # Widgets
        self.gizmo = Canvas3D(master,width=100,height=100,highlightthickness=0,bg=self.color,**kw)
        self.gizmo.location = [0,1.5,0]

        self.gizmo.create_oval((1,0,0),(1,0,0),outline=selectX,activeoutline=x,width=10,tags='x1') # X
        self.gizmo.create_oval((0,1,0),(0,1,0),outline=selectY,activeoutline=y,width=10,tags='y1') # Y
        self.gizmo.create_oval((0,0,1),(0,0,1),outline=selectZ,activeoutline=z,width=10,tags='z1') # Z
        
        self.gizmo.create_oval((-1,0,0),(-1,0,0),outline=selectX,activeoutline=x,width=10,tags='x2') # -X
        self.gizmo.create_oval((0,-1,0),(0,-1,0),outline=selectY,activeoutline=y,width=10,tags='y2') # -Y
        self.gizmo.create_oval((0,0,-1),(0,0,-1),outline=selectZ,activeoutline=z,width=10,tags='z2') # -Z

        self.gizmo.create_line((0,0,0),(.9,0,0),fill=selectX,activefill=x,width=2,tags='x1') # X
        self.gizmo.create_line((0,0,0),(0,.9,0),fill=selectY,activefill=y,width=2,tags='y1') # Y
        self.gizmo.create_line((0,0,0),(0,0,.9),fill=selectZ,activefill=z,width=2,tags='z1') # Z

        self.gizmo.draw()

        # save
        self.gizmo.tag_bind('x1','<ButtonPress-1>', self.savePos)
        self.gizmo.tag_bind('y1','<ButtonPress-1>', self.savePos)
        self.gizmo.tag_bind('z1','<ButtonPress-1>', self.savePos)
        self.gizmo.tag_bind('x2','<ButtonPress-1>', self.savePos)
        self.gizmo.tag_bind('y2','<ButtonPress-1>', self.savePos)
        self.gizmo.tag_bind('z2','<ButtonPress-1>', self.savePos)

        # When moving
        self.gizmo.tag_bind('x1','<B1-Motion>', lambda e: self.on_select('x1'))
        self.gizmo.tag_bind('y1','<B1-Motion>', lambda e: self.on_select('y1'))
        self.gizmo.tag_bind('z1','<B1-Motion>', lambda e: self.on_select('z1'))
        self.gizmo.tag_bind('x2','<B1-Motion>', lambda e: self.on_select('x2'))
        self.gizmo.tag_bind('y2','<B1-Motion>', lambda e: self.on_select('y2'))
        self.gizmo.tag_bind('z2','<B1-Motion>', lambda e: self.on_select('z2'))
        
        # restore
        self.gizmo.tag_bind('x1','<ButtonRelease-1>', self.restorePos)
        self.gizmo.tag_bind('y1','<ButtonRelease-1>', self.restorePos)
        self.gizmo.tag_bind('z1','<ButtonRelease-1>', self.restorePos)
        self.gizmo.tag_bind('x2','<ButtonRelease-1>', self.restorePos)
        self.gizmo.tag_bind('y2','<ButtonRelease-1>', self.restorePos)
        self.gizmo.tag_bind('z2','<ButtonRelease-1>', self.restorePos)
        
        bd = master['highlightthickness']
        self.gizmo.place(rely=1.0, relx=1.0, x=-int(bd), y=-int(bd), anchor=SE)

        # Binds
        self.gizmo.bind("<Enter>", lambda e: self.on_enter())
        self.gizmo.bind("<Leave>", lambda e: self.on_leave())

    def savePos(self,e):
        """Saves the mouses position on the screen before moving"""
        # Hide mouse
        self.gizmo.config(cursor='none')
        # Save mouse pos
        pos = pyautogui.position()
        self.mouseX = pos.x
        self.mouseY = pos.y

    def restorePos(self,e):
        """Restores the mouses position that was saved"""
        # Show mouse
        self.gizmo.config(cursor='')
        # Move mouse back
        pyautogui.moveTo(self.mouseX, self.mouseY)

    def on_enter(self):
        self.gizmo.itemconfigure('gizmo_bg',fill=self.hoverColor,outline=self.hoverColor)

    def on_leave(self):
        self.gizmo.itemconfigure('gizmo_bg',fill=self.color,outline=self.color)

    def on_select(self,tag):
        """When the user selects the gizmo"""
        print(tag)

    def _update(self,rotation):
        """updates the gizmo's canvas and rotation"""
        self.gizmo.delete('all')
        self.gizmo.rotation = rotation
        self.gizmo._draw()
    
    def update(self,rotation):
        """updates the gizmo's rotation"""
        self.gizmo.delete('all')
        self.gizmo.canvas.create_oval(0,0,100,100,tags='gizmo_bg',fill=self.color,outline=self.color)
        self.gizmo.canvas.tag_lower('all', 'gizmo_bg')
        self.gizmo.rotation = rotation
        self.gizmo.draw()
