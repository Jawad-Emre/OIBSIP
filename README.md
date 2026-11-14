# Oasis Infobyte Internship Program (OIBSIP)

**Intern Name:** Jawad Ahmad  
**Domain:** Python Programming  
**Internship ID:** OIB/O2/IP5683  
**Batch:** October – November 2026  

---

## 📌 Repository Overview
This repository contains all project deliverables and task submissions completed during the **Oasis Infobyte Internship Program (OIBSIP)** under the AICTE initiative.

Every project is organized into its dedicated folder adhering strictly to the official naming standard:  
`OIBSIP/[TrackName]-[Level/Task]-[ProjectName]/`

---

## 📂 Completed Projects Matrix (All Advanced Tier)

| Task # | Project Folder | Level / Tier | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Task 2** | [**`Python-Task2-BMICalculator`**](./Python-Task2-BMICalculator) | Advanced Tier | Dual-interface BMI Health Tracker with Modern Web Dashboard (Flask + Chart.js) & Desktop GUI (Tkinter + Matplotlib) with SQLite multi-user ID separation. | ✅ Completed |
| **Task 3** | [**`Python-Task3-PasswordGenerator`**](./Python-Task3-PasswordGenerator) | Advanced Tier | Cryptographically secure desktop random password generator using Python's `secrets` module, Tkinter GUI, dynamic strength meter, and `pyperclip` clipboard integration. | ✅ Completed |
| **Task 4** | [**`Python-Task4-WeatherApp`**](./Python-Task4-WeatherApp) | Advanced Tier | Real-time weather monitoring dashboard using OpenWeatherMap REST API, PIL condition icons, hourly forecast panel, 5-day daily forecast, and IP auto-location. | ✅ Completed |

---

## 🛠️ Environment Setup & Installation

All projects share a common virtual environment and dependencies defined in the root of this repository.

### 1. Clone the Repository
```bash
git clone https://github.com/Jawad-Emre/OIBSIP.git
cd OIBSIP
```

### 2. Create & Activate Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate in PowerShell (Windows):
.\.venv\Scripts\Activate.ps1

# Or in Linux / macOS:
source .venv/bin/activate
```

### 3. Install Master Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Applications

### Task 2: BMI Calculator
```bash
# Modern Web Dashboard:
python Python-Task2-BMICalculator/web_app.py

# Or Classic Desktop Window:
python Python-Task2-BMICalculator/app.py
```

### Task 3: Random Password Generator
```bash
python Python-Task3-PasswordGenerator/app.py
```

### Task 4: Weather & Forecast App
```bash
python Python-Task4-WeatherApp/app.py
```

---

## 📜 Submission Guidelines Compliance
- **Repository Name:** Exact match (`OIBSIP`).
- **Folder Structure:** Exact match (`[TrackName]-[Level/Task]-[ProjectName]/`).
- **Documentation:** Every task folder includes a dedicated, comprehensive `README.md`.
- **Data Persistence & Security:** SQLite relational database with unique User ID separation for Task 2, cryptographically secure `secrets` module for Task 3, and private `.env` configuration for Task 4.
- **Requirement Target:** Completed **3 out of 3 required tasks** at the **Advanced Tier**.
