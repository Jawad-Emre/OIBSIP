"""
Database Management Module for BMI Calculator
Handles SQLite data persistence, user profiles with unique IDs, and historical health records.
"""

import sqlite3
import os
from typing import List, Dict, Optional, Tuple

DB_FILENAME = "bmi_records.db"

def get_db_path() -> str:
    """Returns absolute path to the SQLite database located in the script directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, DB_FILENAME)

class DatabaseError(Exception):
    """Custom exception class for database operations."""
    pass

def init_db() -> None:
    """Initializes the database tables if they do not exist."""
    try:
        with sqlite3.connect(get_db_path()) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            
            # Users table with auto-increment ID
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # BMI historical records table linked by user_id
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)
            conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to initialize database: {e}")

def create_user(name: str) -> Tuple[int, str]:
    """
    Creates a new user profile with a unique auto-incremented ID.
    Returns a tuple of (user_id, formatted_display_name).
    """
    cleaned_name = name.strip()
    if not cleaned_name:
        raise ValueError("User name cannot be empty.")

    try:
        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name) VALUES (?);", (cleaned_name,))
            conn.commit()
            user_id = cursor.lastrowid
            display_name = f"{cleaned_name} (ID: {user_id})"
            return user_id, display_name
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while creating user: {e}")

def get_all_users() -> List[Dict]:
    """
    Retrieves all registered users.
    Returns a list of dicts with keys: 'id', 'name', 'display'.
    """
    try:
        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM users ORDER BY id ASC;")
            rows = cursor.fetchall()
            return [{"id": row[0], "name": row[1], "display": f"{row[1]} (ID: {row[0]})"} for row in rows]
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while fetching users: {e}")

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Retrieves user details by their unique ID."""
    try:
        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, created_at FROM users WHERE id = ?;", (user_id,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "created_at": row[2], "display": f"{row[1]} (ID: {row[0]})"}
            return None
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while retrieving user {user_id}: {e}")

def add_bmi_record(user_id: int, weight: float, height: float, bmi: float, category: str) -> int:
    """
    Saves a new BMI calculation record for a given user.
    Returns the newly created record ID.
    """
    try:
        with sqlite3.connect(get_db_path()) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bmi_records (user_id, weight, height, bmi, category)
                VALUES (?, ?, ?, ?, ?);
            """, (user_id, weight, height, bmi, category))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while saving BMI record: {e}")

def get_user_records(user_id: int) -> List[Dict]:
    """
    Retrieves all BMI records for a specific user, sorted from earliest to latest.
    """
    try:
        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, weight, height, bmi, category, recorded_at
                FROM bmi_records
                WHERE user_id = ?
                ORDER BY datetime(recorded_at) ASC, id ASC;
            """, (user_id,))
            rows = cursor.fetchall()
            records = []
            for r in rows:
                records.append({
                    "id": r[0],
                    "weight": r[1],
                    "height": r[2],
                    "bmi": r[3],
                    "category": r[4],
                    "recorded_at": r[5]
                })
            return records
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while fetching records: {e}")

def delete_record(record_id: int) -> None:
    """Deletes a specific BMI record by its ID."""
    try:
        with sqlite3.connect(get_db_path()) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bmi_records WHERE id = ?;", (record_id,))
            conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Database error while deleting record: {e}")
