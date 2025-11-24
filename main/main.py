from customtkinter import (
    RIGHT,
    CTk,
    CTkFrame,
    CTkLabel,
    CTkButton,
    CTkImage,
    CTkScrollableFrame,
    StringVar,
    LEFT,
    set_default_color_theme,
    set_appearance_mode,
)
from pathlib import Path
from PIL import Image
from main.db import Db
from main.customError import DbNotFoundError

from main.vendingMachine import VendingMachine

set_appearance_mode("dark")  # z.B. "dark" oder "system"
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

        self.title("Getränkeautomat")
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
        # Haupt-Container
        self.body = CTkFrame(self, corner_radius=16)
        self.body.pack(fill="both", expand=True, padx=20, pady=20)

        self.body.rowconfigure(0, weight=0)  # Header
        self.body.rowconfigure(1, weight=1)  # Content
        self.body.columnconfigure(0, weight=3)
        self.body.columnconfigure(1, weight=2)

        # ---------- Header ----------
        header = CTkFrame(self.body, corner_radius=16, fg_color=("gray90", "gray15"))
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)

        title_label = CTkLabel(
            header,
            text="GETRÄNKEAUTOMAT",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        )
        title_label.grid(row=0, column=0, sticky="w", padx=20, pady=12)

        subtitle_label = CTkLabel(
            header,
            text="Einwurf · Auswahl · Genuss",
            font=("Segoe UI", 12),
            anchor="e",
            text_color=("gray40", "gray70"),
        )
        subtitle_label.grid(row=0, column=1, sticky="e", padx=20)

        # ---------- Content: Links / Rechts ----------
        # Linker Bereich
        left_frame = CTkFrame(self.body, corner_radius=16)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # Anzeige-Display (oben, wie Konsole)
        self.display_frame = CTkFrame(
            left_frame,
            corner_radius=16,
            fg_color=("gray85", "gray10"),
        )
        self.display_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12), padx=4)
        self.display_frame.columnconfigure(0, weight=1)
        self.display_frame.columnconfigure(1, weight=0)

        self.display_label = CTkLabel(
            self.display_frame,
            textvariable=self.display_msg,
            font=("Segoe UI", 16, "bold"),
            anchor="w",
            justify="left",
            wraplength=550,
        )
        self.display_label.grid(row=0, column=0, sticky="w", padx=16, pady=12)

        right_disp = CTkFrame(self.display_frame, fg_color="transparent")
        right_disp.grid(row=0, column=1, sticky="e", padx=16, pady=12)

        CTkLabel(
            right_disp,
            textvariable=self.display_balance,
            font=("Segoe UI", 14, "bold"),
            anchor="e",
        ).pack(anchor="e")
        CTkLabel(
            right_disp,
            text="Auswahl:",
            font=("Segoe UI", 10),
            anchor="e",
        ).pack(anchor="e", pady=(8, 0))
        CTkLabel(
            right_disp,
            textvariable=self.display_code,
            font=("Consolas", 18, "bold"),
            anchor="e",
        ).pack(anchor="e")

        # Katalog (als Scroll-Grid für Getränke)
        self.catalog_frame = CTkScrollableFrame(
            left_frame,
            corner_radius=16,
            fg_color=("gray92", "gray12"),
        )
        self.catalog_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=(4, 0))
        for c in range(3):
            self.catalog_frame.columnconfigure(c, weight=1)

        # Rechter Bereich: Geld + Auswahl
        right_frame = CTkFrame(self.body, corner_radius=16)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(12, 0))
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        # Geld-Panel (oben)
        money_frame = CTkFrame(right_frame, corner_radius=16)
        money_frame.grid(row=0, column=0, sticky="new", padx=8, pady=(8, 4))
        money_frame.columnconfigure((0, 1, 2), weight=1)

        CTkLabel(
            money_frame,
            text="Geld einwerfen",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, columnspan=3, pady=(8, 10))

        for i, val in enumerate(self.vm._coins):
            r, c = divmod(i, 3)
            img_path = Image.open(f"main/static/images/{self._format_coin(val)}.png")
            img = CTkImage(light_image=img_path, size=(34, 34))
            btn = CTkButton(
                money_frame,
                image=img,
                text=f"{val/100:.2f} €" if val >= 100 else f"{val} ct",
                compound="top",
                width=10,
                height=60,
                fg_color=("gray85", "gray20"),
                hover_color=("gray75", "gray30"),
                corner_radius=12,
                command=lambda v=val: self._on_insert(v),
            )
            btn.grid(row=r + 1, column=c, padx=6, pady=6, sticky="ew")

        # Auswahl-Panel (unten)
        keypad = CTkFrame(right_frame, corner_radius=16)
        keypad.grid(row=1, column=0, sticky="nsew", padx=8, pady=(4, 8))
        keypad.columnconfigure((0, 1, 2), weight=1)
        keypad.rowconfigure((1, 2, 3), weight=1)

        CTkLabel(
            keypad,
            text="Auswahl",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, columnspan=3, pady=(10, 8))

        # Buchstaben-Reihe
        for c, letter in enumerate(["A", "B", "C"]):
            CTkButton(
                keypad,
                text=letter,
                width=8,
                height=60,
                font=("Segoe UI", 18, "bold"),
                fg_color=("#4A90E2", "#1F4B99"),
                hover_color=("#6BA6F2", "#265BBF"),
                corner_radius=16,
                command=lambda L=letter: self._on_select_part(L),
            ).grid(
                row=1,
                column=c,
                padx=6,
                pady=6,
                sticky="nsew",
            )

        # Zahlen-Reihe
        for c, num in enumerate(["1", "2", "3"]):
            CTkButton(
                keypad,
                text=num,
                width=8,
                height=60,
                font=("Segoe UI", 18, "bold"),
                fg_color=("gray80", "gray25"),
                hover_color=("gray70", "gray35"),
                corner_radius=16,
                command=lambda N=num: self._on_select_part(N),
            ).grid(
                row=2,
                column=c,
                padx=6,
                pady=6,
                sticky="nsew",
            )

        # Clear-Button für Auswahl (unten als Zusatz)
        clear_btn = CTkButton(
            keypad,
            text="Auswahl löschen",
            font=("Segoe UI", 12),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            corner_radius=16,
            command=self._on_clear,
        )
        clear_btn.grid(row=3, column=0, columnspan=3, padx=8, pady=(10, 12), sticky="ew")

        # Escape -> Fenster schließen
        self.bind("<Escape>", lambda e: self.destroy())

    # -----------------------------
    # Katalog/Anzeige
    # -----------------------------
    def _refresh_catalog(self):
        # alle alten Widgets entfernen
        for w in self.catalog_frame.winfo_children():
            w.destroy()

        items = sorted(self.vm.list_items(), key=lambda x: x.drink.key)
        cols = 3
        for idx, item in enumerate(items):
            r, c = divmod(idx, cols)
            card = CTkFrame(
                self.catalog_frame,
                corner_radius=16,
                fg_color=("white", "gray18"),
            )
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
            card.columnconfigure(0, weight=3)
            card.columnconfigure(1, weight=2)

            # Key / Preis Zeile
            CTkLabel(
                card,
                text=item.drink.key,
                font=("Consolas", 14, "bold"),
                anchor="w",
            ).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 0))

            CTkLabel(
                card,
                text=f"{item.drink.price_cents / 100:.2f} €",
                font=("Segoe UI", 13, "bold"),
                anchor="e",
            ).grid(row=0, column=1, sticky="e", padx=10, pady=(8, 0))

            # Name
            CTkLabel(
                card,
                text=f"{item.drink.name}",
                font=("Segoe UI", 12),
                anchor="w",
            ).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(4, 0))

            # Bestand
            stock_txt = f"Bestand: {item.stock}" if item.stock > 0 else "Ausverkauft"
            stock_color = ("gray20", "gray80") if item.stock > 0 else ("#B00020", "#FF8080")

            CTkLabel(
                card,
                text=stock_txt,
                font=("Segoe UI", 11),
                anchor="w",
                text_color=stock_color,
            ).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(4, 8))

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
