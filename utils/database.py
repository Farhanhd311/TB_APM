import os
import hashlib
from datetime import datetime, date, timedelta

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "caloriq_db")
DB_PORT = os.getenv("DB_PORT", "3306")


def _resolve_user_id(user_id=None):
    if user_id is not None:
        return user_id
    try:
        import streamlit as st
        user = st.session_state.get("user")
        if user:
            return user.get("id")
    except Exception:
        pass
    return None


def _hash_password(password: str) -> str:
    return hashlib.sha256((password or "").encode("utf-8")).hexdigest()


def get_connection(use_database=True):
    try:
        conn_params = {"host": DB_HOST, "user": DB_USER, "password": DB_PASSWORD, "port": DB_PORT}
        if use_database:
            conn_params["database"] = DB_NAME
        return mysql.connector.connect(**conn_params)
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def init_db():
    conn = get_connection(use_database=False)
    if not conn:
        return
    try:
        c = conn.cursor()
        c.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if conn.is_connected():
            c.close()
            conn.close()

    conn = get_connection()
    if not conn:
        return
    try:
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(64) NOT NULL,
                created_at DATETIME NOT NULL
            )"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NULL,
                timestamp DATETIME NOT NULL,
                date DATE NOT NULL,
                gender VARCHAR(10),
                gender_val INT,
                age INT,
                height FLOAT,
                weight FLOAT,
                duration INT,
                heart_rate INT,
                body_temp FLOAT,
                calories FLOAT,
                intensity VARCHAR(50),
                bmi FLOAT,
                bmi_category VARCHAR(50),
                INDEX idx_predictions_user_id (user_id)
            )"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS user_profile (
                id INT PRIMARY KEY,
                user_id INT NULL UNIQUE,
                name VARCHAR(100) DEFAULT '',
                gender VARCHAR(10) DEFAULT 'Male',
                age INT DEFAULT 25,
                height FLOAT DEFAULT 170,
                weight FLOAT DEFAULT 70,
                language VARCHAR(10) DEFAULT 'id',
                created_at DATETIME,
                updated_at DATETIME
            )"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS daily_targets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NULL,
                date DATE NOT NULL,
                target_calories FLOAT NOT NULL,
                UNIQUE KEY uq_daily_targets_user_date (user_id, date)
            )"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS badges_earned (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NULL,
                badge_id VARCHAR(50) NOT NULL,
                earned_at DATETIME NOT NULL,
                UNIQUE KEY uq_badges_user_badge (user_id, badge_id)
            )"""
        )

        # Minimal migration for old schema
        c.execute("SHOW COLUMNS FROM predictions LIKE 'user_id'")
        if not c.fetchone():
            c.execute("ALTER TABLE predictions ADD COLUMN user_id INT NULL AFTER id")
        c.execute("SHOW COLUMNS FROM user_profile LIKE 'user_id'")
        if not c.fetchone():
            c.execute("ALTER TABLE user_profile ADD COLUMN user_id INT NULL UNIQUE AFTER id")
        c.execute("SHOW COLUMNS FROM daily_targets LIKE 'user_id'")
        if not c.fetchone():
            c.execute("ALTER TABLE daily_targets ADD COLUMN user_id INT NULL AFTER id")
        c.execute("SHOW COLUMNS FROM badges_earned LIKE 'user_id'")
        if not c.fetchone():
            c.execute("ALTER TABLE badges_earned ADD COLUMN user_id INT NULL AFTER id")

        conn.commit()
    except Error as e:
        print(f"Error initializing tables: {e}")
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def create_user(username: str, password: str):
    username = (username or "").strip()
    if len(username) < 3:
        return False, "Username minimal 3 karakter."
    if len(password or "") < 6:
        return False, "Password minimal 6 karakter."
    conn = get_connection()
    if not conn:
        return False, "Koneksi database gagal."
    try:
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (%s, %s, %s)",
            (username, _hash_password(password), now),
        )
        user_id = c.lastrowid
        c.execute(
            """INSERT INTO user_profile
               (id, user_id, name, gender, age, height, weight, language, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (user_id, user_id, username, "Male", 25, 170, 70, "id", now, now),
        )
        conn.commit()
        return True, "Registrasi berhasil. Silakan login."
    except Error as e:
        if "Duplicate entry" in str(e):
            return False, "Username sudah digunakan."
        return False, "Gagal membuat akun."
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def authenticate_user(username: str, password: str):
    conn = get_connection()
    if not conn:
        return None
    try:
        c = conn.cursor(dictionary=True)
        c.execute(
            "SELECT id, username FROM users WHERE username = %s AND password_hash = %s LIMIT 1",
            ((username or "").strip(), _hash_password(password)),
        )
        return c.fetchone()
    except Error:
        return None
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def save_prediction(data: dict, user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return False
    conn = get_connection()
    if not conn:
        return False
    try:
        c = conn.cursor()
        c.execute(
            """INSERT INTO predictions
               (user_id, timestamp, date, gender, gender_val, age, height, weight,
                duration, heart_rate, body_temp, calories, intensity, bmi, bmi_category)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                user_id,
                data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                data.get("date", date.today().isoformat()),
                data.get("gender", ""),
                data.get("gender_val", 0),
                data.get("age", 0),
                data.get("height", 0),
                data.get("weight", 0),
                data.get("duration", 0),
                data.get("heart_rate", 0),
                data.get("body_temp", 0),
                data.get("calories", 0),
                data.get("intensity", ""),
                data.get("bmi", 0),
                data.get("bmi_category", ""),
            ),
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Error saving prediction: {e}")
        return False
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def get_predictions(date_from=None, date_to=None, user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return []
    conn = get_connection()
    if not conn:
        return []
    rows = []
    try:
        c = conn.cursor(dictionary=True)
        if date_from and date_to:
            c.execute(
                "SELECT * FROM predictions WHERE user_id = %s AND date BETWEEN %s AND %s ORDER BY timestamp DESC",
                (user_id, str(date_from), str(date_to)),
            )
        else:
            c.execute("SELECT * FROM predictions WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
        for r in c.fetchall():
            if isinstance(r.get("timestamp"), datetime):
                r["timestamp"] = r["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(r.get("date"), date):
                r["date"] = r["date"].isoformat()
            rows.append(r)
    except Error as e:
        print(f"Error getting predictions: {e}")
    finally:
        if conn.is_connected():
            c.close()
            conn.close()
    return rows


def get_today_predictions(user_id=None):
    today = date.today().isoformat()
    return get_predictions(today, today, user_id=user_id)


def get_today_total_calories(user_id=None):
    return sum(r["calories"] for r in get_today_predictions(user_id=user_id))


def get_all_predictions(user_id=None):
    return get_predictions(user_id=user_id)


def get_prediction_count(user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return 0
    conn = get_connection()
    if not conn:
        return 0
    try:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM predictions WHERE user_id = %s", (user_id,))
        row = c.fetchone()
        return row[0] if row else 0
    except Error:
        return 0
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def delete_all_predictions(user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return
    conn = get_connection()
    if not conn:
        return
    try:
        c = conn.cursor()
        c.execute("DELETE FROM predictions WHERE user_id = %s", (user_id,))
        conn.commit()
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def get_total_calories(user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return 0
    conn = get_connection()
    if not conn:
        return 0
    try:
        c = conn.cursor()
        c.execute("SELECT COALESCE(SUM(calories), 0) FROM predictions WHERE user_id = %s", (user_id,))
        row = c.fetchone()
        return row[0] if row else 0
    except Error:
        return 0
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def get_max_calories_single(user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return 0
    conn = get_connection()
    if not conn:
        return 0
    try:
        c = conn.cursor()
        c.execute("SELECT COALESCE(MAX(calories), 0) FROM predictions WHERE user_id = %s", (user_id,))
        row = c.fetchone()
        return row[0] if row else 0
    except Error:
        return 0
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def get_daily_calories(days=30, user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return []
    conn = get_connection()
    if not conn:
        return []
    rows = []
    try:
        c = conn.cursor(dictionary=True)
        start_date = (date.today() - timedelta(days=days)).isoformat()
        c.execute(
            """SELECT date, SUM(calories) as total_cal, COUNT(*) as sessions
               FROM predictions WHERE user_id = %s AND date >= %s
               GROUP BY date ORDER BY date""",
            (user_id, start_date),
        )
        for r in c.fetchall():
            if isinstance(r.get("date"), date):
                r["date"] = r["date"].isoformat()
            rows.append(r)
    except Error:
        pass
    finally:
        if conn.is_connected():
            c.close()
            conn.close()
    return rows


def _format_profile_row(row):
    if not row:
        return None
    if isinstance(row.get("created_at"), datetime):
        row["created_at"] = row["created_at"].strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(row.get("updated_at"), datetime):
        row["updated_at"] = row["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
    return row


def _link_legacy_profile(c, user_id):
    """Attach old singleton profile rows (user_id NULL) to the logged-in user."""
    c.execute(
        "SELECT id FROM user_profile WHERE user_id IS NULL ORDER BY updated_at DESC, id ASC LIMIT 1"
    )
    legacy = c.fetchone()
    if not legacy:
        return False
    legacy_id = legacy[0]
    c.execute(
        "UPDATE user_profile SET user_id = %s WHERE id = %s AND user_id IS NULL",
        (user_id, legacy_id),
    )
    return c.rowcount > 0


def save_profile(name, gender, age, height, weight, language, user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return False
    conn = get_connection()
    if not conn:
        return False
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c = conn.cursor()
        c.execute("SELECT id FROM user_profile WHERE user_id = %s LIMIT 1", (user_id,))
        existing = c.fetchone()

        if existing:
            c.execute(
                """UPDATE user_profile
                   SET name=%s, gender=%s, age=%s, height=%s, weight=%s, language=%s, updated_at=%s
                   WHERE user_id=%s""",
                (name, gender, age, height, weight, language, now, user_id),
            )
        else:
            c.execute("SELECT id FROM user_profile WHERE id = %s LIMIT 1", (user_id,))
            legacy = c.fetchone()
            if legacy:
                c.execute(
                    """UPDATE user_profile
                       SET user_id=%s, name=%s, gender=%s, age=%s, height=%s, weight=%s,
                           language=%s, updated_at=%s
                       WHERE id=%s""",
                    (user_id, name, gender, age, height, weight, language, now, user_id),
                )
            else:
                _link_legacy_profile(c, user_id)
                c.execute("SELECT id FROM user_profile WHERE user_id = %s LIMIT 1", (user_id,))
                if c.fetchone():
                    c.execute(
                        """UPDATE user_profile
                           SET name=%s, gender=%s, age=%s, height=%s, weight=%s,
                               language=%s, updated_at=%s
                           WHERE user_id=%s""",
                        (name, gender, age, height, weight, language, now, user_id),
                    )
                else:
                    c.execute(
                        """INSERT INTO user_profile
                           (id, user_id, name, gender, age, height, weight, language, created_at, updated_at)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (user_id, user_id, name, gender, age, height, weight, language, now, now),
                    )
        conn.commit()
        return True
    except Error as e:
        print(f"Error saving profile: {e}")
        return False
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def get_profile(user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return None
    conn = get_connection()
    if not conn:
        return None
    try:
        c = conn.cursor(dictionary=True)
        c.execute("SELECT * FROM user_profile WHERE user_id = %s LIMIT 1", (user_id,))
        row = c.fetchone()

        if not row:
            c.execute("SELECT * FROM user_profile WHERE id = %s LIMIT 1", (user_id,))
            row = c.fetchone()
            if row and row.get("user_id") is None:
                c.execute(
                    "UPDATE user_profile SET user_id = %s WHERE id = %s AND user_id IS NULL",
                    (user_id, user_id),
                )
                conn.commit()
                row["user_id"] = user_id
            elif not row:
                _link_legacy_profile(c, user_id)
                conn.commit()
                c.execute("SELECT * FROM user_profile WHERE user_id = %s LIMIT 1", (user_id,))
                row = c.fetchone()

        return _format_profile_row(row)
    except Error as e:
        print(f"Error getting profile: {e}")
        return None
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def save_target(target_calories: float, target_date: str = None, user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return False
    target_date = target_date or date.today().isoformat()
    conn = get_connection()
    if not conn:
        return False
    try:
        c = conn.cursor()
        c.execute(
            """INSERT INTO daily_targets (user_id, date, target_calories)
               VALUES (%s, %s, %s)
               ON DUPLICATE KEY UPDATE target_calories=%s""",
            (user_id, target_date, target_calories, target_calories),
        )
        conn.commit()
        return True
    except Error:
        return False
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def get_target(target_date: str = None, user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return None
    target_date = target_date or date.today().isoformat()
    conn = get_connection()
    if not conn:
        return None
    try:
        c = conn.cursor()
        c.execute("SELECT target_calories FROM daily_targets WHERE user_id = %s AND date = %s", (user_id, target_date))
        row = c.fetchone()
        return row[0] if row else None
    except Error:
        return None
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def get_target_history(days=30, user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return []
    conn = get_connection()
    if not conn:
        return []
    rows = []
    try:
        c = conn.cursor(dictionary=True)
        start_date = (date.today() - timedelta(days=days)).isoformat()
        c.execute(
            "SELECT date, target_calories FROM daily_targets WHERE user_id = %s AND date >= %s ORDER BY date",
            (user_id, start_date),
        )
        for r in c.fetchall():
            if isinstance(r.get("date"), date):
                r["date"] = r["date"].isoformat()
            rows.append(r)
    except Error:
        pass
    finally:
        if conn.is_connected():
            c.close()
            conn.close()
    return rows


def save_badge(badge_id: str, user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return False
    conn = get_connection()
    if not conn:
        return False
    try:
        c = conn.cursor()
        c.execute(
            "INSERT IGNORE INTO badges_earned (user_id, badge_id, earned_at) VALUES (%s, %s, %s)",
            (user_id, badge_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        return True
    except Error:
        return False
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def get_earned_badges(user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return []
    conn = get_connection()
    if not conn:
        return []
    rows = []
    try:
        c = conn.cursor(dictionary=True)
        c.execute("SELECT badge_id, earned_at FROM badges_earned WHERE user_id = %s ORDER BY earned_at", (user_id,))
        for r in c.fetchall():
            if isinstance(r.get("earned_at"), datetime):
                r["earned_at"] = r["earned_at"].strftime("%Y-%m-%d %H:%M:%S")
            rows.append(r)
    except Error:
        pass
    finally:
        if conn.is_connected():
            c.close()
            conn.close()
    return rows


def get_unique_active_days(user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return []
    conn = get_connection()
    if not conn:
        return []
    rows = []
    try:
        c = conn.cursor()
        c.execute("SELECT DISTINCT date FROM predictions WHERE user_id = %s ORDER BY date", (user_id,))
        for r in c.fetchall():
            d = r[0]
            rows.append(d.isoformat() if isinstance(d, date) else str(d))
    except Error:
        pass
    finally:
        if conn.is_connected():
            c.close()
            conn.close()
    return rows


def get_streak(user_id=None):
    days = get_unique_active_days(user_id=user_id)
    if not days:
        return 0
    streak = 0
    cursor_day = date.today()
    day_set = set(days)
    while cursor_day.isoformat() in day_set:
        streak += 1
        cursor_day -= timedelta(days=1)
    return streak


def get_last_prediction_date(user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return None
    conn = get_connection()
    if not conn:
        return None
    try:
        c = conn.cursor()
        c.execute("SELECT date FROM predictions WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1", (user_id,))
        row = c.fetchone()
        if not row:
            return None
        return row[0].isoformat() if isinstance(row[0], date) else str(row[0])
    except Error:
        return None
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


def reset_all_data(user_id=None):
    user_id = _resolve_user_id(user_id)
    if not user_id:
        return
    conn = get_connection()
    if not conn:
        return
    try:
        c = conn.cursor()
        c.execute("DELETE FROM predictions WHERE user_id = %s", (user_id,))
        c.execute("DELETE FROM user_profile WHERE user_id = %s", (user_id,))
        c.execute("DELETE FROM daily_targets WHERE user_id = %s", (user_id,))
        c.execute("DELETE FROM badges_earned WHERE user_id = %s", (user_id,))
        conn.commit()
    except Error as e:
        print(f"Error resetting data: {e}")
    finally:
        if conn.is_connected():
            c.close()
            conn.close()


init_db()
