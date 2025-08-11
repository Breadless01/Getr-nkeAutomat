from customtkinter import RIGHT, CTk, CTkFrame, CTkLabel, CTkButton, CTkImage, StringVar, LEFT, set_default_color_theme
from pathlib import Path
from PIL import Image

from main.vendingMachine import VendingMachine

set_default_color_theme("main/static/theme.json")

class App(CTk):

    def __init__(self):
        super().__init__()
        self.csv_path = Path("main/stock.csv")
        if self.csv_path.exists():
            self.vm = VendingMachine(csv_path=self.csv_path)
        else:
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        self.title("Getränke Automat")
        self.geometry("800x1000")   

        self.display_msg = StringVar(value="Bitte Getränk wählen…")
        self.display_balance = StringVar(value=self._format_balance()) 

        self._build_ui()
        self._refresh_drinks()

    # -----------------------------
    # UI Aufbau
    # -----------------------------

    def _build_ui(self):
        self.body = CTkFrame(self)
        self.body.pack(fill="both", expand=True)
        self.body.columnconfigure(0, weight=3)
        self.body.columnconfigure(1, weight=1)

        # Left
        left_frame = CTkFrame(self.body)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Header / Display
        self.display_frame = CTkFrame(left_frame)
        self.display_frame.pack(fill="x", pady=(0, 12))

        self.display_label = CTkLabel(self.display_frame, textvariable=self.display_msg,
                                   font=("Segoe UI", 16, "bold"), anchor="w", justify="left")
        self.display_label.grid(row=0, column=0, sticky="w")

        self.balance_label = CTkLabel(self.display_frame, textvariable=self.display_balance,
                                   font=("Segoe UI", 14), anchor="w")
        self.balance_label.grid(row=1, column=0, sticky="w")

        
        # Right
        right_frame = CTkFrame(self.body)
        right_frame.grid(row=0, column=1, sticky="nswe", padx=(12, 0))

        # Geld Buttons
        for val in self.vm._coins:
            path = Image.open(f"main/static/images/{self._format_coin(val)}.png")
            img = CTkImage(light_image=path, size=(30, 30))
            btn = CTkButton(right_frame, image=img, text="", width=10, height=2,
                         command=lambda v=val: self._on_insert(v))
            btn.pack(pady=4, fill="x")

        # Produkt-Buttons
        self.grid_frame = CTkFrame(right_frame)
        self.grid_frame.pack(fill="both", expand=True)
        for c in range(3):
            self.grid_frame.columnconfigure(c, weight=1)

        # Escape -> Fenster schließen
        self.bind("<Escape>", lambda e: self.destroy())

    def _refresh_drinks(self):
        # Clear grid
        for w in self.grid_frame.winfo_children():
            w.destroy()

        items = sorted(self.vm.list_items(), key=lambda x: x.drink.key)
        cols = 3
        for idx, item in enumerate(items):
            r, c = divmod(idx, cols)
            text = item.drink.key
            state = "normal" if item.stock > 0 else "disabled"
            btn = CTkButton(self.grid_frame, text=text, width=18, height=5, state=state,
                         command=lambda k=item.drink.key: self._on_select(k))
            btn.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")

    # -----------------------------
    # Events & Helpers
    # -----------------------------

    def _on_select(self, key: str):
        result = self.vm.try_purchase(key)
        if result.success:
            self._update_display(f"Ausgabe: {result.dispensed.name}")
        else:
            self._update_display(result.message)
        self._refresh_drinks()
        self._update_balance()

    def _on_insert(self, amount_cents: int):
        self.vm.insert(amount_cents)
        self._update_balance()
        self._update_display(f"Eingeworfen: {self._format_coin(amount_cents)}")

    def _update_display(self, msg: str):
        self.display_msg.set(msg)

    def _update_balance(self):
        self.display_balance.set(self._format_balance())

    def _format_balance(self) -> str:
        return f"Guthaben: {self.vm.balance_cents/100:.2f} €"
    
    def _format_coin(self, cents: int) -> str:
        if cents >= 100:
            return f"{cents//100}Euro"
        else:
            return f"{cents}Cent"
    
    @classmethod
    def run(cls):
        app = cls()
        app.mainloop()