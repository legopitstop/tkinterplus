from tkinterplus.experimental import Audio
import os
import tkinter

LOCAL = os.getcwd()

root = tkinter.Tk()
root.title("Audio")
root.minsize(500, 500)

# TODO
# - make this use winsound if platform is Windows.
# - Only plays once, then stops
widget = Audio(root)
widget.open(os.path.join(LOCAL, "tests", "assets", "images", "sound.ogg"))
widget.grid(row=0, column=0, sticky="ew")

widget2 = Audio(root)
widget2.open(os.path.join(LOCAL, "tests", "assets", "images", "sound.wav"))
widget2.grid(row=1, column=0, sticky="ew")

root.grid_columnconfigure(0, weight=1)
root.configure(padx=10, pady=10)
root.mainloop()
