"""
Weather Application — Desktop GUI (Advanced Tier)
Oasis Infobyte Internship Program (OIBSIP) Task 4
Author: Jawad Ahmad

Tech Stack:
- Python 3.x
- requests (REST API)
- tkinter & ttk (Native Desktop GUI)
- PIL / Pillow (Icon rendering)
- OpenWeatherMap API & Geolocation

Features:
- Real-time weather lookup by City Name or ZIP code
- Automatic IP-based geolocation button ("📍 Use My Location")
- Dynamic Unit Toggle (°C / °F) with instant recalculation
- High-resolution weather condition icons rendered via PIL
- Hourly forecast panel (next 6 intervals / 18 hours)
- 5-day daily forecast panel with min/max temperatures
- Metric cards for Humidity, Wind Speed, Pressure, and Feels Like
- In-GUI error messaging & inline API key configuration dialog
- Full viewport scrolling support (Canvas + Mousewheel)
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from typing import Optional

import weather_api

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather & Forecast Dashboard — OIBSIP Task 4")
        self.geometry("860x780")
        self.minsize(780, 620)
        self.configure(bg="#0F172A")  # Modern deep slate navy background

        # State Variables
        self.unit_var = tk.StringVar(value="C")  # "C" or "F"
        self.search_var = tk.StringVar(value="")
        self.api_key = weather_api.load_api_key()
        self.weather_cache = None  # Holds the current fetched data
        self.icon_images = []     # Keeps references to prevent garbage collection

        self._setup_styles()
        self._build_ui()

        # Check API Key on startup
        if not self.api_key:
            self._show_error_banner("⚠️ OpenWeatherMap API key is missing. Click '🔑 Configure API Key' above to set it.")
        else:
            # Auto-detect location or default to London for immediate display
            self._initial_load()

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Base configuration
        self.style.configure(".", background="#0F172A", foreground="#F8FAFC", font=("Segoe UI", 10))
        
        # Primary Action Button
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background="#2563EB", foreground="#FFFFFF")
        self.style.map("Primary.TButton", background=[("active", "#1D4ED8")])

        # Secondary Action Button
        self.style.configure("Secondary.TButton", font=("Segoe UI", 9, "bold"), background="#334155", foreground="#F8FAFC")
        self.style.map("Secondary.TButton", background=[("active", "#475569")])

        # Toggle Button Style
        self.style.configure("Toggle.TButton", font=("Segoe UI", 10, "bold"), background="#1E293B", foreground="#38BDF8")
        self.style.map("Toggle.TButton", background=[("active", "#334155")])

        # Scrollbar
        self.style.configure("Vertical.TScrollbar", background="#1E293B", troughcolor="#0F172A", arrowcolor="#38BDF8")

    def _build_ui(self):
        # 1. Top Header Banner
        header = tk.Frame(self, bg="#1E293B", padx=20, pady=12, highlightthickness=1, highlightbackground="#334155")
        header.pack(fill="x", side="top")

        hdr_top = tk.Frame(header, bg="#1E293B")
        hdr_top.pack(fill="x")

        title_lbl = tk.Label(hdr_top, text="🌤️ Live Weather & Forecast Dashboard", font=("Segoe UI", 16, "bold"), bg="#1E293B", fg="#FFFFFF")
        title_lbl.pack(side="left")

        # Right-side utilities: Key setup & Unit Toggle
        util_frame = tk.Frame(hdr_top, bg="#1E293B")
        util_frame.pack(side="right")

        key_btn = ttk.Button(util_frame, text="🔑 Configure API Key", style="Secondary.TButton", command=self._prompt_api_key)
        key_btn.pack(side="left", padx=(0, 10))

        self.unit_toggle_btn = ttk.Button(util_frame, text="Switch to °F", style="Toggle.TButton", command=self._toggle_units)
        self.unit_toggle_btn.pack(side="left")

        sub_lbl = tk.Label(header, text="Oasis Infobyte Internship Program · Python Programming Track · Task 4 (Advanced Tier)",
                           font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8")
        sub_lbl.pack(anchor="w", pady=(2, 0))

        # Inline Error Banner Frame (Hidden by default)
        self.error_banner = tk.Frame(self, bg="#7F1D1D", padx=16, pady=8, highlightthickness=1, highlightbackground="#EF4444")
        self.error_lbl = tk.Label(self.error_banner, text="", font=("Segoe UI", 9, "bold"), bg="#7F1D1D", fg="#FEE2E2", wraplength=760, justify="left")
        self.error_lbl.pack(side="left", fill="x", expand=True)
        dismiss_btn = tk.Button(self.error_banner, text="✕", font=("Segoe UI", 9, "bold"), bg="#7F1D1D", fg="#FCA5A5",
                                relief="flat", cursor="hand2", command=self._hide_error_banner)
        dismiss_btn.pack(side="right")

        # 2. Main Scrollable Container (Canvas + Scrollbar)
        main_frame = tk.Frame(self, bg="#0F172A")
        main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main_frame, bg="#0F172A", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)

        self.content = tk.Frame(self.canvas, bg="#0F172A", padx=20, pady=15)
        self.content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas_window = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # --- Section A: Search & Location Bar ---
        search_card = tk.Frame(self.content, bg="#1E293B", padx=16, pady=14, highlightthickness=1, highlightbackground="#334155")
        search_card.pack(fill="x", pady=(0, 15))

        search_row = tk.Frame(search_card, bg="#1E293B")
        search_row.pack(fill="x")

        tk.Label(search_row, text="Location:", font=("Segoe UI", 10, "bold"), bg="#1E293B", fg="#E2E8F0").pack(side="left", padx=(0, 10))

        self.search_entry = tk.Entry(search_row, textvariable=self.search_var, font=("Segoe UI", 11),
                                     bg="#0F172A", fg="#F8FAFC", insertbackground="#38BDF8", relief="flat",
                                     highlightthickness=1, highlightbackground="#334155", highlightcolor="#38BDF8")
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_weather())

        get_btn = ttk.Button(search_row, text="🔍 Get Weather", style="Primary.TButton", command=self.search_weather)
        get_btn.pack(side="left", ipady=4, padx=(0, 8))

        loc_btn = ttk.Button(search_row, text="📍 Use My Location", style="Secondary.TButton", command=self.use_my_location)
        loc_btn.pack(side="left", ipady=4)

        # --- Section B: Current Weather Hero Card ---
        self.hero_card = tk.Frame(self.content, bg="#1E293B", padx=20, pady=20, highlightthickness=1, highlightbackground="#334155")
        self.hero_card.pack(fill="x", pady=(0, 15))

        hero_top = tk.Frame(self.hero_card, bg="#1E293B")
        hero_top.pack(fill="x")

        # Left info: City, country, and time
        city_info = tk.Frame(hero_top, bg="#1E293B")
        city_info.pack(side="left")

        self.city_lbl = tk.Label(city_info, text="Search for a city...", font=("Segoe UI", 20, "bold"), bg="#1E293B", fg="#FFFFFF")
        self.city_lbl.pack(anchor="w")

        self.time_lbl = tk.Label(city_info, text="", font=("Segoe UI", 10), bg="#1E293B", fg="#94A3B8")
        self.time_lbl.pack(anchor="w")

        # Right weather badge
        self.cond_badge = tk.Label(hero_top, text="", font=("Segoe UI", 10, "bold"), bg="#0F172A", fg="#38BDF8", padx=12, pady=4)
        self.cond_badge.pack(side="right")

        # Center Temperature & Icon Banner
        hero_center = tk.Frame(self.hero_card, bg="#1E293B")
        hero_center.pack(fill="x", pady=(15, 15))

        self.icon_lbl = tk.Label(hero_center, bg="#1E293B")
        self.icon_lbl.pack(side="left", padx=(0, 15))

        temp_box = tk.Frame(hero_center, bg="#1E293B")
        temp_box.pack(side="left")

        self.temp_lbl = tk.Label(temp_box, text="--°", font=("Segoe UI", 44, "bold"), bg="#1E293B", fg="#38BDF8")
        self.temp_lbl.pack(anchor="w")

        self.desc_lbl = tk.Label(temp_box, text="Awaiting search", font=("Segoe UI", 12), bg="#1E293B", fg="#E2E8F0")
        self.desc_lbl.pack(anchor="w")

        self.feels_lbl = tk.Label(temp_box, text="Feels like: --°", font=("Segoe UI", 10), bg="#1E293B", fg="#94A3B8")
        self.feels_lbl.pack(anchor="w")

        # Bottom Metrics Grid (Humidity, Wind, Pressure)
        metrics_frame = tk.Frame(self.hero_card, bg="#1E293B")
        metrics_frame.pack(fill="x", pady=(10, 0))

        # 3 Metric boxes
        self.box_humidity = self._create_metric_card(metrics_frame, "💧 Humidity", "--%")
        self.box_humidity.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.box_wind = self._create_metric_card(metrics_frame, "💨 Wind Speed", "-- m/s")
        self.box_wind.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.box_pressure = self._create_metric_card(metrics_frame, "⏲️ Pressure", "-- hPa")
        self.box_pressure.pack(side="left", fill="x", expand=True)

        # --- Section C: Hourly Forecast Panel ---
        self.hourly_frame = tk.Frame(self.content, bg="#1E293B", padx=18, pady=16, highlightthickness=1, highlightbackground="#334155")
        self.hourly_frame.pack(fill="x", pady=(0, 15))

        tk.Label(self.hourly_frame, text="⏱️ Hourly Forecast (Next 18 Hours)", font=("Segoe UI", 11, "bold"), bg="#1E293B", fg="#38BDF8").pack(anchor="w", pady=(0, 10))

        self.hourly_cards_container = tk.Frame(self.hourly_frame, bg="#1E293B")
        self.hourly_cards_container.pack(fill="x")

        # Placeholder message
        self.hourly_empty_lbl = tk.Label(self.hourly_cards_container, text="Hourly forecast will appear here once a city is searched.",
                                         font=("Segoe UI", 9, "italic"), bg="#1E293B", fg="#64748B")
        self.hourly_empty_lbl.pack(pady=10)

        # --- Section D: 5-Day Daily Forecast Panel ---
        self.daily_frame = tk.Frame(self.content, bg="#1E293B", padx=18, pady=16, highlightthickness=1, highlightbackground="#334155")
        self.daily_frame.pack(fill="x", pady=(0, 10))

        tk.Label(self.daily_frame, text="📅 5-Day Extended Forecast", font=("Segoe UI", 11, "bold"), bg="#1E293B", fg="#38BDF8").pack(anchor="w", pady=(0, 10))

        self.daily_cards_container = tk.Frame(self.daily_frame, bg="#1E293B")
        self.daily_cards_container.pack(fill="x")

        self.daily_empty_lbl = tk.Label(self.daily_cards_container, text="5-day forecast will appear here once a city is searched.",
                                       font=("Segoe UI", 9, "italic"), bg="#1E293B", fg="#64748B")
        self.daily_empty_lbl.pack(pady=10)

    def _create_metric_card(self, parent, title: str, default_val: str):
        card = tk.Frame(parent, bg="#0F172A", padx=12, pady=10, highlightthickness=1, highlightbackground="#334155")
        lbl_title = tk.Label(card, text=title, font=("Segoe UI", 9), bg="#0F172A", fg="#94A3B8")
        lbl_title.pack(anchor="w")
        lbl_val = tk.Label(card, text=default_val, font=("Segoe UI", 13, "bold"), bg="#0F172A", fg="#F8FAFC")
        lbl_val.pack(anchor="w", pady=(2, 0))
        card.value_label = lbl_val
        return card

    def _on_mousewheel(self, event):
        if self.canvas.winfo_height() < self.content.winfo_height():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _show_error_banner(self, message: str):
        self.error_lbl.config(text=message)
        self.error_banner.pack(fill="x", side="top", before=self.canvas.master)

    def _hide_error_banner(self):
        self.error_banner.pack_forget()

    def _prompt_api_key(self):
        new_key = simpledialog.askstring("OpenWeatherMap API Key",
                                          "Enter your OpenWeatherMap API Key:\n(Saved locally into .env)",
                                          initialvalue=self.api_key, parent=self)
        if new_key is not None:
            cleaned = new_key.strip()
            if cleaned:
                self.api_key = cleaned
                weather_api.save_api_key(cleaned)
                self._hide_error_banner()
                messagebox.showinfo("API Key Configured", "API Key saved successfully to .env!\nFetching weather data now...")
                if self.search_var.get().strip():
                    self.search_weather()
                else:
                    self.use_my_location()
            else:
                messagebox.showwarning("Empty Key", "API key was left empty.")

    def _toggle_units(self):
        if self.unit_var.get() == "C":
            self.unit_var.set("F")
            self.unit_toggle_btn.config(text="Switch to °C")
        else:
            self.unit_var.set("C")
            self.unit_toggle_btn.config(text="Switch to °F")

        # If data is cached, re-render immediately without needing an API call!
        if self.weather_cache:
            self._render_weather(self.weather_cache)

    def _initial_load(self):
        # Auto load by IP location or default city
        self.use_my_location()

    def use_my_location(self):
        self._hide_error_banner()
        try:
            city = weather_api.detect_user_location()
            self.search_var.set(city)
            self.search_weather()
        except Exception:
            # Default fallback city if IP detection is unavailable
            self.search_var.set("London")
            self.search_weather()

    def search_weather(self):
        query = self.search_var.get().strip()
        if not query:
            self._show_error_banner("Please enter a city name or ZIP code.")
            return

        if not self.api_key:
            self._show_error_banner("⚠️ OpenWeatherMap API key is required. Click '🔑 Configure API Key' to enter it.")
            self._prompt_api_key()
            return

        self._hide_error_banner()
        self.city_lbl.config(text=f"Fetching weather for {query}...")

        try:
            data = weather_api.fetch_weather_data(query, self.api_key)
            self.weather_cache = data
            self._render_weather(data)
        except (ValueError, LookupError, PermissionError, ConnectionError, RuntimeError) as e:
            self._show_error_banner(str(e))
            self.city_lbl.config(text="Location not loaded")

    def _render_weather(self, data: dict):
        unit = self.unit_var.get()
        is_c = (unit == "C")
        unit_sym = "°C" if is_c else "°F"

        curr = data["current"]

        # Update Hero Card Texts
        country_str = f", {curr['country']}" if curr['country'] else ""
        self.city_lbl.config(text=f"{curr['city']}{country_str}")
        self.time_lbl.config(text=curr['timestamp'])

        temp_val = curr["temp_c"] if is_c else curr["temp_f"]
        feels_val = curr["feels_c"] if is_c else curr["feels_f"]

        self.temp_lbl.config(text=f"{temp_val:.1f} {unit_sym}")
        self.desc_lbl.config(text=curr["description"])
        self.feels_lbl.config(text=f"Feels like: {feels_val:.1f} {unit_sym}")
        self.cond_badge.config(text=curr["condition"].upper())

        # Metrics Card Updates
        self.box_humidity.value_label.config(text=f"{curr['humidity']}%")
        if is_c:
            self.box_wind.value_label.config(text=f"{curr['wind_ms']} m/s")
        else:
            self.box_wind.value_label.config(text=f"{curr['wind_mph']} mph")
        self.box_pressure.value_label.config(text=f"{curr['pressure']} hPa")

        # Load Current Icon
        self._load_icon(curr.get("icon_path"), self.icon_lbl, size=(80, 80))

        # Render Hourly Forecast
        self._render_hourly(data.get("hourly", []), unit_sym, is_c)

        # Render Daily Forecast
        self._render_daily(data.get("daily", []), unit_sym, is_c)

    def _load_icon(self, path: Optional[str], label_widget: tk.Label, size=(50, 50)):
        if path and os.path.exists(path):
            try:
                img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label_widget.config(image=photo, text="")
                self.icon_images.append(photo)  # Retain reference
                return
            except Exception:
                pass
        # Fallback text if icon is unavailable
        label_widget.config(image="", text="☁️", font=("Segoe UI", 24))

    def _render_hourly(self, hourly_list: list, unit_sym: str, is_c: bool):
        # Clear previous cards
        for widget in self.hourly_cards_container.winfo_children():
            widget.destroy()

        if not hourly_list:
            tk.Label(self.hourly_cards_container, text="No hourly forecast available.",
                     font=("Segoe UI", 9, "italic"), bg="#1E293B", fg="#64748B").pack(pady=10)
            return

        for item in hourly_list:
            card = tk.Frame(self.hourly_cards_container, bg="#0F172A", padx=14, pady=10,
                            highlightthickness=1, highlightbackground="#334155")
            card.pack(side="left", fill="both", expand=True, padx=4)

            # Time
            tk.Label(card, text=item["time"], font=("Segoe UI", 9, "bold"), bg="#0F172A", fg="#E2E8F0").pack(anchor="center")

            # Icon
            icon_lbl = tk.Label(card, bg="#0F172A")
            icon_lbl.pack(anchor="center", pady=3)
            self._load_icon(item.get("icon_path"), icon_lbl, size=(42, 42))

            # Temp
            t_val = item["temp_c"] if is_c else item["temp_f"]
            tk.Label(card, text=f"{t_val:.1f}{unit_sym}", font=("Segoe UI", 10, "bold"), bg="#0F172A", fg="#38BDF8").pack(anchor="center")

            # Short Condition
            tk.Label(card, text=item["condition"], font=("Segoe UI", 8), bg="#0F172A", fg="#94A3B8").pack(anchor="center")

    def _render_daily(self, daily_list: list, unit_sym: str, is_c: bool):
        # Clear previous daily cards
        for widget in self.daily_cards_container.winfo_children():
            widget.destroy()

        if not daily_list:
            tk.Label(self.daily_cards_container, text="No extended forecast available.",
                     font=("Segoe UI", 9, "italic"), bg="#1E293B", fg="#64748B").pack(pady=10)
            return

        for item in daily_list:
            row = tk.Frame(self.daily_cards_container, bg="#0F172A", padx=16, pady=8,
                           highlightthickness=1, highlightbackground="#334155")
            row.pack(fill="x", pady=4)

            # Day & Date
            day_box = tk.Frame(row, bg="#0F172A", width=140)
            day_box.pack(side="left")
            day_box.pack_propagate(False)

            tk.Label(day_box, text=item["day_name"], font=("Segoe UI", 10, "bold"), bg="#0F172A", fg="#FFFFFF").pack(anchor="w")
            tk.Label(day_box, text=item["date"], font=("Segoe UI", 8), bg="#0F172A", fg="#94A3B8").pack(anchor="w")

            # Icon & Condition
            cond_box = tk.Frame(row, bg="#0F172A")
            cond_box.pack(side="left", padx=(10, 0))

            icon_lbl = tk.Label(cond_box, bg="#0F172A")
            icon_lbl.pack(side="left")
            self._load_icon(item.get("icon_path"), icon_lbl, size=(38, 38))

            tk.Label(cond_box, text=item["description"], font=("Segoe UI", 9), bg="#0F172A", fg="#E2E8F0").pack(side="left", padx=(8, 0))

            # Min / Max Temperatures
            temp_box = tk.Frame(row, bg="#0F172A")
            temp_box.pack(side="right")

            min_val = item["min_c"] if is_c else item["min_f"]
            max_val = item["max_c"] if is_c else item["max_f"]

            tk.Label(temp_box, text=f"{min_val:.1f}{unit_sym}", font=("Segoe UI", 10), bg="#0F172A", fg="#94A3B8").pack(side="left", padx=(0, 8))
            tk.Label(temp_box, text="—", font=("Segoe UI", 10), bg="#0F172A", fg="#64748B").pack(side="left", padx=(0, 8))
            tk.Label(temp_box, text=f"{max_val:.1f}{unit_sym}", font=("Segoe UI", 10, "bold"), bg="#0F172A", fg="#38BDF8").pack(side="left")

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
