import tkinter as tk
from tkinter import ttk

from calculator.engine import evaluate_expression


WINDOW_TITLE = "Universal Python Calculator"
WINDOW_SIZE = "520x780"

STANDARD_ROWS = [
    [("C", "clear"), ("Back", "backspace"), ("(", "("), (")", ")")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("/", "/")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("*", "*")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("-", "-")],
    [("0", "0"), (".", "."), ("ans", "ans"), ("+", "+")],
    [("mem", "mem"), ("%", "%"), ("^", "^") , ("=", "equals")],
]

ADVANCED_ROWS = [
    [("MC", "memory_clear"), ("MR", "memory_recall"), ("M+", "memory_add"), ("M-", "memory_subtract")],
    [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("sqrt", "sqrt(")],
    [("asin", "asin("), ("acos", "acos("), ("atan", "atan("), ("fact", "fact(")],
    [("log", "log("), ("log10", "log10("), ("pi", "pi"), ("e", "e")],
]

COLORS = {
    "app_bg": "#060816",
    "panel_bg": "#0d1326",
    "card_bg": "#121b33",
    "display_bg": "#040b18",
    "history_bg": "#0b1224",
    "text_primary": "#f5fbff",
    "text_secondary": "#8ca4d8",
    "accent": "#00e5ff",
    "accent_alt": "#8b5cf6",
    "accent_warm": "#ff8a3d",
    "number_bg": "#16203c",
    "operator_bg": "#1f2d52",
    "action_bg": "#132847",
    "equal_bg": "#00c2ff",
    "selected_bg": "#19325a",
}


class CalculatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(460, 720)
        self.root.configure(bg=COLORS["app_bg"])

        self.expression = tk.StringVar()
        self.result = tk.StringVar(value="0")
        self.status = tk.StringVar(value="Ready")
        self.memory_label = tk.StringVar(value="MEM 0")

        self.angle_mode = "DEG"
        self.feature_mode = "STANDARD"
        self.memory_value = 0.0
        self.last_answer = 0.0
        self.history = []

        self.mode_buttons = {}
        self.feature_buttons = {}
        self.keypad_frame = None
        self.history_list = None

        self._configure_styles()
        self._build_layout()
        self._bind_events()
        self._set_angle_mode("DEG")
        self._show_feature_mode("STANDARD")

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Root.TFrame", background=COLORS["app_bg"])
        style.configure("Card.TFrame", background=COLORS["card_bg"])
        style.configure(
            "Status.TLabel",
            background=COLORS["app_bg"],
            foreground=COLORS["text_secondary"],
            font=("Segoe UI", 10),
        )

    def _build_layout(self):
        root = ttk.Frame(self.root, style="Root.TFrame", padding=18)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)

        self._build_display(root)
        self._build_toolbar(root)
        self._build_status(root)
        self._build_keypad_area(root)
        self._build_history(root)

    def _build_display(self, parent):
        display = tk.Frame(
            parent,
            bg=COLORS["display_bg"],
            bd=0,
            highlightthickness=1,
            highlightbackground="#17325b",
            padx=18,
            pady=18,
        )
        display.grid(row=0, column=0, sticky="nsew", pady=(0, 14))
        display.grid_columnconfigure(0, weight=1)
        display.grid_columnconfigure(1, weight=1)

        tk.Label(
            display,
            text="UNIVERSAL CALCULATOR",
            bg=COLORS["display_bg"],
            fg=COLORS["accent"],
            font=("Segoe UI Semibold", 11),
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            display,
            textvariable=self.memory_label,
            bg=COLORS["display_bg"],
            fg=COLORS["text_secondary"],
            font=("Segoe UI", 10),
        ).grid(row=0, column=1, sticky="e")

        self.entry = tk.Entry(
            display,
            textvariable=self.expression,
            justify="right",
            relief="flat",
            bd=0,
            bg=COLORS["display_bg"],
            fg=COLORS["text_secondary"],
            insertbackground=COLORS["accent"],
            font=("Consolas", 20),
        )
        self.entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(16, 10), ipady=10)

        tk.Label(
            display,
            textvariable=self.result,
            bg=COLORS["display_bg"],
            fg=COLORS["text_primary"],
            font=("Segoe UI Semibold", 38),
            anchor="e",
        ).grid(row=2, column=0, columnspan=2, sticky="ew")

    def _build_toolbar(self, parent):
        toolbar = tk.Frame(parent, bg=COLORS["app_bg"])
        toolbar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        toolbar.grid_columnconfigure(0, weight=1)
        toolbar.grid_columnconfigure(1, weight=1)

        left = tk.Frame(toolbar, bg=COLORS["app_bg"])
        left.grid(row=0, column=0, sticky="w")

        right = tk.Frame(toolbar, bg=COLORS["app_bg"])
        right.grid(row=0, column=1, sticky="e")

        self.feature_buttons["STANDARD"] = self._create_toggle_button(
            left, "Standard", lambda: self._show_feature_mode("STANDARD")
        )
        self.feature_buttons["ADVANCED"] = self._create_toggle_button(
            left, "Advanced", lambda: self._show_feature_mode("ADVANCED")
        )
        self.feature_buttons["STANDARD"].pack(side="left", padx=(0, 8))
        self.feature_buttons["ADVANCED"].pack(side="left")

        self.mode_buttons["DEG"] = self._create_toggle_button(
            right, "DEG", lambda: self._set_angle_mode("DEG")
        )
        self.mode_buttons["RAD"] = self._create_toggle_button(
            right, "RAD", lambda: self._set_angle_mode("RAD")
        )
        self.mode_buttons["DEG"].pack(side="left", padx=(0, 8))
        self.mode_buttons["RAD"].pack(side="left")

    def _build_status(self, parent):
        ttk.Label(parent, textvariable=self.status, style="Status.TLabel").grid(
            row=2, column=0, sticky="w", pady=(0, 10)
        )

    def _build_keypad_area(self, parent):
        keypad_card = tk.Frame(
            parent,
            bg=COLORS["panel_bg"],
            bd=0,
            highlightthickness=1,
            highlightbackground="#182a4c",
            padx=14,
            pady=14,
        )
        keypad_card.grid(row=3, column=0, sticky="nsew", pady=(0, 14))
        keypad_card.grid_columnconfigure(0, weight=1)
        keypad_card.grid_rowconfigure(1, weight=1)

        self.keypad_title = tk.Label(
            keypad_card,
            text="Standard Tools",
            bg=COLORS["panel_bg"],
            fg=COLORS["text_primary"],
            font=("Segoe UI Semibold", 12),
        )
        self.keypad_title.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.keypad_frame = tk.Frame(keypad_card, bg=COLORS["panel_bg"])
        self.keypad_frame.grid(row=1, column=0, sticky="nsew")

    def _build_history(self, parent):
        history_card = tk.Frame(
            parent,
            bg=COLORS["history_bg"],
            bd=0,
            highlightthickness=1,
            highlightbackground="#15284a",
            padx=14,
            pady=14,
        )
        history_card.grid(row=4, column=0, sticky="nsew")
        history_card.grid_columnconfigure(0, weight=1)
        history_card.grid_rowconfigure(1, weight=1)

        tk.Label(
            history_card,
            text="History",
            bg=COLORS["history_bg"],
            fg=COLORS["text_primary"],
            font=("Segoe UI Semibold", 12),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        history_frame = tk.Frame(history_card, bg=COLORS["history_bg"])
        history_frame.grid(row=1, column=0, sticky="nsew")
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(0, weight=1)

        self.history_list = tk.Listbox(
            history_frame,
            bg=COLORS["history_bg"],
            fg=COLORS["text_secondary"],
            selectbackground=COLORS["selected_bg"],
            selectforeground=COLORS["text_primary"],
            relief="flat",
            bd=0,
            highlightthickness=0,
            activestyle="none",
            exportselection=False,
            font=("Consolas", 11),
        )
        self.history_list.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(
            history_frame,
            command=self.history_list.yview,
            bg=COLORS["panel_bg"],
            troughcolor=COLORS["app_bg"],
            activebackground=COLORS["accent_alt"],
        )
        self.history_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        actions = tk.Frame(history_card, bg=COLORS["history_bg"])
        actions.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        self._create_action_button(
            actions, "Use Selected", self._use_selected_history
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self._create_action_button(
            actions, "Clear History", self._clear_history
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def _bind_events(self):
        self.root.bind("<Return>", lambda _event: self._calculate())
        self.root.bind("<KP_Enter>", lambda _event: self._calculate())
        self.root.bind("<Escape>", lambda _event: self._clear_expression())
        self.history_list.bind("<Double-Button-1>", lambda _event: self._use_selected_history())
        self.entry.focus_set()

    def _create_toggle_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=COLORS["action_bg"],
            fg=COLORS["text_secondary"],
            activebackground=COLORS["accent_alt"],
            activeforeground=COLORS["text_primary"],
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            font=("Segoe UI Semibold", 10),
            cursor="hand2",
        )

    def _create_action_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=COLORS["action_bg"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["accent_alt"],
            activeforeground=COLORS["text_primary"],
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            font=("Segoe UI Semibold", 10),
            cursor="hand2",
        )

    def _create_key_button(self, parent, label, value, row, column):
        styles = self._button_colors(label)
        button = tk.Button(
            parent,
            text=label,
            command=lambda: self._handle_button(value),
            bg=styles["bg"],
            fg=styles["fg"],
            activebackground=styles["active_bg"],
            activeforeground=styles["fg"],
            relief="flat",
            bd=0,
            padx=8,
            pady=8,
            font=styles["font"],
            cursor="hand2",
        )
        button.grid(row=row, column=column, sticky="nsew", padx=5, pady=5, ipadx=4, ipady=6)

    def _button_colors(self, label):
        if label == "=":
            return {
                "bg": COLORS["equal_bg"],
                "active_bg": COLORS["accent"],
                "fg": COLORS["display_bg"],
                "font": ("Segoe UI Semibold", 15),
            }
        if label.isdigit() or label == ".":
            return {
                "bg": COLORS["number_bg"],
                "active_bg": COLORS["selected_bg"],
                "fg": COLORS["text_primary"],
                "font": ("Segoe UI Semibold", 16),
            }
        if label in {"+", "-", "*", "/", "%", "^"}:
            return {
                "bg": COLORS["operator_bg"],
                "active_bg": COLORS["accent_alt"],
                "fg": COLORS["text_primary"],
                "font": ("Segoe UI Semibold", 14),
            }
        return {
            "bg": COLORS["action_bg"],
            "active_bg": COLORS["selected_bg"],
            "fg": COLORS["text_secondary"],
            "font": ("Segoe UI Semibold", 11),
        }

    def _show_feature_mode(self, mode):
        self.feature_mode = mode
        self.keypad_title.config(
            text="Standard Tools" if mode == "STANDARD" else "Advanced Tools"
        )
        self._render_keypad(STANDARD_ROWS if mode == "STANDARD" else ADVANCED_ROWS)

        for name, button in self.feature_buttons.items():
            self._paint_toggle(button, active=name == mode)

        self.status.set(
            "Standard features ready" if mode == "STANDARD" else "Advanced features ready"
        )
        self.entry.focus_set()

    def _set_angle_mode(self, mode):
        self.angle_mode = mode
        for name, button in self.mode_buttons.items():
            self._paint_toggle(button, active=name == mode, accent=COLORS["accent_alt"])
        self.status.set(f"Angle mode switched to {mode}")
        self.entry.focus_set()

    def _paint_toggle(self, button, active, accent=None):
        active_bg = accent or COLORS["accent"]
        if active:
            button.configure(bg=active_bg, fg=COLORS["display_bg"])
        else:
            button.configure(bg=COLORS["action_bg"], fg=COLORS["text_secondary"])

    def _render_keypad(self, rows):
        for child in self.keypad_frame.winfo_children():
            child.destroy()

        column_count = max(len(row) for row in rows)
        for column in range(column_count):
            self.keypad_frame.grid_columnconfigure(column, weight=1)
        for row_index in range(len(rows)):
            self.keypad_frame.grid_rowconfigure(row_index, weight=1)

        for row_index, row in enumerate(rows):
            for column_index, (label, value) in enumerate(row):
                self._create_key_button(self.keypad_frame, label, value, row_index, column_index)

    def _handle_button(self, value):
        if value == "equals":
            self._calculate()
            return
        if value == "clear":
            self._clear_expression()
            return
        if value == "backspace":
            self._backspace()
            return
        if value == "memory_clear":
            self._set_memory(0.0, "Memory cleared")
            return
        if value == "memory_recall":
            self._insert_text("mem")
            self.status.set("Memory inserted")
            return
        if value == "memory_add":
            self._update_memory(add=True)
            return
        if value == "memory_subtract":
            self._update_memory(add=False)
            return

        self._insert_text(value)

    def _insert_text(self, text):
        position = self.entry.index(tk.INSERT)
        current = self.expression.get()
        self.expression.set(current[:position] + text + current[position:])
        self.entry.icursor(position + len(text))
        self.status.set("Typing...")
        self.entry.focus_set()

    def _backspace(self):
        position = self.entry.index(tk.INSERT)
        if position == 0:
            return
        current = self.expression.get()
        self.expression.set(current[: position - 1] + current[position:])
        self.entry.icursor(position - 1)
        self.status.set("Edited")
        self.entry.focus_set()

    def _clear_expression(self):
        self.expression.set("")
        self.result.set("0")
        self.status.set("Cleared")
        self.entry.focus_set()

    def _calculate(self):
        expression = self.expression.get().strip()
        if not expression:
            self.status.set("Enter a calculation first")
            return

        try:
            value = evaluate_expression(
                expression,
                ans=self.last_answer,
                memory=self.memory_value,
                angle_mode=self.angle_mode,
            )
        except ValueError as error:
            self.result.set("Error")
            self.status.set(str(error))
            self.entry.focus_set()
            return

        self.last_answer = value
        formatted = self._format_number(value)
        self.result.set(formatted)
        self.status.set(f"Calculation complete in {self.angle_mode} mode")
        history_item = f"[{self.angle_mode}] {expression} = {formatted}"
        self.history.append(history_item)
        self.history_list.insert(tk.END, history_item)
        self.entry.focus_set()

    def _get_display_value(self):
        current = self.result.get()
        if current in {"", "Error"}:
            expression = self.expression.get().strip()
            if not expression:
                return None
            return evaluate_expression(
                expression,
                ans=self.last_answer,
                memory=self.memory_value,
                angle_mode=self.angle_mode,
            )
        return float(current)

    def _update_memory(self, add):
        try:
            value = self._get_display_value()
        except ValueError as error:
            self.status.set(str(error))
            return

        if value is None:
            self.status.set("Nothing available to store")
            return

        if add:
            self._set_memory(self.memory_value + value, "Added result to memory")
        else:
            self._set_memory(self.memory_value - value, "Subtracted result from memory")

    def _set_memory(self, value, message):
        self.memory_value = value
        self.memory_label.set(f"MEM {self._format_number(value)}")
        self.status.set(message)
        self.entry.focus_set()

    def _use_selected_history(self):
        selection = self.history_list.curselection()
        if not selection:
            self.status.set("Select a history item first")
            return

        item = self.history_list.get(selection[0])
        expression = item.split(" = ")[0]
        if expression.startswith("[") and "] " in expression:
            expression = expression.split("] ", 1)[1]
        self.expression.set(expression)
        self.entry.icursor(len(expression))
        self.status.set("History expression loaded")
        self.entry.focus_set()

    def _clear_history(self):
        self.history.clear()
        self.history_list.delete(0, tk.END)
        self.status.set("History cleared")
        self.entry.focus_set()

    def _format_number(self, value):
        if float(value).is_integer():
            return str(int(value))
        return f"{value:.10g}"

    def run(self):
        self.root.mainloop()


def main():
    app = CalculatorGUI()
    app.run()
