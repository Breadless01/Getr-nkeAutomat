class Drink:

    def __init__(self, name, price, quantity):

        self.name = name
        self.price = price
        self.quantity = quantity

    def getQuantity(self):
        return self.quantity
    
    def buy(self, numBought):
        self.quantity -= numBought

    def getName(self):
        return self.name
    
    def getPrice(self):
        return self.price
    
    def __repr__(self):
        return f"Drink(name={self.name}, price={self.price}, quantity={self.quantity})"