import os
import joblib
import pandas as pd
import numpy as np
import streamlit as st


MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "random_forest_model.pkl")

FEATURES = ["Gender", "Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp"]


@st.cache_resource(show_spinner=False)
def load_model():
    """Load and cache the trained Random Forest model."""
    return joblib.load(MODEL_PATH)


def predict_calories(gender: int, age: int, height: float, weight: float,
                     duration: int, heart_rate: int, body_temp: float) -> float:
    """Run prediction with the loaded model. Returns calories (float)."""
    model = load_model()
    data = pd.DataFrame([[gender, age, height, weight, duration, heart_rate, body_temp]],
                        columns=FEATURES)
    return float(round(model.predict(data)[0], 2))


def get_feature_importances() -> pd.Series:
    """Return feature importance from the trained model."""
    model = load_model()
    return pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)


def get_intensity(calories: float) -> dict:
    """Return intensity category info based on calorie value."""
    if calories < 150:
        return {"label": "Ringan", "color": "#06D6A0", "emoji": "🟢", "bar_color": "#06D6A0"}
    elif calories < 300:
        return {"label": "Sedang", "color": "#FFD166", "emoji": "🟡", "bar_color": "#FFD166"}
    else:
        return {"label": "Tinggi", "color": "#FF6B6B", "emoji": "🔴", "bar_color": "#FF6B6B"}


def get_equivalent_activity(calories: float) -> str:
    """Return a human-readable activity equivalent for the calorie value."""
    if calories < 50:
        return "≈ Berdiri & bergerak ringan selama 30 menit"
    elif calories < 100:
        return "≈ Berjalan santai selama 25 menit"
    elif calories < 150:
        return "≈ Berjalan cepat selama 30 menit"
    elif calories < 200:
        return "≈ Bersepeda santai selama 30 menit"
    elif calories < 250:
        return "≈ Jogging ringan selama 25 menit"
    elif calories < 300:
        return "≈ Berenang gaya bebas selama 20 menit"
    elif calories < 400:
        return "≈ Lari 7 km/jam selama 30 menit"
    elif calories < 500:
        return "≈ Lari cepat 10 km/jam selama 30 menit"
    else:
        return "≈ Sprint intensitas tinggi selama 40 menit"


def get_suggestions(calories: float, duration: int, heart_rate: int, weight: float) -> list:
    """Generate smart, personalized suggestions."""
    tips = []
    if duration < 20:
        extra = round(calories * (10 / duration), 1) if duration > 0 else 30
        tips.append(f"⏱️ Tambah durasi **10 menit** untuk membakar sekitar **{extra} kcal** lebih banyak.")
    if heart_rate < 100:
        tips.append("💓 Heart rate masih rendah. Tingkatkan intensitas olahraga untuk hasil lebih optimal.")
    if calories < 100:
        tips.append("🔥 Coba olahraga dengan intensitas lebih tinggi seperti jogging atau HIIT.")
    if calories >= 300:
        tips.append("🏆 Luar biasa! Intensitas Anda sangat tinggi. Jangan lupa istirahat cukup dan hidrasi.")
    bmi = weight / ((170 / 100) ** 2)  # rough estimate
    if bmi > 25:
        tips.append("⚖️ Konsistensi adalah kunci! Olahraga rutin 3-5x seminggu membantu turunkan berat badan.")
    if not tips:
        tips.append("✅ Aktivitas Anda sudah bagus! Pertahankan konsistensi untuk hasil terbaik.")
    return tips


def calculate_bmi(height_cm: float, weight_kg: float) -> tuple:
    """Return (bmi_value, category, color)."""
    if height_cm <= 0:
        return 0, "—", "#B0D8D8"
    h_m = height_cm / 100
    bmi = weight_kg / (h_m ** 2)
    if bmi < 18.5:
        return round(bmi, 1), "Kurus", "#7EB8FF"
    elif bmi < 25:
        return round(bmi, 1), "Normal", "#06D6A0"
    elif bmi < 30:
        return round(bmi, 1), "Berlebih", "#FFD166"
    else:
        return round(bmi, 1), "Obesitas", "#FF6B6B"
