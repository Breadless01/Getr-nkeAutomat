
from threading import Thread


class App:
    def __init__(self):
        print("App initialized")
        self.

    def run(self):
        self.automat.addDrink("Coke", 1.50, 10)
        self.automat.addDrink("Water", 1.00, 20)
        print("Available drinks:", self.automat.getDrinkList())

        self.openWindow()
        print("Widow opened")

    def addMoney(self, amount):
        self.automat.addInputMoney(amount)
    
    def openWindow(self):
        def window_thread():
            main_window.display()
        
        thread = Thread(target=window_thread)
        thread.start()

    