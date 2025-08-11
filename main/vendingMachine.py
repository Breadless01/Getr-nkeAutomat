from dataclasses import dataclass, field
from typing import Dict, List, Optional, Literal, Tuple
import csv
from pathlib import Path
from decimal import *

getcontext().prec = 2

# -----------------------------
# Domain
# -----------------------------

@dataclass(frozen=True)
class Drink:
    key: str
    name: str
    price_cents: int

@dataclass
class StockItem:
    drink: Drink
    stock: int

# -----------------------------
# Result-Typen
# -----------------------------

@dataclass
class CoinBreakdown:
    total_euro: Decimal
    coins: List[int] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.total_euro > 0

OutcomeCode = Literal["OK", "OUT_OF_STOCK", "INSUFFICIENT_FUNDS", "UNKNOWN_ITEM"]

@dataclass
class PurchaseOutcome:
    success: bool
    code: OutcomeCode
    message: str
    dispensed: Optional[Drink] = None

# -----------------------------
# VendingMachine
# -----------------------------

class VendingMachine:

    def __init__(self,
                 *,
                 coins_desc_cents: Optional[List[int]] = None,
                 csv_path: Path):
        
        if coins_desc_cents is None:
            coins_desc_cents = [2000, 1000, 500, 200, 100, 50, 20, 10, 5]
        self._coins = coins_desc_cents
        self._balance = 0
        self._inventory: Dict[str, StockItem] = {}
        self._csv_path = csv_path
        with open(self._csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row['key']
                name = row['name']
                price_cents = self._parse_price_to_cents(row['price'])
                stock = int(row['stock'])
                self._inventory[key] = StockItem(Drink(key, name, price_cents), max(0, int(stock)))

    @property
    def balance_cents(self) -> int:
        return self._balance
    
    def insert(self, amount_cents: int) -> None:
        amount_cents = amount_cents
        if amount_cents <= 0:
            raise ValueError("insert amount must be positive")
        self._balance += amount_cents

    def try_purchase(self, key: str) -> PurchaseOutcome:
        if key not in self._inventory:
            return PurchaseOutcome(False, "UNKNOWN_ITEM", f"Unbekannter Artikel: {key}")
        item = self._inventory[key]
        if item.stock <= 0:
            return PurchaseOutcome(False, "OUT_OF_STOCK", f"{item.drink.name} ist ausverkauft.")
        price = item.drink.price_cents
        if self._balance < price:
            missing = price - self._balance
            return PurchaseOutcome(False, "INSUFFICIENT_FUNDS",
                                   f"Es fehlen {missing/100:.2f} € für {item.drink.name}.")
        item.stock -= 1
        self._balance -= price
        self._updateStock()
        
        return PurchaseOutcome(True, "OK", f"{item.drink.name} ausgegeben.", item.drink)
    
    def payout_change(self) -> CoinBreakdown:
        if self._balance <= 0:
            return CoinBreakdown(0.00, [])
        total, coins = self._breakdown(self._balance)
        self._balance -= total
        return CoinBreakdown(total, coins)
    
    def cancel(self) -> CoinBreakdown:
        change = self.payout_change()
        self._balance = 0
        return change

    def list_items(self) -> List[StockItem]:
        return [StockItem(i.drink, i.stock) for i in self._inventory.values()]

    def get_item(self, key: str) -> Optional[StockItem]:
        item = self._inventory.get(key)
        if not item:
            return None
        return StockItem(item.drink, item.stock)

    def set_price(self, key: str, new_price_cents: int) -> None:
        if key not in self._inventory:
            raise KeyError(key)
        self._inventory[key].drink = Drink(
            key, self._inventory[key].drink.name, self._norm(new_price_cents)
        )

    def add_stock(self, key: str, amount: int) -> None:
        if key not in self._inventory:
            raise KeyError(key)
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._inventory[key].stock += amount 
    

    # Helper methods
    def _breakdown(self, amount_cents: int) -> Tuple[int, List[int]]:
        rest = amount_cents
        coins: List[int] = []
        for c in self._coins:
            while rest >= c:
                coins.append(c)
                rest -= c
        dispensed = amount_cents - rest
        return self._parse_price_to_euro(dispensed), coins
    
    def _parse_price_to_cents(self, value: str) -> int:
        value = str(value).strip()
        if value.isdigit():
            return int(value)
        value = value.replace(',', '.')
        cents = int(round(Decimal(value) * 100))
        return cents
    
    def _parse_price_to_euro(self, value: str) -> Decimal:
        value = str(value).strip()
        if value.isdigit():
            return int(value) / 100.0
        return Decimal(value)
    
    def _updateStock(self): 
        with open(self._csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['key', 'name', 'price', 'stock'])
            for item in sorted(self.list_items(), key=lambda x: x.drink.key):
                writer.writerow([item.drink.key, item.drink.name, item.drink.price_cents, item.stock])