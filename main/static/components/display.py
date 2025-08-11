from tkinter import Tk, Frame, Label
from main.vendingMachine import Automat

class Display:
    def __init__(self, master):
        self.master = master
        self.amount = 0.0

    def update(self):
        self.total_label.config(text=f"{self.amount:.2f} Euro")

    def display(self):
        frame = Frame(self.master, bg='#000000', width=300, height=200)
        frame.pack(padx=10, pady=10, fill='x') 

        self.total_label = Label(frame, text=f"{self.amount:.2f} Euro", font=("Arial", 24))
        self.total_label.pack()