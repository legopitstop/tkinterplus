from tkinterplus.experimental import askeditimage
import tkinter

# Add widgets to DeveloperTools
# add_widget(Treeview)

root = tkinter.Tk()
root.title("Developer Tools")
root.minsize(500, 500)


def open():
    image = askeditimage(root, "Edit Image")
    print(image)


tkinter.Button(root, text="Open Image", command=open).pack()

root.mainloop()
