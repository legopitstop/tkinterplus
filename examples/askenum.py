from tkinterplus import askenum
import tkinter


def main():
    root = tkinter.Tk()
    root.title("askenum")
    root.minsize(500, 500)

    def callback():
        print(askenum(root, "Select an option", ["Option 1", "Option 2", "Option 3"]))

    button = tkinter.Button(root, text="Ask Enum", command=callback)
    button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
