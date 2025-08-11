from tkinter import *
from static.components.moneyInput import MoneyInput

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Getränke Automat")
        self.geometry("800x600")

    def packSlaves(self):
        displayFrame = Frame(self)
        displayFrame.pack(side=LEFT)
        
        inputFrame = Frame(self)
        inputFrame.pack(side=RIGHT)

        money_input = MoneyInput(inputFrame)
        money_input.display()

    def display(self):
        self.packSlaves()
        self.mainloop()