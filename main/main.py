from static.mainWindow import MainWindow


class App:
    def __init__(self):
        print("App initialized")

    def run(self):
        main_window = MainWindow()
        main_window.display()