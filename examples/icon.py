from tkinter import LEFT, Tk, Button
from tkinterplus import Asset, Icon, MaterialIcon
from dotenv import load_dotenv
load_dotenv() # load .env file that has the github personal access token: GITHUB_TOKEN = 'YOUR_TOKEN'

root = Tk()
root.title('Icon')
root.minsize(200,200)

# Load an image from disk
icon = Icon(Asset.TK_PLUME, size=(64, 64))
Button(root, text='Hello World', image=icon, compound=LEFT).pack()

# Load a Google Material icon
icon2 = MaterialIcon('person', size=(64, 64))
Button(root, text='Hello World', image=icon2, compound=LEFT).pack()

root.mainloop()