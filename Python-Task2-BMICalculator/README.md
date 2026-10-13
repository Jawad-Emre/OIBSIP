# BMI Health & Progression Tracker (Task 2)

**Oasis Infobyte Internship Program (OIBSIP)**  
**Domain:** Python Programming  
**Author:** Jawad Ahmad  
**Level / Tier:** Advanced Tier (Modern Web Dashboard + Desktop GUI + SQLite Multi-User Persistence + Matplotlib / Chart.js Analytics)

---

## 📌 Project Overview
The **BMI Health & Progression Tracker** is a Python application engineered to compute, classify, record, and visually analyze Body Mass Index (BMI) over time.

This project delivers **Dual Interface Support** connected to a unified SQLite database:
1. **🌐 Modern Web Dashboard (`web_app.py`):** Powered by Flask, SQLite, Tailwind CSS, and Chart.js. Delivers a clean, responsive SaaS fitness tracking dashboard with live BMI gauge and interactive time-series charts.
2. **🖥️ Classic Desktop GUI (`app.py`):** Built with Python's native `tkinter`, `ttk`, and `matplotlib` to provide a standalone desktop application window.

Both interfaces share the same unified SQLite database (`bmi_records.db`), so records and profiles created in one are instantly accessible in the other.

---

## 🚀 Feature Checklist

### Beginner Tier Requirements
- [x] Input prompts for weight (kg) and height (meters or centimeters).
- [x] Precision BMI calculation using the formula:  
  $$\text{BMI} = \frac{\text{Weight (kg)}}{(\text{Height (m)})^2}$$
- [x] Standard classification into WHO health categories:
  - **Underweight:** $< 18.5$ (Blue)
  - **Normal Weight:** $18.5 - 24.9$ (Green)
  - **Overweight:** $25.0 - 29.9$ (Amber/Orange)
  - **Obese:** $\ge 30.0$ (Red)
- [x] Rounded BMI display to 2 decimal places.
- [x] Comprehensive input validation rejecting non-numeric, zero, negative, and extreme outlier values.

### Advanced Tier Requirements
- [x] **Dual Interfaces:** Modern Web Dashboard (Flask + Chart.js) and Native Desktop Window (`tkinter` + `matplotlib`).
- [x] **Multi-User Profile Support with Unique Auto-Generated IDs:** Enables individual profiles with separate tracking. Eliminates ambiguity between users who share the same name (e.g., `Jawad (ID: 1)` vs `Jawad (ID: 2)`).
- [x] **Color-Coded Feedback Badges:** Instant visual indication of health status.
- [x] **SQLite Database Integration:** Automatic local storage (`bmi_records.db`) with full CRUD support (Add, View, Delete records).
- [x] **Visual Trend Analytics:** Interactive time-series graph with WHO reference bands.
- [x] **Graceful Error Handling:** Exception handling for database read/write failures.

---

## 🛠️ Tech Stack & Architecture
- **Backend & Core:** Python 3.x, `sqlite3`
- **Web App:** Flask, Tailwind CSS, Chart.js, FontAwesome
- **Desktop GUI:** `tkinter`, `ttk`, `matplotlib`

### Project Structure
```text
OIBSIP/
├── .venv/                                   # Shared virtual environment
├── .gitignore                               # Git ignore configuration
├── requirements.txt                         # Master dependencies file
└── Python-Task2-BMICalculator/
    ├── web_app.py                           # Modern Flask Web Dashboard (auto-opens in browser)
    ├── app.py                               # Classic Tkinter Desktop GUI Window
    ├── database.py                          # Unified SQLite database manager (CRUD operations)
    ├── templates/
    │   └── index.html                       # Tailwind CSS & Chart.js Web UI
    ├── README.md                            # Comprehensive project documentation
    └── bmi_records.db                       # Unified SQLite database
```

---

## ⚙️ Installation & Setup

### 1. Activate the Virtual Environment
From the root `OIBSIP` directory, activate the shared virtual environment:

```powershell
# In PowerShell:
.\.venv\Scripts\Activate.ps1
```

```cmd
# In Command Prompt:
.venv\Scripts\activate.bat
```

### 2. Install Dependencies
Install all required packages from the root requirements file:
```bash
pip install -r requirements.txt
```

---

## 🖥️ Running the Application

### Option A: Modern Web Dashboard
```bash
python Python-Task2-BMICalculator/web_app.py
```
> Automatically opens `http://127.0.0.1:5000` in your web browser with live animations, smooth cards, and interactive Chart.js graphs.

### Option B: Native Desktop GUI Window
```bash
python Python-Task2-BMICalculator/app.py
```
> Launches the Tkinter native desktop application with Matplotlib visual charts.

---

## 📄 License & Acknowledgements
Developed as part of the **Oasis Infobyte Internship Program (OIBSIP)** under the AICTE initiative.
