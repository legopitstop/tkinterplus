from tkinter import EW, Message, Button, StringVar, Tk
from tkinterplus import Accordion
import os

LOCAL = os.path.dirname(os.path.realpath(__file__))

#TODO Add handle cursor to header

root = Tk()
root.minsize(500,300)

section1 = 'Mauris mauris ante, blandit et, ultrices a, suscipit eget, quam. Integer ut neque. Vivamus nisi metus, molestie vel, gravida in, condimentum sit amet, nunc. Nam a nibh. Donec suscipit eros. Nam mi. Proin viverra leo ut odio. Curabitur malesuada. Vestibulum a velit eu ante scelerisque vulputate.'
section2 = 'Sed non urna. Donec et ante. Phasellus eu ligula. Vestibulum sit amet purus. Vivamus hendrerit, dolor at aliquet laoreet, mauris turpis porttitor velit, faucibus interdum tellus libero ac justo. Vivamus non quam. In suscipit faucibus urna.'
section3 = 'Nam enim risus, molestie et, porta ac, aliquam ac, risus. Quisque lobortis. Phasellus pellentesque purus in massa. Aenean in pede. Phasellus ac libero ac tellus pellentesque semper. Sed ac felis. Sed commodo, magna quis lacinia ornare, quam ante aliquam nisi, eu iaculis leo purus venenatis dui.'
section4 = 'Cras dictum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aenean lacinia mauris vel est.\n\nSuspendisse eu nisl. Nullam ut libero. Integer dignissim consequat lectus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.'

test = StringVar() # Track which sections are open. Like a Radiobutton

widget = Accordion(root, text='Section 1', name='1', variable=test)
Message(widget, text=section1).pack(expand=True)
widget.grid(row=0,column=0, sticky=EW, padx=20, pady=4)

widget1 = Accordion(root, text='Section 2', name='2', variable=test)
Message(widget1, text=section2).pack(expand=True)
widget1.grid(row=1,column=0, sticky=EW, padx=20, pady=4)

widget2 = Accordion(root, text='Section 3', name='3', variable=test)
Message(widget2, text=section3).pack(expand=True)
widget2.grid(row=2,column=0, sticky=EW, padx=20, pady=4)

widget3 = Accordion(root, text='Section 4', name='4', variable=test)
Message(widget3, text=section4).pack(expand=True)
widget3.grid(row=3,column=0, sticky=EW, padx=20, pady=4)

Button(root, text='Click Me!', command=lambda: print('Opened', test.get())).grid(row=4,column=0)

# Responsive
root.grid_columnconfigure(0, weight=1)
root.mainloop()