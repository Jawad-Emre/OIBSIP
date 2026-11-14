"""
Weather API Integration Module — Oasis Infobyte SIP Task 4 (Advanced Tier)
Author: Jawad Ahmad

Handles:
- OpenWeatherMap API communication (Current Weather & 5-Day/3-Hour Forecast)
- Environment variable / .env configuration loading
- IP-based automatic geolocation (ip-api.com / ipinfo.io)
- Hourly and daily forecast data processing
- Icon caching via requests and PIL
"""

import os
import re
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "icons")
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Ensure icons cache directory exists
os.makedirs(ICONS_DIR, exist_ok=True)

def load_api_key() -> str:
    """
    Reads OPENWEATHER_API_KEY from environment or .env file.
    """
    # 1. Check OS environment variable
    key = os.environ.get("OPENWEATHER_API_KEY", "").strip()
    if key:
        return key

    # 2. Check local .env file
    if os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() == "OPENWEATHER_API_KEY":
                            return v.strip().strip('"').strip("'")
        except Exception:
            pass

    return ""

def save_api_key(key: str) -> None:
    """Saves or updates the OPENWEATHER_API_KEY in the local .env file."""
    cleaned_key = key.strip()
    lines = []
    found = False

    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("OPENWEATHER_API_KEY="):
                    lines.append(f"OPENWEATHER_API_KEY={cleaned_key}\n")
                    found = True
                else:
                    lines.append(line)

    if not found:
        lines.append(f"OPENWEATHER_API_KEY={cleaned_key}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

def detect_user_location() -> str:
    """
    Detects the user's current city based on IP address using free geolocation.
    Returns: city name or raises RuntimeError.
    """
    try:
        # Service 1: ip-api.com (Fast, free, reliable)
        res = requests.get("http://ip-api.com/json/?fields=city,country,status", timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == "success" and data.get("city"):
                return data["city"]
    except Exception:
        pass

    try:
        # Fallback Service 2: ipinfo.io
        res = requests.get("https://ipinfo.io/json", timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("city"):
                return data["city"]
    except Exception as e:
        raise RuntimeError(f"Could not auto-detect location: {e}")

    raise RuntimeError("Unable to detect city from your current IP address.")

def get_icon_path(icon_code: str) -> Optional[str]:
    """
    Downloads and caches OpenWeatherMap weather icon PNG.
    Returns the absolute path to the cached PNG file.
    """
    if not icon_code:
        return None

    icon_file = os.path.join(ICONS_DIR, f"{icon_code}.png")
    if os.path.exists(icon_file) and os.path.getsize(icon_file) > 0:
        return icon_file

    url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    try:
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            with open(icon_file, "wb") as f:
                f.write(res.content)
            return icon_file
    except Exception:
        pass

    return None

def fetch_weather_data(query: str, api_key: str) -> Dict:
    """
    Fetches real-time current weather and 5-day / 3-hour forecast from OpenWeatherMap.
    
    Returns structured data with both Metric (°C) and Imperial (°F) units.
    """
    cleaned_query = query.strip()
    if not cleaned_query:
        raise ValueError("City name or ZIP code cannot be empty.")

    if not api_key:
        raise ValueError("OpenWeatherMap API Key is missing. Please provide your API key.")

    # 1. Fetch Current Weather
    curr_url = "https://api.openweathermap.org/data/2.5/weather"
    params_curr = {
        "q": cleaned_query,
        "appid": api_key,
        "units": "metric"
    }

    try:
        res_curr = requests.get(curr_url, params=params_curr, timeout=10)
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network error while connecting to weather service:\n{e}")

    if res_curr.status_code == 401:
        raise PermissionError(
            "Invalid or unactivated API Key.\n\n"
            "If you recently created your OpenWeatherMap key, it typically takes 10 to 30 minutes "
            "for OpenWeatherMap servers to activate new free keys. Please try again shortly."
        )
    elif res_curr.status_code == 404:
        raise LookupError(f"Location '{cleaned_query}' not found. Please check spelling or try adding a country code (e.g. 'London, UK').")
    elif res_curr.status_code != 200:
        raise RuntimeError(f"Weather API returned status code {res_curr.status_code}: {res_curr.text}")

    curr_json = res_curr.json()

    # 2. Fetch 5-Day / 3-Hour Forecast
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    params_fore = {
        "q": cleaned_query,
        "appid": api_key,
        "units": "metric"
    }

    try:
        res_fore = requests.get(forecast_url, params=params_fore, timeout=10)
        fore_json = res_fore.json() if res_fore.status_code == 200 else {}
    except Exception:
        fore_json = {}

    # Parse Current Weather
    main_data = curr_json.get("main", {})
    weather_desc = curr_json.get("weather", [{}])[0]
    wind_data = curr_json.get("wind", {})
    sys_data = curr_json.get("sys", {})

    temp_c = float(main_data.get("temp", 0.0))
    feels_c = float(main_data.get("feels_like", 0.0))
    temp_f = (temp_c * 9 / 5) + 32
    feels_f = (feels_c * 9 / 5) + 32

    wind_ms = float(wind_data.get("speed", 0.0))
    wind_mph = wind_ms * 2.23694

    icon_code = weather_desc.get("icon", "01d")
    icon_path = get_icon_path(icon_code)

    current_parsed = {
        "city": curr_json.get("name", cleaned_query),
        "country": sys_data.get("country", ""),
        "temp_c": round(temp_c, 1),
        "temp_f": round(temp_f, 1),
        "feels_c": round(feels_c, 1),
        "feels_f": round(feels_f, 1),
        "humidity": int(main_data.get("humidity", 0)),
        "pressure": int(main_data.get("pressure", 0)),
        "wind_ms": round(wind_ms, 1),
        "wind_mph": round(wind_mph, 1),
        "condition": weather_desc.get("main", "Clear"),
        "description": weather_desc.get("description", "").title(),
        "icon_code": icon_code,
        "icon_path": icon_path,
        "timestamp": datetime.now().strftime("%A, %b %d • %I:%M %p")
    }

    # Parse Hourly Forecast (Next 6 items = next 18 hours in 3-hour intervals)
    hourly_list = []
    forecast_items = fore_json.get("list", [])
    
    for item in forecast_items[:6]:
        dt_txt = item.get("dt_txt", "")
        # Format time label (e.g. "3 PM" or "03:00 PM")
        try:
            dt_obj = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
            time_label = dt_obj.strftime("%I %p").lstrip("0")
        except Exception:
            time_label = dt_txt.split(" ")[-1][:5]

        h_main = item.get("main", {})
        h_weather = item.get("weather", [{}])[0]
        h_temp_c = float(h_main.get("temp", 0.0))
        h_temp_f = (h_temp_c * 9 / 5) + 32
        h_icon = h_weather.get("icon", "01d")

        hourly_list.append({
            "time": time_label,
            "temp_c": round(h_temp_c, 1),
            "temp_f": round(h_temp_f, 1),
            "condition": h_weather.get("main", ""),
            "icon_code": h_icon,
            "icon_path": get_icon_path(h_icon)
        })

    # Parse 5-Day Daily Forecast
    # Group entries by date
    daily_groups = defaultdict(list)
    today_str = datetime.now().strftime("%Y-%m-%d")

    for item in forecast_items:
        dt_txt = item.get("dt_txt", "")
        date_str = dt_txt.split(" ")[0]
        if date_str != today_str:
            daily_groups[date_str].append(item)

    daily_list = []
    # Take up to 5 days
    for date_str in sorted(daily_groups.keys())[:5]:
        entries = daily_groups[date_str]
        temps = [float(e.get("main", {}).get("temp", 0)) for e in entries]
        min_c = min(temps)
        max_c = max(temps)
        min_f = (min_c * 9 / 5) + 32
        max_f = (max_c * 9 / 5) + 32

        # Pick midday entry (around 12:00:00) for representative icon and description
        mid_entry = entries[len(entries) // 2]
        d_weather = mid_entry.get("weather", [{}])[0]
        d_icon = d_weather.get("icon", "01d")

        try:
            dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = dt_obj.strftime("%A")
            formatted_date = dt_obj.strftime("%b %d")
        except Exception:
            day_name = date_str
            formatted_date = date_str

        daily_list.append({
            "day_name": day_name,
            "date": formatted_date,
            "min_c": round(min_c, 1),
            "max_c": round(max_c, 1),
            "min_f": round(min_f, 1),
            "max_f": round(max_f, 1),
            "condition": d_weather.get("main", "Clear"),
            "description": d_weather.get("description", "").title(),
            "icon_code": d_icon,
            "icon_path": get_icon_path(d_icon)
        })

    return {
        "current": current_parsed,
        "hourly": hourly_list,
        "daily": daily_list
    }
