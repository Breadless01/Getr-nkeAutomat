import tkinter

class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("800x600")

    def display(self):
        self.mainloop()