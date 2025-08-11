from tkinter import Frame, Tk, Label, Button
from PIL import Image, ImageTk
from main.vendingMachine import Automat


class MoneyInput:
    def __init__(self, master):
        self.master = master   

    def update(self):
        pass

    def addMoney(self, amount):
        self.automat.addInputMoney(amount)

    def display(self):
        # 10 Cent Frame
        frame10cent = Frame(self.master)
        frame10cent.pack(padx=10, pady=10, fill='x')

        label10cent = Label(frame10cent, text="10 Cent", font=("Arial", 24))
        label10cent.grid(row=0, column=1)

        btn10cent = Button(frame10cent, text="Add", command=lambda: self.addMoney(0.10))
        btn10cent.grid(row=0, column=0)

        # 20 Cent Frame
        frame20cent = Frame(self.master)
        frame20cent.pack(padx=10, pady=10, fill='x')

        label20cent = Label(frame20cent, text="20 Cent", font=("Arial", 24))
        label20cent.grid(row=0, column=1)

        btn20cent = Button(frame20cent, text="Add", command=lambda: self.addMoney(0.20))
        btn20cent.grid(row=0, column=0)

        # 50 Cent Frame
        frame50cent = Frame(self.master)
        frame50cent.pack(padx=10, pady=10, fill='x')

        label50cent = Label(frame50cent, text="50 Cent", font=("Arial", 24))
        label50cent.grid(row=0, column=1)

        btn50cent = Button(frame50cent, text="Add", command=lambda: self.addMoney(0.50))
        btn50cent.grid(row=0, column=0)

        # 1 Euro Frame
        frame1euro = Frame(self.master)
        frame1euro.pack(padx=10, pady=10, fill='x')

        label1euro = Label(frame1euro, text="1 Euro", font=("Arial", 24))
        label1euro.grid(row=0, column=1)

        btn1euro = Button(frame1euro, text="Add", command=lambda: self.addMoney(1.00))
        btn1euro.grid(row=0, column=0)

        # 2 Euro Frame
        frame2euro = Frame(self.master)
        frame2euro.pack(padx=10, pady=10, fill='x')

        label2euro = Label(frame2euro, text="2 Euro", font=("Arial", 24))
        label2euro.grid(row=0, column=1)

        btn2euro = Button(frame2euro, text="Add", command=lambda: self.addMoney(2.00))
        btn2euro.grid(row=0, column=0)

        # 5 Euro Frame
        frame5euro = Frame(self.master)
        frame5euro.pack(padx=10, pady=10, fill='x')

        label5euro = Label(frame5euro, text="5 Euro", font=("Arial", 24))
        label5euro.grid(row=0, column=1)

        btn5euro = Button(frame5euro, text="Add", command=lambda: self.addMoney(5.00))
        btn5euro.grid(row=0, column=0)

        # 10 Euro Frame
        frame10euro = Frame(self.master)
        frame10euro.pack(padx=10, pady=10, fill='x')

        label10euro = Label(frame10euro, text="10 Euro", font=("Arial", 24))
        label10euro.grid(row=0, column=1)

        btn10euro = Button(frame10euro, text="Add", command=lambda: self.addMoney(10.00))
        btn10euro.grid(row=0, column=0)

        # 20 Euro Frame
        frame20euro = Frame(self.master)
        frame20euro.pack(padx=10, pady=10, fill='x')

        label20euro = Label(frame20euro, text="20 Euro", font=("Arial", 24))
        label20euro.grid(row=0, column=1)

        btn20euro = Button(frame20euro, text="Add", command=lambda: self.addMoney(20.00))
        btn20euro.grid(row=0, column=0)