from tkinter import RIGHT, Tk, Frame, LEFT
from pathlib import Path

from main.vendingMachine import VendingMachine



# path = Path('main/stock.csv')
# if not path.exists():
#     raise FileNotFoundError(f"CSV file not found: {path}")
# vm = VendingMachine(csv_path=path)
# print("Geladen aus CSV:", [ (i.drink.key, i.drink.price_cents, i.stock) for i in vm.list_items() ])

# vm.insert(500)  # 5 Euro
# print("Balance:", vm.balance_cents)

# outcome = vm.try_purchase("A1")  # Coca Cola
# print("Kauf:", outcome.message)
# change = vm.payout_change()
# print("Wechselgeld:", "{:.2f}".format(change.total_euro), "Euro", change.coins)




class App(Tk):

    def __init__(self):
        super().__init__()
        self.csv_path = Path("main/stock.csv")
        if self.csv_path.exists():
            self.vm = VendingMachine(csv_path=self.csv_path)
        else:
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        self.title("Getränke Automat")
        self.geometry("800x1000")        
    
    @classmethod
    def run(cls):
        app = cls()
        app.mainloop()