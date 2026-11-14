# Live Weather & Forecast Dashboard (Task 4)

**Oasis Infobyte Internship Program (OIBSIP)**  
**Domain:** Python Programming  
**Author:** Jawad Ahmad  
**Level / Tier:** Advanced Tier (Desktop GUI Application via Tkinter + PIL/Pillow Icons + OpenWeatherMap REST API)

---

## 📌 Project Overview
The **Live Weather & Forecast Dashboard** is a Python desktop GUI application that fetches, processes, and displays real-time weather information and extended forecasts for any city or ZIP code globally.

Powered by the **OpenWeatherMap API**, this application provides a modern, intuitive weather monitoring center complete with dynamic weather condition icons, hourly forecast timelines, a 5-day daily forecast panel, automatic IP-based location detection, and seamless Celsius/Fahrenheit unit toggling.

---

## 🚀 Feature Checklist

### Beginner Tier Requirements
- [x] Search input supporting city names and international ZIP/postal codes.
- [x] REST API calls to OpenWeatherMap with JSON parsing.
- [x] Display of current temperature (both °C and °F supported), humidity percentage, wind speed, and weather condition descriptions.
- [x] Graceful error handling for invalid cities, network connection failures, and API authentication issues.
- [x] Input validation: Rejects blank queries and informs the user.

### Advanced Tier Requirements
- [x] **Desktop GUI Window:** Built using Python's native `tkinter` and `ttk` with a modern dark theme.
- [x] **Dynamic Weather Icons:** Downloads, caches, and renders high-resolution OpenWeatherMap condition icons using `PIL` (Pillow).
- [x] **Hourly Forecast Panel:** Displays real-time weather conditions and temperatures for upcoming hourly intervals.
- [x] **5-Day Extended Daily Forecast:** Aggregates and displays upcoming daily forecasts with min/max temperatures and condition summaries.
- [x] **Dynamic Unit Toggle Switch:** Instant one-click toggle between **Celsius (°C)** and **Fahrenheit (°F)** with live recalculation without re-fetching API data.
- [x] **Automatic Location Detection (Bonus):** "📍 Use My Location" button detects user city based on IP address using free geolocation services (`ip-api.com` / `ipinfo.io`).
- [x] **In-GUI Error Handling:** User-friendly alert banners displayed directly inside the GUI (no terminal print statements).
- [x] **Secure API Configuration:** Reads from a local `.env` file with an in-app GUI configuration dialog.

---

## 🛠️ Tech Stack & Architecture
- **Language:** Python 3.x
- **Networking & API:** `requests` (OpenWeatherMap API & Geolocation)
- **GUI Framework:** `tkinter` & `ttk` (Native Python GUI)
- **Image Processing:** `PIL` / `Pillow` (Condition icon rendering)
- **Environment Management:** Local `.env` configuration (ignored by git for security)

### Project Structure
```text
OIBSIP/
├── .venv/                                   # Shared virtual environment
├── requirements.txt                         # Master dependencies file
└── Python-Task4-WeatherApp/
    ├── app.py                               # Main Tkinter Desktop GUI Application
    ├── weather_api.py                       # OpenWeatherMap API engine & forecast aggregator
    ├── .env.example                         # Environment configuration template
    ├── .env                                 # Local API key storage (gitignored)
    ├── icons/                               # Cached weather condition icons (PNG)
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

### 2. Configure Your OpenWeatherMap API Key
1. Get your free API key at [https://openweathermap.org/](https://openweathermap.org/).
2. Open [`.env`](file:///d:/OASIS%20InfoBytes/OIBSIP/Python-Task4-WeatherApp/.env) and paste your key:
   ```env
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ```
   *(Alternatively, you can click **"🔑 Configure API Key"** directly inside the application GUI!)*

### 3. Run the Application
Launch the Desktop GUI application:
```bash
python Python-Task4-WeatherApp/app.py
```

---

## 🖥️ Application Features & Controls

1. **City Search:** Type any city (e.g. `New York`, `Tokyo`, `Paris, FR`) and click **"🔍 Get Weather"** or press `Enter`.
2. **Auto-Location:** Click **"📍 Use My Location"** to automatically detect your city via IP.
3. **Unit Switcher:** Click the toggle button in the top right to switch between **Celsius (°C)** and **Fahrenheit (°F)**.
4. **Current Weather Card:** View live temperature, condition icon, feels-like temperature, humidity, wind speed, and atmospheric pressure.
5. **Forecast Panels:** Review upcoming 18-hour hourly trends and the 5-day daily forecast.

---

## 📄 License & Acknowledgements
Developed as part of the **Oasis Infobyte Internship Program (OIBSIP)** under the AICTE initiative.
