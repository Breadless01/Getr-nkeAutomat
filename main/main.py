from customtkinter import RIGHT, CTk, CTkFrame, CTkLabel, CTkButton, CTkImage, StringVar, LEFT, set_default_color_theme
from pathlib import Path
from PIL import Image
from db import Db
from customError import DbNotFoundError

from main.vendingMachine import VendingMachine

set_default_color_theme("main/static/theme.json")

class App(CTk):

    def __init__(self):
        super().__init__()
        self.csv_path = Path("main/stock.csv")
        self.db = Db()
        if self.db:
            self.vm = VendingMachine(db=self.db)
        if self.csv_path.exists():
            self.vm = VendingMachine(csv_path=self.csv_path)
        else:
            raise DbNotFoundError(f"CSV file or DB not found")
        self.title("Getränke Automat")
        self.geometry("1100x900")
        self.minsize(900, 800)

        # Display-Variablen
        self.display_msg = StringVar(value="Bitte Getränk wählen…")
        self.display_balance = StringVar(value=self._format_balance())
        self.display_code = StringVar(value="--")

        # Auswahlzustand
        self._sel_letter: str | None = None
        self._sel_number: str | None = None

        self._build_ui()
        self._refresh_catalog()
        self._update_display("Bereit.")

    # -----------------------------
    # UI Aufbau
    # -----------------------------

    def _build_ui(self):
        self.body = CTkFrame(self)
        self.body.pack(fill="both", expand=True)
        self.body.columnconfigure(0, weight=3)
        self.body.columnconfigure(1, weight=1)

        # Linker Bereich: Anzeige + Katalog (nur Anzeige, keine Buttons)
        left_frame = CTkFrame(self.body)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.rowconfigure(1, weight=1)

        # Anzeige-Display (oben)
        self.display_frame = CTkFrame(left_frame)
        self.display_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.columnconfigure(1, weight=0)

        self.display_label = CTkLabel(self.display_frame, textvariable=self.display_msg,
                                   font=("Segoe UI", 16, "bold"), anchor="w", justify="left")
        self.display_label.grid(row=0, column=0, sticky="w")

        right_disp = CTkFrame(self.display_frame)
        right_disp.grid(row=0, column=1, sticky="ew")
        CTkLabel(right_disp, textvariable=self.display_balance, font=("Segoe UI", 14), anchor="e").pack(anchor="e")
        CTkLabel(right_disp, text="Auswahl:", font=("Segoe UI", 10)).pack(anchor="e")
        CTkLabel(right_disp, textvariable=self.display_code, font=("Consolas", 14, "bold")).pack(anchor="e")

        # Katalog (Card-Grid): zeigt verfügbare Getränke + Preise/Bestand
        self.catalog_frame = CTkFrame(left_frame)
        self.catalog_frame.grid(row=1, column=0, sticky="nsew")
        for c in range(3):
            self.catalog_frame.columnconfigure(c, weight=1)

        # Rechter Bereich: oben Geld, darunter Auswahl-Buttons als Grid
        right_frame = CTkFrame(self.body)
        right_frame.grid(row=0, column=1, sticky="nswe", padx=(12, 0))
        right_frame.rowconfigure(1, weight=1)

        # Geld-Panel (oben)
        money_frame = CTkFrame(right_frame)
        money_frame.grid(row=0, column=0, sticky="new")
        CTkLabel(money_frame, text="Geld einwerfen", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 8))
        for i, val in enumerate(self.vm._coins):
            r, c = divmod(i, 3)
            path = Image.open(f"main/static/images/{self._format_coin(val)}.png")
            img = CTkImage(light_image=path, size=(30, 30))
            btn = CTkButton(money_frame, image=img, text="", width=10, height=2,
                         command=lambda v=val: self._on_insert(v))
            btn.grid(row=r+1, column=c, padx=4, pady=4, sticky="ew")
        for c in range(3):
            money_frame.columnconfigure(c, weight=1)

        # Auswahl-Panel (unten)
        keypad = CTkFrame(right_frame)
        keypad.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        keypad.columnconfigure((0, 1, 2), weight=1)
        CTkLabel(keypad, text="Auswahl", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 8))
        # Buchstaben-Reihe
        for c, letter in enumerate(["A", "B", "C"]):
            CTkButton(keypad, text=letter, width=8, height=2, command=lambda L=letter: self._on_select_part(L)).grid(row=1,
                                                                                                                  column=c,
                                                                                                                  padx=4,
                                                                                                                  pady=4,
                                                                                                                  sticky="ew")
        # Zahlen-Reihe
        for c, num in enumerate(["1", "2", "3"]):
            CTkButton(keypad, text=num, width=8, height=2, command=lambda N=num: self._on_select_part(N)).grid(row=2,
                                                                                                            column=c,
                                                                                                            padx=4,
                                                                                                            pady=4,
                                                                                                            sticky="ew")

        # Escape -> Fenster schließen
        self.bind("<Escape>", lambda e: self.destroy())

    # -----------------------------
    # Katalog/Anzeige
    # -----------------------------
    def _refresh_catalog(self):
        for w in self.catalog_frame.winfo_children():
            w.destroy()
        items = sorted(self.vm.list_items(), key=lambda x: x.drink.key)
        cols = 3
        for idx, item in enumerate(items):
            r, c = divmod(idx, cols)
            card = CTkFrame(self.catalog_frame)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            for cc in range(2):
                card.columnconfigure(cc, weight=1)
            CTkLabel(card, text=item.drink.key, font=("Consolas", 12, "bold"), anchor="w").grid(row=0, column=0,
                                                                                             sticky="w")
            CTkLabel(card, text=f"{item.drink.name}", font=("Segoe UI", 12)).grid(row=1, column=0, columnspan=2,
                                                                               sticky="w")
            CTkLabel(card, text=f"{item.drink.price_cents / 100:.2f} €", font=("Segoe UI", 11, "bold"),
                  anchor="e").grid(row=0, column=1, sticky="e")
            stock_txt = f"Bestand: {item.stock}" if item.stock > 0 else "Ausverkauft"
            CTkLabel(card, text=stock_txt, font=("Segoe UI", 10)).grid(row=2, column=0, columnspan=2, sticky="w")
        for c in range(cols):
            self.catalog_frame.columnconfigure(c, weight=1)

    # -----------------------------
    # Auswahl-Logik (Keypad)
    # -----------------------------
    def _on_select_part(self, part: str):
        if part.isalpha():
            self._sel_letter = part
        else:
            self._sel_number = part
        self._update_code_display()
        if self._sel_letter and self._sel_number:
            self._on_confirm()

    def _update_code_display(self):
        l = self._sel_letter or "-"
        n = self._sel_number or "-"
        self.display_code.set(f"{l}{n}")

    def _on_confirm(self):
        if not (self._sel_letter and self._sel_number):
            self._update_display("Bitte Buchstabe und Zahl wählen")
            return
        key = f"{self._sel_letter}{self._sel_number}"
        self._execute_selection(key)
        self._on_clear()

    def _on_clear(self):
        self._sel_letter = None
        self._sel_number = None
        self._update_code_display()

    def _execute_selection(self, key: str):
        result = self.vm.try_purchase(key)
        if result.success:
            self._update_display(f"Ausgabe: {result.dispensed.name}")
        else:
            self._update_display(result.message)
        self._refresh_catalog()
        self._payout_change()
        self._update_balance()

    def _payout_change(self):
        result = self.vm.payout_change()
        self._update_display(f"Change: {result.total_euro:.2f} €")

    # -----------------------------
    # Geld
    # -----------------------------

    def _on_insert(self, amount_cents: int):
        self.vm.insert(amount_cents)
        self._update_balance()
        self._update_display(f"Eingeworfen: {self._format_coin(amount_cents)}")

    # -----------------------------
    # Helpers
    # -----------------------------

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