from main.drinks import Drink


class Automat:

    def __init__(self):
        self.__change = {1: 0, 2: 0, 5: 0, 10: 0, 20: 0, 50: 0}
        self.__drinkList = []

    def addDrink(self, drinkName, drinkPrice, drinkQuantity):
        newDrink = Drink(drinkName, drinkPrice, drinkQuantity)
        self.__drinkList.append(newDrink)

    def getChange(self):
        return self.change
    
    def buyDrink(self, drinkName, numBought):
        for drink in self.__drinkList:
            if drink.getName() == drinkName:
                if drink.getQuantity() >= numBought:
                    drink.buy(numBought)
                    self.change += drink.getPrice() * numBought
                    print(f"Bought {numBought} of {drinkName}. Change is now {self.change}.")
                else:
                    print(f"Not enough {drinkName} in stock.")
                return
            
    def getDrinkList(self):
        return self.__drinkList
    
    def __repr__(self):
        return f"Automat(change={self.__change}, drinks={self.__drinkList})"