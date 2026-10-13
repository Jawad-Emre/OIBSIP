"""
BMI Calculator — Oasis Infobyte SIP Task 2 (Advanced Tier)
Author: Jawad Ahmad
Features:
- Multi-User Profile Support with Unique Auto-Generated User IDs
- Precision BMI Calculation & WHO Category Classification
- Dynamic Color-Coded Health Feedback Badges
- SQLite Database Persistence (CRUD)
- Historical Records Table View
- Interactive Matplotlib BMI Trend Progression Chart
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import database as db

# Category styling constants
CATEGORY_COLORS = {
    "Underweight": "#1976D2",   # Blue
    "Normal": "#2E7D32",        # Green
    "Overweight": "#F57C00",    # Orange
    "Obese": "#D32F2F"          # Red
}

CATEGORY_DESCRIPTIONS = {
    "Underweight": "Your BMI is below the healthy range (< 18.5). Consider consulting a nutritionist.",
    "Normal": "Your BMI is within the ideal healthy range (18.5 – 24.9). Keep up the great work!",
    "Overweight": "Your BMI is slightly above the healthy range (25.0 – 29.9). Regular exercise is recommended.",
    "Obese": "Your BMI indicates obesity (≥ 30.0). A balanced diet and medical guidance are advised."
}

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Computes BMI using the formula: weight / height^2."""
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return weight_kg / (height_m ** 2)

def classify_bmi(bmi_val: float) -> str:
    """Classifies BMI according to standard WHO categories."""
    if bmi_val < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_val < 25.0:
        return "Normal"
    elif 25.0 <= bmi_val < 30.0:
        return "Overweight"
    else:
        return "Obese"

class BMICalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Health & Progression Tracker — OIBSIP")
        self.geometry("860x720")
        self.minsize(800, 680)
        self.configure(bg="#F4F6F9")

        # Initialize database
        try:
            db.init_db()
        except db.DatabaseError as e:
            messagebox.showerror("Database Initialization Error", str(e))

        self.current_user_id = None
        self.users_cache = []

        self._setup_styles()
        self._build_ui()
        self._load_users()

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Configure generic colors
        self.style.configure(".", background="#F4F6F9", font=("Segoe UI", 10))
        self.style.configure("TLabel", background="#F4F6F9", foreground="#2C3E50")
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1A252F")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 10), foreground="#7F8C8D")
        self.style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        
        # Primary Action Button
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background="#2563EB", foreground="#FFFFFF")
        self.style.map("Primary.TButton", background=[("active", "#1D4ED8")])
        
        # Secondary Action Button
        self.style.configure("Secondary.TButton", font=("Segoe UI", 10), background="#E2E8F0", foreground="#1E293B")
        self.style.map("Secondary.TButton", background=[("active", "#CBD5E1")])

        # Treeview styling
        self.style.configure("Treeview", 
                             background="#FFFFFF", 
                             foreground="#1E293B", 
                             rowheight=26, 
                             fieldbackground="#FFFFFF",
                             font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#EDF2F7", foreground="#2D3748")

    def _build_ui(self):
        # 1. Top Header
        header_frame = tk.Frame(self, bg="#FFFFFF", padx=20, pady=12, highlightthickness=1, highlightbackground="#E2E8F0")
        header_frame.pack(fill="x", side="top")

        title_lbl = ttk.Label(header_frame, text="BMI Health & Progression Tracker", style="Header.TLabel", background="#FFFFFF")
        title_lbl.pack(anchor="w")
        sub_lbl = ttk.Label(header_frame, text="Oasis Infobyte Internship Task 2 · Multi-User Analytics & Trend Tracker", style="SubHeader.TLabel", background="#FFFFFF")
        sub_lbl.pack(anchor="w")

        # 2. Main Scrollable or Padded Container
        container = tk.Frame(self, bg="#F4F6F9", padx=20, pady=15)
        container.pack(fill="both", expand=True)

        # Top Bar: User Profile Section
        profile_card = tk.LabelFrame(container, text=" User Profile Management ", font=("Segoe UI", 10, "bold"),
                                     bg="#FFFFFF", fg="#1E293B", padx=15, pady=10, relief="groove")
        profile_card.pack(fill="x", pady=(0, 15))

        profile_inner = tk.Frame(profile_card, bg="#FFFFFF")
        profile_inner.pack(fill="x")

        tk.Label(profile_inner, text="Select Active Profile:", font=("Segoe UI", 10), bg="#FFFFFF", fg="#334155").pack(side="left", padx=(0, 10))
        
        self.user_combobox = ttk.Combobox(profile_inner, state="readonly", width=32, font=("Segoe UI", 10))
        self.user_combobox.pack(side="left", padx=(0, 10))
        self.user_combobox.bind("<<ComboboxSelected>>", self._on_user_selected)

        new_user_btn = ttk.Button(profile_inner, text="+ Add New Profile", style="Secondary.TButton", command=self._add_new_user)
        new_user_btn.pack(side="left", padx=(0, 15))

        self.active_user_badge = tk.Label(profile_inner, text="No profile selected", font=("Segoe UI", 9, "bold"),
                                          bg="#EFF6FF", fg="#1D4ED8", padx=10, pady=4, relief="flat")
        self.active_user_badge.pack(side="right")

        # Middle Section: Calculator (Left) and Result Card (Right)
        middle_frame = tk.Frame(container, bg="#F4F6F9")
        middle_frame.pack(fill="x", pady=(0, 15))

        # --- Left: Input Form ---
        calc_card = tk.LabelFrame(middle_frame, text=" Calculate BMI ", font=("Segoe UI", 10, "bold"),
                                  bg="#FFFFFF", fg="#1E293B", padx=15, pady=12, relief="groove")
        calc_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Weight Input
        tk.Label(calc_card, text="Weight (kg):", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=0, column=0, sticky="w", pady=(5, 2))
        self.weight_entry = ttk.Entry(calc_card, font=("Segoe UI", 10), width=18)
        self.weight_entry.grid(row=1, column=0, sticky="w", pady=(0, 10))

        # Height Input with Unit Selector
        tk.Label(calc_card, text="Height:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#334155").grid(row=2, column=0, sticky="w", pady=(0, 2))
        
        height_input_row = tk.Frame(calc_card, bg="#FFFFFF")
        height_input_row.grid(row=3, column=0, sticky="w", pady=(0, 15))

        self.height_entry = ttk.Entry(height_input_row, font=("Segoe UI", 10), width=12)
        self.height_entry.pack(side="left", padx=(0, 8))

        self.height_unit_var = tk.StringVar(value="Meters (m)")
        self.height_unit_combo = ttk.Combobox(height_input_row, textvariable=self.height_unit_var,
                                              values=["Meters (m)", "Centimeters (cm)"], state="readonly", width=15)
        self.height_unit_combo.pack(side="left")

        # Action Buttons
        btn_row = tk.Frame(calc_card, bg="#FFFFFF")
        btn_row.grid(row=4, column=0, sticky="w", pady=(5, 0))

        calc_btn = ttk.Button(btn_row, text="⚡ Calculate & Save", style="Primary.TButton", command=self._calculate_and_save)
        calc_btn.pack(side="left", padx=(0, 8))

        clear_btn = ttk.Button(btn_row, text="Clear", style="Secondary.TButton", command=self._clear_inputs)
        clear_btn.pack(side="left")

        # --- Right: Result Summary Card ---
        self.result_card = tk.LabelFrame(middle_frame, text=" Results & Health Evaluation ", font=("Segoe UI", 10, "bold"),
                                         bg="#FFFFFF", fg="#1E293B", padx=15, pady=12, relief="groove")
        self.result_card.pack(side="right", fill="both", expand=True)

        self.bmi_display_lbl = tk.Label(self.result_card, text="--.--", font=("Segoe UI", 36, "bold"), bg="#FFFFFF", fg="#94A3B8")
        self.bmi_display_lbl.pack(pady=(5, 2))

        self.category_badge = tk.Label(self.result_card, text="Awaiting Input", font=("Segoe UI", 10, "bold"),
                                       bg="#F1F5F9", fg="#64748B", padx=12, pady=4)
        self.category_badge.pack(pady=(0, 8))

        self.description_lbl = tk.Label(self.result_card, text="Enter your weight and height on the left to calculate your BMI and evaluate health metrics.",
                                        font=("Segoe UI", 9), bg="#FFFFFF", fg="#64748B", wraplength=320, justify="center")
        self.description_lbl.pack(pady=(0, 5))

        # Bottom Section: Historical Table & Visual Trend
        history_card = tk.LabelFrame(container, text=" Historical Records & Progression ", font=("Segoe UI", 10, "bold"),
                                     bg="#FFFFFF", fg="#1E293B", padx=15, pady=12, relief="groove")
        history_card.pack(fill="both", expand=True)

        # Toolbar
        history_toolbar = tk.Frame(history_card, bg="#FFFFFF")
        history_toolbar.pack(fill="x", pady=(0, 8))

        trend_btn = ttk.Button(history_toolbar, text="📈 View BMI Trend Graph", style="Primary.TButton", command=self._show_trend_chart)
        trend_btn.pack(side="left", padx=(0, 10))

        del_btn = ttk.Button(history_toolbar, text="🗑️ Delete Selected Entry", style="Secondary.TButton", command=self._delete_selected_record)
        del_btn.pack(side="left", padx=(0, 10))

        refresh_btn = ttk.Button(history_toolbar, text="🔄 Refresh Table", style="Secondary.TButton", command=self._load_records)
        refresh_btn.pack(side="left")

        # Treeview Table
        columns = ("id", "date", "weight", "height", "bmi", "category")
        self.tree = ttk.Treeview(history_card, columns=columns, show="headings", height=8, selectmode="browse")
        
        self.tree.heading("id", text="Rec ID")
        self.tree.heading("date", text="Recorded Date & Time")
        self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("height", text="Height (m)")
        self.tree.heading("bmi", text="BMI Value")
        self.tree.heading("category", text="Category")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("date", width=160, anchor="center")
        self.tree.column("weight", width=100, anchor="center")
        self.tree.column("height", width=100, anchor="center")
        self.tree.column("bmi", width=100, anchor="center")
        self.tree.column("category", width=130, anchor="center")

        tree_scrollbar = ttk.Scrollbar(history_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")

    def _load_users(self):
        """Loads users from database and populates profile selector."""
        try:
            self.users_cache = db.get_all_users()
            display_list = [u["display"] for u in self.users_cache]
            self.user_combobox["values"] = display_list

            if self.users_cache:
                # If there was a current user, keep it; otherwise select first
                target_idx = 0
                if self.current_user_id:
                    for idx, u in enumerate(self.users_cache):
                        if u["id"] == self.current_user_id:
                            target_idx = idx
                            break
                self.user_combobox.current(target_idx)
                self._on_user_selected()
            else:
                self.current_user_id = None
                self.user_combobox.set("")
                self.active_user_badge.config(text="No Profiles Yet — Click '+ Add New Profile'", fg="#DC2626", bg="#FEE2E2")
                self._clear_table()
        except db.DatabaseError as e:
            messagebox.showerror("Database Error", f"Unable to load user profiles:\n{e}")

    def _on_user_selected(self, event=None):
        selected_text = self.user_combobox.get()
        if not selected_text:
            return
        
        for u in self.users_cache:
            if u["display"] == selected_text:
                self.current_user_id = u["id"]
                self.active_user_badge.config(
                    text=f"Active Profile: {u['display']}",
                    fg="#1D4ED8",
                    bg="#EFF6FF"
                )
                self._load_records()
                break

    def _add_new_user(self):
        name = simpledialog.askstring("Add User Profile", "Enter User Name (e.g., Jawad):", parent=self)
        if name is None:
            return
        cleaned = name.strip()
        if not cleaned:
            messagebox.showwarning("Invalid Input", "User name cannot be empty.")
            return

        try:
            new_id, display_name = db.create_user(cleaned)
            # Informative notification highlighting ID separation
            messagebox.showinfo("Profile Created Successfully", 
                                f"New User Profile Created!\n\n"
                                f"Name: {cleaned}\n"
                                f"Unique User ID: {new_id}\n\n"
                                f"Displayed as: {display_name}")
            self.current_user_id = new_id
            self._load_users()
        except (db.DatabaseError, ValueError) as e:
            messagebox.showerror("Error Creating Profile", str(e))

    def _calculate_and_save(self):
        if not self.current_user_id:
            messagebox.showwarning("Profile Required", "Please select or create a User Profile first before calculating.")
            return

        weight_str = self.weight_entry.get().strip()
        height_str = self.height_entry.get().strip()

        # Input Validation
        if not weight_str or not height_str:
            messagebox.showerror("Missing Information", "Please enter both Weight and Height.")
            return

        try:
            weight = float(weight_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Weight must be a valid numeric number (e.g. 70.5).")
            return

        try:
            height = float(height_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Height must be a valid numeric number (e.g. 1.75 or 175).")
            return

        if weight <= 0 or height <= 0:
            messagebox.showerror("Value Range Error", "Weight and Height must both be greater than 0.")
            return

        if weight > 500 or weight < 2:
            messagebox.showwarning("Extreme Weight", "Please verify the weight value entered (range: 2kg to 500kg).")

        # Convert cm to meters if needed
        unit = self.height_unit_var.get()
        if "Centimeters" in unit:
            height_m = height / 100.0
        else:
            height_m = height

        if height_m > 3.0 or height_m < 0.4:
            messagebox.showerror("Invalid Height", "Height in meters should be realistic (0.4m to 3.0m).")
            return

        # Perform Calculation
        bmi_value = round(calculate_bmi(weight, height_m), 2)
        category = classify_bmi(bmi_value)

        # Update Result Card UI
        color = CATEGORY_COLORS.get(category, "#1E293B")
        self.bmi_display_lbl.config(text=f"{bmi_value:.2f}", fg=color)
        self.category_badge.config(text=f"{category.upper()}", bg=color, fg="#FFFFFF")
        self.description_lbl.config(text=CATEGORY_DESCRIPTIONS[category])

        # Save to Database
        try:
            db.add_bmi_record(self.current_user_id, weight, round(height_m, 2), bmi_value, category)
            self._load_records()
        except db.DatabaseError as e:
            messagebox.showerror("Persistence Error", f"Calculated successfully, but failed to save to database:\n{e}")

    def _clear_inputs(self):
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)

    def _clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _load_records(self):
        self._clear_table()
        if not self.current_user_id:
            return

        try:
            records = db.get_user_records(self.current_user_id)
            for r in records:
                # Format timestamp
                try:
                    dt = datetime.strptime(r["recorded_at"], "%Y-%m-%d %H:%M:%S")
                    formatted_date = dt.strftime("%Y-%m-%d %I:%M %p")
                except Exception:
                    formatted_date = r["recorded_at"]

                self.tree.insert("", "end", values=(
                    r["id"],
                    formatted_date,
                    f"{r['weight']:.1f}",
                    f"{r['height']:.2f}",
                    f"{r['bmi']:.2f}",
                    r["category"]
                ))
        except db.DatabaseError as e:
            messagebox.showerror("Database Error", f"Unable to fetch records:\n{e}")

    def _delete_selected_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Item", "Please select a record from the table to delete.")
            return

        values = self.tree.item(selected_item, "values")
        rec_id = int(values[0])
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Record #{rec_id}?")
        if confirm:
            try:
                db.delete_record(rec_id)
                self._load_records()
            except db.DatabaseError as e:
                messagebox.showerror("Delete Error", f"Failed to delete record:\n{e}")

    def _show_trend_chart(self):
        if not self.current_user_id:
            messagebox.showwarning("No Profile", "Please select a profile first.")
            return

        try:
            records = db.get_user_records(self.current_user_id)
            if not records:
                messagebox.showinfo("No Data", "No records found for this user profile yet. Calculate at least one entry to view trends.")
                return

            user_obj = db.get_user_by_id(self.current_user_id)
            user_title = user_obj["display"] if user_obj else f"User {self.current_user_id}"

            dates = []
            bmis = []
            for r in records:
                try:
                    dt = datetime.strptime(r["recorded_at"], "%Y-%m-%d %H:%M:%S")
                except Exception:
                    dt = datetime.now()
                dates.append(dt)
                bmis.append(r["bmi"])

            # Plotting with Matplotlib
            plt.style.use("seaborn-v0_8" if "seaborn-v0_8" in plt.style.available else "default")
            fig, ax = plt.subplots(figsize=(9, 5))

            # Plot user trend line
            ax.plot(dates, bmis, marker="o", color="#1E3A8A", linewidth=2.5, markersize=7, label="Your BMI")

            # Annotate points
            for d, b in zip(dates, bmis):
                ax.annotate(f"{b:.1f}", (d, b), textcoords="offset points", xytext=(0, 10), ha="center",
                            fontweight="bold", fontsize=9, color="#1E293B")

            # Benchmark shaded health bands
            y_min = min(min(bmis) - 2.0, 15.0)
            y_max = max(max(bmis) + 2.0, 35.0)
            ax.set_ylim(y_min, y_max)

            ax.axhspan(0, 18.5, color="#DBEAFE", alpha=0.5, label="Underweight (< 18.5)")
            ax.axhspan(18.5, 24.9, color="#DCFCE7", alpha=0.5, label="Normal Weight (18.5–24.9)")
            ax.axhspan(25.0, 29.9, color="#FEF3C7", alpha=0.5, label="Overweight (25–29.9)")
            ax.axhspan(30.0, 100, color="#FEE2E2", alpha=0.5, label="Obese (≥ 30.0)")

            ax.set_title(f"BMI Progression Trend — {user_title}", fontsize=14, fontweight="bold", pad=15)
            ax.set_xlabel("Date & Time of Measurement", fontsize=11, fontweight="bold", labelpad=10)
            ax.set_ylabel("BMI Value (kg/m²)", fontsize=11, fontweight="bold", labelpad=10)
            ax.grid(True, linestyle="--", alpha=0.6)

            # Date formatting on X-axis
            if len(dates) > 1 and (dates[-1] - dates[0]).total_seconds() > 86400:
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %Y"))
            else:
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d, %H:%M"))
            fig.autofmt_xdate()

            ax.legend(loc="upper right", frameon=True, facecolor="#FFFFFF")
            plt.tight_layout()
            plt.show()

        except db.DatabaseError as e:
            messagebox.showerror("Trend Chart Error", f"Failed to retrieve data for trend chart:\n{e}")
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Error generating chart:\n{e}")

if __name__ == "__main__":
    app = BMICalculatorApp()
    app.mainloop()
