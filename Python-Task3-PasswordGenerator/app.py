"""
Random Password Generator — Desktop GUI Application (Advanced Tier)
Oasis Infobyte Internship Program (OIBSIP) Task 3
Author: Jawad Ahmad

Tech Stack:
- Python 3.x
- secrets module (cryptographically secure)
- tkinter & ttk (native GUI)
- pyperclip (clipboard integration)

Features:
- Length control via synchronized Slider & Spinbox (min 8, max 64)
- Complexity checkboxes (Uppercase, Lowercase, Numbers, Symbols)
- Option to exclude ambiguous characters (0, O, l, 1, I)
- Guaranteed inclusion of at least 1 character from each selected set
- Dynamic visual strength indicator (Progress bar + color badge)
- "Copy to Clipboard" button + automatic clipboard copy on generation
- Session history displaying the last 5 passwords (in-memory only, not saved to disk)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

import generator

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Random Password Generator — OIBSIP Task 3")
        self.geometry("780x720")
        self.minsize(720, 680)
        self.configure(bg="#0F172A")  # Dark modern slate background

        # State Variables
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=False)
        self.auto_copy_var = tk.BooleanVar(value=True)

        self._setup_styles()
        self._build_ui()
        
        # Generate initial password
        self.generate()

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Base styling
        self.style.configure(".", background="#0F172A", foreground="#F8FAFC", font=("Segoe UI", 10))
        
        # Card Frames
        self.style.configure("Card.TFrame", background="#1E293B", relief="flat")

        # Labels
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground="#FFFFFF", background="#1E293B")
        self.style.configure("SubTitle.TLabel", font=("Segoe UI", 9), foreground="#94A3B8", background="#1E293B")
        self.style.configure("Section.TLabel", font=("Segoe UI", 10, "bold"), foreground="#38BDF8", background="#1E293B")
        self.style.configure("Regular.TLabel", font=("Segoe UI", 10), foreground="#E2E8F0", background="#1E293B")

        # Checkboxes
        self.style.configure("TCheckbutton", background="#1E293B", foreground="#F1F5F9", font=("Segoe UI", 10))
        self.style.map("TCheckbutton", 
                       background=[("active", "#1E293B")],
                       foreground=[("active", "#38BDF8")])

        # Buttons
        self.style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), background="#2563EB", foreground="#FFFFFF")
        self.style.map("Primary.TButton", background=[("active", "#1D4ED8")])

        self.style.configure("Secondary.TButton", font=("Segoe UI", 9, "bold"), background="#334155", foreground="#F8FAFC")
        self.style.map("Secondary.TButton", background=[("active", "#475569")])

        # Progressbar
        self.style.configure("Strength.Horizontal.TProgressbar", troughcolor="#334155", thickness=10)

        # Treeview for Session History
        self.style.configure("Treeview", 
                             background="#1E293B", 
                             foreground="#F8FAFC", 
                             fieldbackground="#1E293B", 
                             rowheight=28, 
                             font=("Consolas", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#334155", foreground="#38BDF8")
        self.style.map("Treeview", background=[("selected", "#2563EB")])

    def _build_ui(self):
        # 1. Top Header Banner
        header = tk.Frame(self, bg="#1E293B", padx=20, pady=14, highlightthickness=1, highlightbackground="#334155")
        header.pack(fill="x", side="top")

        title_lbl = ttk.Label(header, text="🛡️ Random Password Generator", style="Title.TLabel")
        title_lbl.pack(anchor="w")
        sub_lbl = ttk.Label(header, text="Oasis Infobyte Internship Program · Python Programming Track · Task 3 (Advanced Tier)", style="SubTitle.TLabel")
        sub_lbl.pack(anchor="w")

        # 2. Main Scrollable/Padded Body
        container = tk.Frame(self, bg="#0F172A", padx=20, pady=15)
        container.pack(fill="both", expand=True)

        # --- Section 1: Generated Password Display Card ---
        display_card = tk.Frame(container, bg="#1E293B", padx=18, pady=16, highlightthickness=1, highlightbackground="#334155")
        display_card.pack(fill="x", pady=(0, 15))

        lbl_row = tk.Frame(display_card, bg="#1E293B")
        lbl_row.pack(fill="x", mb=6 if hasattr(tk, 'mb') else None)
        ttk.Label(lbl_row, text="Generated Password", style="Section.TLabel").pack(side="left")

        self.copy_status_badge = tk.Label(display_card, text="", font=("Segoe UI", 9, "bold"), bg="#1E293B", fg="#10B981")
        self.copy_status_badge.pack(anchor="e")

        # Password Entry / Output Box
        output_row = tk.Frame(display_card, bg="#1E293B")
        output_row.pack(fill="x", pady=(4, 10))

        self.password_entry = tk.Entry(output_row, font=("Consolas", 15, "bold"), bg="#0F172A", fg="#38BDF8",
                                       insertbackground="#38BDF8", relief="flat", highlightthickness=1,
                                       highlightbackground="#334155", highlightcolor="#38BDF8")
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))

        copy_btn = ttk.Button(output_row, text="📋 Copy", style="Secondary.TButton", command=self.copy_current_password)
        copy_btn.pack(side="right", ipady=4, ipadx=6)

        regen_btn = ttk.Button(output_row, text="🔄 Regenerate", style="Secondary.TButton", command=self.generate)
        regen_btn.pack(side="right", ipady=4, ipadx=4, padx=(0, 6))

        # Strength Bar & Feedback
        strength_frame = tk.Frame(display_card, bg="#1E293B")
        strength_frame.pack(fill="x", pady=(4, 2))

        self.strength_bar = ttk.Progressbar(strength_frame, style="Strength.Horizontal.TProgressbar", orient="horizontal", maximum=100)
        self.strength_bar.pack(side="left", fill="x", expand=True, padx=(0, 15))

        self.strength_badge = tk.Label(strength_frame, text="Strong", font=("Segoe UI", 9, "bold"),
                                       bg="#10B981", fg="#FFFFFF", padx=10, pady=3, relief="flat")
        self.strength_badge.pack(side="right")

        # --- Section 2: Complexity & Configuration Controls ---
        config_card = tk.Frame(container, bg="#1E293B", padx=18, pady=16, highlightthickness=1, highlightbackground="#334155")
        config_card.pack(fill="x", pady=(0, 15))

        ttk.Label(config_card, text="Password Customization & Complexity", style="Section.TLabel").pack(anchor="w", pady=(0, 12))

        # Length Slider & Spinbox
        length_row = tk.Frame(config_card, bg="#1E293B")
        length_row.pack(fill="x", pady=(0, 12))

        ttk.Label(length_row, text="Password Length (min 8):", style="Regular.TLabel").pack(side="left", padx=(0, 12))

        self.length_slider = tk.Scale(length_row, from_=8, to=64, orient="horizontal", variable=self.length_var,
                                      bg="#1E293B", fg="#F8FAFC", highlightthickness=0, troughcolor="#334155",
                                      activebackground="#38BDF8", command=self._on_slider_change)
        self.length_slider.pack(side="left", fill="x", expand=True, padx=(0, 12))

        self.length_spin = tk.Spinbox(length_row, from_=8, to=64, textvariable=self.length_var, width=5,
                                     font=("Segoe UI", 10, "bold"), bg="#0F172A", fg="#38BDF8", relief="flat",
                                     buttonbackground="#334155", command=self._on_spin_change)
        self.length_spin.pack(side="right")
        self.length_spin.bind("<KeyRelease>", lambda e: self._on_spin_change())

        # Character Set Checkboxes (2 columns)
        chk_grid = tk.Frame(config_card, bg="#1E293B")
        chk_grid.pack(fill="x", pady=(0, 10))

        ttk.Checkbutton(chk_grid, text="Include Uppercase Letters (A-Z)", variable=self.upper_var).grid(row=0, column=0, sticky="w", pady=4, padx=(0, 20))
        ttk.Checkbutton(chk_grid, text="Include Lowercase Letters (a-z)", variable=self.lower_var).grid(row=0, column=1, sticky="w", pady=4)

        ttk.Checkbutton(chk_grid, text="Include Numbers / Digits (0-9)", variable=self.digits_var).grid(row=1, column=0, sticky="w", pady=4, padx=(0, 20))
        ttk.Checkbutton(chk_grid, text="Include Special Symbols (!@#$%...)", variable=self.symbols_var).grid(row=1, column=1, sticky="w", pady=4)

        # Advanced Checkboxes
        extra_grid = tk.Frame(config_card, bg="#1E293B")
        extra_grid.pack(fill="x", pady=(6, 12))

        ttk.Checkbutton(extra_grid, text="Exclude Ambiguous Characters (0, O, l, 1, I)", variable=self.ambiguous_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(extra_grid, text="Automatically Copy Password on Generation", variable=self.auto_copy_var).pack(anchor="w", pady=2)

        # Primary Action Button
        gen_btn = ttk.Button(config_card, text="⚡ Generate Strong Password", style="Primary.TButton", command=self.generate)
        gen_btn.pack(fill="x", ipady=8, pady=(4, 0))

        # --- Section 3: In-Memory Session History (Last 5 Passwords) ---
        history_card = tk.Frame(container, bg="#1E293B", padx=18, pady=14, highlightthickness=1, highlightbackground="#334155")
        history_card.pack(fill="both", expand=True)

        history_header = tk.Frame(history_card, bg="#1E293B")
        history_header.pack(fill="x", pady=(0, 8))

        ttk.Label(history_header, text="Recent Session History (Last 5 Passwords — In-Memory Only)", style="Section.TLabel").pack(side="left")

        clear_hist_btn = ttk.Button(history_header, text="Clear History", style="Secondary.TButton", command=self._clear_history)
        clear_hist_btn.pack(side="right")

        # Treeview Table
        cols = ("time", "password", "length", "strength")
        self.history_tree = ttk.Treeview(history_card, columns=cols, show="headings", height=5, selectmode="browse")

        self.history_tree.heading("time", text="Time")
        self.history_tree.heading("password", text="Password (Click to Select / Copy)")
        self.history_tree.heading("length", text="Length")
        self.history_tree.heading("strength", text="Strength")

        self.history_tree.column("time", width=80, anchor="center")
        self.history_tree.column("password", width=380, anchor="w")
        self.history_tree.column("length", width=70, anchor="center")
        self.history_tree.column("strength", width=100, anchor="center")

        self.history_tree.pack(fill="both", expand=True, side="left")
        self.history_tree.bind("<Double-1>", self._on_history_double_click)

        # Quick Copy Selected from History
        hist_btn_frame = tk.Frame(history_card, bg="#1E293B")
        hist_btn_frame.pack(side="right", fill="y", padx=(8, 0))

        copy_hist_btn = ttk.Button(hist_btn_frame, text="📋 Copy\nSelected", style="Secondary.TButton", command=self._copy_selected_history)
        copy_hist_btn.pack(side="top", pady=2, ipady=6)

    def _on_slider_change(self, val):
        try:
            self.length_var.set(int(float(val)))
        except ValueError:
            pass

    def _on_spin_change(self):
        try:
            val = self.length_var.get()
            if 8 <= val <= 64:
                self.length_slider.set(val)
        except (ValueError, tk.TclError):
            pass

    def generate(self):
        try:
            length = self.length_var.get()
        except (ValueError, tk.TclError):
            messagebox.showerror("Invalid Input", "Password length must be an integer (minimum 8).")
            return

        try:
            pwd, strength_label, strength_score, color_hex = generator.generate_password(
                length=length,
                include_upper=self.upper_var.get(),
                include_lower=self.lower_var.get(),
                include_digits=self.digits_var.get(),
                include_symbols=self.symbols_var.get(),
                exclude_ambiguous=self.ambiguous_var.get()
            )

            # Update Entry Box
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, pwd)

            # Update Strength Visuals
            self.strength_bar["value"] = strength_score
            self.strength_badge.config(text=f"{strength_label.upper()} ({strength_score}%)", bg=color_hex)

            # Automatic Copy if enabled
            if self.auto_copy_var.get():
                pyperclip.copy(pwd)
                self._show_copy_feedback("✓ Automatically copied to clipboard!")
            else:
                self.copy_status_badge.config(text="")

            # Update History Table
            self._update_history_table()

        except ValueError as e:
            messagebox.showwarning("Generation Error", str(e))

    def copy_current_password(self):
        pwd = self.password_entry.get()
        if not pwd:
            return
        pyperclip.copy(pwd)
        self._show_copy_feedback("✓ Copied to clipboard!")

    def _show_copy_feedback(self, text: str):
        self.copy_status_badge.config(text=text)
        # Clear after 2.5 seconds
        self.after(2500, lambda: self.copy_status_badge.config(text=""))

    def _update_history_table(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        for entry in generator.session_history.get_all():
            self.history_tree.insert("", "end", values=(
                entry["timestamp"],
                entry["password"],
                entry["length"],
                entry["strength"]
            ))

    def _on_history_double_click(self, event):
        self._copy_selected_history()

    def _copy_selected_history(self):
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showinfo("Select History", "Please select a password from the history list to copy.")
            return

        values = self.history_tree.item(selected[0], "values")
        pwd = values[1]
        pyperclip.copy(pwd)
        self._show_copy_feedback(f"✓ Copied password from history!")

    def _clear_history(self):
        generator.session_history.clear()
        self._update_history_table()
        self._show_copy_feedback("History cleared.")

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
