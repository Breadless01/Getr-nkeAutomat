from static.mainWindow import MainWindow
from main.automat import Automat
from threading import Thread


class App:
    def __init__(self):
        print("App initialized")

    def run(self):
        automat = Automat()
        automat.addDrink("Coke", 1.50, 10)
        automat.addDrink("Water", 1.00, 20)
        print("Available drinks:", automat.getDrinkList())

        self.openWindow()
    
    def openWindow(self):
        def window_thread():
            main_window = MainWindow()
            main_window.display()
        
        thread = Thread(target=window_thread)
        thread.start()