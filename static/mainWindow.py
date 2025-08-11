from tkinter import *
from static.components.moneyInput import MoneyInput
from static.components.display import Display

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Getränke Automat")
        self.geometry("800x600")
        self.components = []

    def addComponent(self, component):
        self.components.append(component)
        component.display()

    def packSlaves(self):
        displayFrame = Frame(self)
        displayFrame.pack(side=LEFT)
        
        inputFrame = Frame(self)
        inputFrame.pack(side=RIGHT)

        self.addComponent(MoneyInput(inputFrame))
        self.addComponent(Display(displayFrame))

    def updateComponents(self):
        for component in self.components:
            component.update()

    def display(self):
        self.packSlaves()
        self.mainloop()