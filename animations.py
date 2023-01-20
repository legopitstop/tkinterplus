from tkinter import *
from tkinterplus import FAST, SLOW, Animation, Ease
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

root = Tk()
root.title('Animations')
root.minsize(400,400)
# root.configure(bg='#f0f0f0')

# frame1 = Label(root, text='Block1', width=10, bg='red', highlightbackground='green')
frame1 = Label(root, text='Block1', width=10, bg='red', highlightbackground='green')
frame1.place(x=0,y=0)

frame2 = Label(root, text='Block2', width=10, bg='green', highlightbackground='red')
frame2.place(x=0,y=50)

anim1 = Animation(frame1)
anim2 = Animation(frame2)

def block1():
    anim1.animate(width=20, queue=False, duration=3000)
    anim1.animate(highlightthickness=10, duration=1500)
    anim1.animate(highlightbackground='darkgreen', duration=1500)
    
def block2():
    # def step(now:int, fx:Animation):
    #     data = f'{fx.widget} {fx.prop}: {now}'
    #     print(data)

    # anim2.animate(width=20, duration=1000)
    # anim2.animate(highlightthickness=10, duration=1000, stepcommand=step)
    # anim2.animate(highlightbackground='darkred', duration=1000)
    anim2.slide_toggle()

def canvas3():
    anim3.animate(y=150, duration=SLOW, easing=Ease.BOUNCE_OUT)

def reset():
    frame1.configure(width=10, highlightthickness=0, highlightbackground='green')
    frame2.configure(width=10, highlightthickness=0, highlightbackground='red')
    frame1.place(x=0,y=0)
    frame2.place(x=0,y=50)
    canvas.pack(fill='both', expand=1)
    canvas.moveto(item, 0, 0)

def all():
    block1()
    block2()
    canvas3()

Button(root, text='Block1', command=block1).pack()
Button(root, text='Block2', command=block2).pack()
Button(root, text='Canvas', command=canvas3).pack()
Button(root, text='All', command=all).pack()
Button(root, text='Reset', command=reset).pack()
canvas = Canvas(root, width=200, height=200, bg='black')
item = canvas.create_rectangle(1, 1, 100, 100, fill='white')
canvas.pack(fill='both', expand=1)
anim3 = Animation(canvas, item)

# Responsive
root.grid_columnconfigure(0, weight=1)
root.mainloop()