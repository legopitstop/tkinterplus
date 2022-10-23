from math import cos, pi, radians, sin
import math

rx = lambda v, angle : (v[0],(cos(radians(angle))*v[1]) + ((-sin(radians(angle)))*v[2]),
                             (sin(radians(angle))*v[1]) + ((cos(radians(angle)))*v[2]))

ry = lambda v, angle : (((cos(radians(angle)))*v[0]) + ((-sin(radians(angle)))*v[1]), v[2],
                        ((sin(radians(angle)))*v[0]) + ((cos(radians(angle)))*v[1]))

rz = lambda v, angle : (((cos(radians(angle)))*v[0]) + ((-sin(radians(angle)))*v[1]),
                        ((sin(radians(angle)))*v[0]) + ((cos(radians(angle)))*v[1]), v[2])
class shape:
    def __init__(self, file, canvas):
        self.location, self.scale = [0, 0, 0], 1
        self.rotation = [0, 0, 0]
        self.canvas = canvas
        self.EdgeThickness = 1
        self.color="#ffffff"
        self.width = int(self.canvas["width"])
        self.height = int(self.canvas["height"])

        self.lines=[]
        self.add_face((0,0,0),(2,0,0),(0,2,0),(2,2,0))
        self.add_face((0,0,2),(2,0,2),(0,2,2),(2,2,2))
        self.add_face((0,2,2),(2,2,2),(0,2,0),(2,2,0))
        self.add_face((0,0,2),(2,0,2),(0,0,0),(2,0,0))
        self.add_face((0,0,0),(0,0,2),(0,2,0),(0,2,2))
        self.add_face((2,0,0),(2,0,2),(2,2,0),(2,2,2))

    def add_face(self,v1,v2,v3,v4):
            vertex = [
                ((v2[1], v2[0], v2[2]), (v1[1], v1[0], v1[2])),
                ((v1[1], v1[0], v1[2]), (v3[1], v3[0], v3[2])),
                ((v3[1], v3[0], v3[2]), (v4[1], v4[0], v4[2])),
                ((v4[1], v4[0], v4[2]), (v2[1], v2[0], v2[2]))
            ]
            for l in vertex:
                self.lines.append(l)
        

    # ADDED
    def render(self):
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
        vr = list(map(lambda v:(add(self.location, rz(ry(rx(v[0], self.rotation[0]), self.rotation[1]), self.rotation[2])),add(self.location, rz(ry(rx(v[1], self.rotation[0]), self.rotation[1]), self.rotation[2]))),self.lines))
        for l in vr: self.canvas.create_line(xcor(l[0][0], l[0][1]), ycor(l[0][2], l[0][1]), xcor(l[1][0], l[1][1]), ycor(l[1][2], l[1][1]), fill=self.color, width=self.EdgeThickness)

if __name__=='__main__':
    from tkinter import *
    import os

    LOCAL = os.path.dirname(os.path.realpath(__file__))

    root = Tk()
    c=Canvas(root)
    c.grid(row=0,column=0,sticky='nesw')
    c.configure(background='black')

    root.grid_rowconfigure(0,weight=1)
    root.grid_columnconfigure(0,weight=1)

    def clear(): c.delete('all')

    s=shape(LOCAL+'/cube.obj',c)

    s.color = 'white'
    s.scale=0.5
    s.location[1]=10
    s.rotation[1]=90

    s.old_x=0
    s.old_y=90
    s.pan_x=0
    s.pan_y=0

    # BINDS

    def rotate(e:Event):
        clear()
        if e.keycode==88:s.rotation[0]+=5
        elif e.keycode==89:s.rotation[1]+=5
        elif e.keycode==90:s.rotation[2]+=5
        s.render()

    def rotateMotion(e:Event):
        clear()
        dX = (e.x-s.old_x)*2*math.pi/c.winfo_width()
        dY = (e.y-s.old_y)*2*math.pi/c.winfo_height()
        # THETA+= dX;
        # PHI+=dY;
        s.old_x = e.x
        s.old_y = e.y

        s.rotation[0] -= dX
        s.rotation[1] -= dY

        print(s.rotation)
        s.render()

    def panMotion(e:Event):
        clear()
        dX = (e.x-s.pan_x)*math.pi/c.winfo_width()
        dY = (e.y-s.pan_y)*math.pi/c.winfo_height()

        
        s.pan_x = e.x
        s.pan_y = e.y


        s.location[0] += dX
        s.location[2] -= dY

        print(s.location)

        s.render()

    def zoomMotion(e:Event):
        clear()
        if e.delta>=120:
            s.scale+=0.1
        else:
            s.scale-=0.1
        print(s.scale)
        s.render()

    root.bind('<KeyPress>',rotate)
    root.bind('<B1-Motion>',rotateMotion)
    root.bind('<MouseWheel>',zoomMotion)
    root.bind('<B3-Motion>',panMotion)
    s.render()

    # Right drag = pan
    # Left drag = spin
    # scroll = zoom

    root.mainloop()
