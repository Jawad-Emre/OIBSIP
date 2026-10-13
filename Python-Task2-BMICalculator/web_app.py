"""
BMI Health Tracker — Web Dashboard (Flask Application)
Oasis Infobyte SIP Task 2 (Advanced Web View)
Author: Jawad Ahmad
Features:
- REST API integration with SQLite persistence
- Multi-User Profile isolation with unique auto-incremented IDs
- Modern Responsive Web UI (Tailwind CSS + Chart.js)
- Precision WHO classification & dynamic feedback
"""

import os
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify
import database as db

app = Flask(__name__)

# Ensure database tables exist
db.init_db()

CATEGORY_DESCRIPTIONS = {
    "Underweight": "Your BMI is below the healthy range (< 18.5). Consider consulting a nutritionist for healthy calorie intake.",
    "Normal": "Your BMI is in the ideal healthy range (18.5 – 24.9). Great job maintaining a balanced lifestyle!",
    "Overweight": "Your BMI is slightly above the healthy range (25.0 – 29.9). Regular physical exercise and balanced nutrition can help.",
    "Obese": "Your BMI indicates obesity (≥ 30.0). It is advised to seek medical guidance and plan a comprehensive wellness routine."
}

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return weight_kg / (height_m ** 2)

def classify_bmi(bmi_val: float) -> str:
    if bmi_val < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_val < 25.0:
        return "Normal"
    elif 25.0 <= bmi_val < 30.0:
        return "Overweight"
    else:
        return "Obese"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        users = db.get_all_users()
        return jsonify(users)
    except db.DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400

    try:
        user_id, display = db.create_user(name)
        return jsonify({"id": user_id, "name": name, "display": display}), 201
    except (db.DatabaseError, ValueError) as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/records/<int:user_id>", methods=["GET"])
def get_records(user_id):
    try:
        records = db.get_user_records(user_id)
        # Format for table display
        for r in records:
            r["weight"] = f"{r['weight']:.1f}"
            r["height"] = f"{r['height']:.2f}"
            r["bmi"] = f"{r['bmi']:.2f}"
        return jsonify(records)
    except db.DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/records/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    try:
        db.delete_record(record_id)
        return jsonify({"success": True})
    except db.DatabaseError as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    weight = data.get("weight")
    height = data.get("height")
    height_unit = data.get("height_unit", "meters")

    if not user_id:
        return jsonify({"error": "User profile must be selected"}), 400

    try:
        weight_val = float(weight)
        height_val = float(height)
    except (TypeError, ValueError):
        return jsonify({"error": "Weight and height must be numeric"}), 400

    if weight_val <= 0 or height_val <= 0:
        return jsonify({"error": "Weight and height must be positive values"}), 400

    # Unit conversion
    if height_unit == "cm":
        height_m = height_val / 100.0
    else:
        height_m = height_val

    if height_m < 0.4 or height_m > 3.0:
        return jsonify({"error": "Please enter a realistic height (0.4m to 3.0m)"}), 400

    bmi = round(calculate_bmi(weight_val, height_m), 2)
    category = classify_bmi(bmi)
    description = CATEGORY_DESCRIPTIONS.get(category, "")

    try:
        rec_id = db.add_bmi_record(user_id, weight_val, round(height_m, 2), bmi, category)
        return jsonify({
            "record_id": rec_id,
            "weight": weight_val,
            "height_m": round(height_m, 2),
            "bmi": bmi,
            "category": category,
            "description": description
        })
    except db.DatabaseError as e:
        return jsonify({"error": str(e)}), 500

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 BMI Health Tracker Web Dashboard Starting...")
    print("🌐 Open URL: http://127.0.0.1:5000")
    print("=" * 60)
    # Open default browser automatically after 1 second
    Timer(1.2, open_browser).start()
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)
