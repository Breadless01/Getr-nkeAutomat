import tkinter


class MoneyInput:
    def __init__(self, master: tkinter.Tk):
        self.master = master
        self.amount = 0.00

    def display(self):
        label = tkinter.Label(self.master, image=tkinter.PhotoImage(file="static/images/1Euro.png"))
        label.pack(pady=10)