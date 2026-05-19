from tkinterplus import simpledialog
import tkinter


def main():
    root = tkinter.Tk()
    root.title("simpledialog")
    root.minsize(500, 500)
    root.configure(padx=10, pady=10)

    def dialog1():
        res = simpledialog.askopenurl(
            "Open Website", "https://example.com", parent=root
        )
        print(res)

    tkinter.Button(root, text="dialog1", command=dialog1).pack()
    root.mainloop()


if __name__ == "__main__":
    main()
