# Random Password Generator (Task 3)

**Oasis Infobyte Internship Program (OIBSIP)**  
**Domain:** Python Programming  
**Author:** Jawad Ahmad  
**Level / Tier:** Advanced Tier (Desktop GUI Application via Tkinter + Secrets Module + Pyperclip Clipboard Integration)

---

## 📌 Project Overview
The **Random Password Generator** is a Python desktop GUI tool engineered to generate cryptographically secure, randomized passwords based on custom user requirements.

Unlike standard generators that rely on pseudorandom algorithms (`random`), this application utilizes Python's standard `secrets` module (`SystemRandom`) to generate passwords suitable for securing sensitive personal accounts, databases, and encryption keys.

---

## 🚀 Feature Checklist

### Beginner Tier Requirements
- [x] Length specification with a strictly enforced minimum of 8 characters.
- [x] Character type customization: Uppercase (`A-Z`), Lowercase (`a-z`), Numbers (`0-9`), and Symbols (`!@#$%...`).
- [x] Input validation: Rejects lengths under 8 and requires at least 2 character types selected.
- [x] Generates and displays passwords matching all specified criteria.
- [x] Reusable: Generate unlimited passwords without restarting the application.

### Advanced Tier Requirements
- [x] **Desktop GUI:** Built with Python's native `tkinter` and `ttk` library with a modern dark theme.
- [x] **Precision Length Controls:** Synchronized slider and numerical spinbox (range: 8 to 64).
- [x] **Cryptographically Secure Engine:** Powered exclusively by Python's `secrets` module instead of `random`.
- [x] **Guaranteed Inclusion Rule:** Ensures the generated password contains at least one character from each selected character set.
- [x] **Exclude Ambiguous Characters:** Optional filter to omit easily confused characters (`0`, `O`, `l`, `1`, `I`).
- [x] **Dynamic Visual Strength Meter:** Color-coded progress bar and badge dynamically classifying strength (`Weak`, `Medium`, `Strong`, `Very Strong`).
- [x] **Clipboard Integration (`pyperclip`):** One-click "Copy" button with automatic clipboard copy on generation.
- [x] **In-Memory Session History:** Real-time table displaying the last 5 generated passwords during the session (strictly in-memory, never persisted to disk for cybersecurity best practices).

---

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Cryptographic Engine:** `secrets` (Python Standard Library)
- **GUI Framework:** `tkinter` & `ttk` (Native Python GUI)
- **Clipboard Management:** `pyperclip`

### Project Structure
```text
OIBSIP/
├── .venv/                                   # Shared virtual environment
├── requirements.txt                         # Master dependencies file
└── Python-Task3-PasswordGenerator/
    ├── app.py                               # Main Tkinter Desktop GUI Application
    ├── generator.py                         # Secure generation logic, entropy & history
    └── README.md                            # Comprehensive task documentation
```

---

## ⚙️ Installation & Running

### 1. Activate the Virtual Environment
From the root `OIBSIP` directory, activate the shared virtual environment:

```powershell
# In PowerShell (Windows):
.\.venv\Scripts\Activate.ps1
```

```cmd
# In Command Prompt (cmd):
.venv\Scripts\activate.bat
```

### 2. Verify Dependencies
Dependencies are already included in the root `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Launch the Desktop GUI application:
```bash
python Python-Task3-PasswordGenerator/app.py
```

---

## 🖥️ Application Controls & Usage

1. **Adjust Length:** Move the slider or type into the spinbox (8 to 64 characters).
2. **Select Character Sets:** Check or uncheck Uppercase, Lowercase, Numbers, or Symbols (at least 2 required).
3. **Exclude Ambiguous:** Check *"Exclude Ambiguous Characters"* to avoid confusing `0` vs `O` or `1` vs `l`.
4. **Generate:** Click **"⚡ Generate Strong Password"**. The password is generated, evaluated for strength, and copied directly to your clipboard.
5. **Session History:** View the last 5 passwords generated in your session. Double-click or click **"Copy Selected"** to reuse any previous password.

---

## 📄 License & Acknowledgements
Developed as part of the **Oasis Infobyte Internship Program (OIBSIP)** under the AICTE initiative.
