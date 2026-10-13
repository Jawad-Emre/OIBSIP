# Oasis Infobyte Internship Program (OIBSIP)

**Intern Name:** Jawad Ahmad  
**Domain:** Python Programming  
**Internship ID:** OIB/O2/IP5683  
**Batch:** October – November 2026  

---

## 📌 Repository Overview
This repository contains all project deliverables and task submissions completed during the **Oasis Infobyte Internship Program (OIBSIP)**.

Every project is organized into its dedicated folder adhering strictly to the required naming standard:  
`OIBSIP/[TrackName]-[Level/Task]-[ProjectName]/`

---

## 📂 Assigned Projects & Status

| Task # | Project Folder | Level / Tier | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Task 2** | [**`Python-Task2-BMICalculator`**](./Python-Task2-BMICalculator) | Advanced Tier | Dual-interface BMI Health Tracker with Modern Web Dashboard (Flask + Chart.js) & Desktop GUI (Tkinter + Matplotlib) with SQLite multi-user ID separation. | ✅ Completed |
| **Task 3** | `Python-Task3-PasswordGenerator` | Advanced Tier | Cryptographically secure random password generator with GUI controls & clipboard integration. | ⏳ In Progress |
| **Task 4** | `Python-Task4-WeatherApp` | Advanced Tier | Real-time weather dashboard with OpenWeatherMap API & condition forecasts. | ⏳ Upcoming |

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

## 📜 Submission Guidelines Compliance
- **Repository Name:** `OIBSIP`
- **Folder Structure:** `[TrackName]-[Level/Task]-[ProjectName]/`
- **Documentation:** Every task folder includes a dedicated `README.md` with features, architecture, and running instructions.
- **Data Persistence:** SQLite database with unique User ID separation.
