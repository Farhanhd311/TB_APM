import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import time

# Import utilities
from utils.styles import get_custom_css
from utils.predictor import (
    predict_calories, 
    get_intensity, 
    get_equivalent_activity, 
    get_suggestions, 
    calculate_bmi
)

st.set_page_config(
    page_title="Prediksi Kalori — CaloriQ",
    page_icon="🔥",
    layout="wide",
)

# Apply CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Session State for history
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# Title
st.markdown('<div class="section-title">🔥 Prediksi Kalori Terbakar</div><div class="section-sub">Masukkan data aktivitas fisik Anda untuk mendapatkan prediksi akurat</div>', unsafe_allow_html=True)

# Form Layout
col_input, col_result = st.columns([1.2, 1])

with col_input:
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">👤 Data Personal</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            gender = st.radio("Jenis Kelamin", ["Male", "Female"], horizontal=True)
            gender_val = 1 if gender == "Male" else 0
            
            age = st.slider("Usia (Tahun)", 10, 80, 25)
        
        with c2:
            height = st.slider("Tinggi Badan (cm)", 140, 210, 170)
            weight = st.slider("Berat Badan (kg)", 30, 150, 70)
            
            # Real-time BMI Calculation
            bmi_val, bmi_cat, bmi_col = calculate_bmi(height, weight)
            st.markdown(f"""
                <div style='margin-top: 10px;'>
                    <span style='color:#7DCFBA; font-size:0.85rem;'>BMI Anda: </span>
                    <span style='color:#FFFFFF; font-weight:700;'>{bmi_val}</span>
                    <span class="bmi-pill" style='background:{bmi_col}22; color:{bmi_col}; border: 1px solid {bmi_col}44;'>{bmi_cat}</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">⏱️ Detail Aktivitas</div>', unsafe_allow_html=True)
        
        duration = st.slider("Durasi Olahraga (Menit)", 1, 60, 30)
        
        c3, c4 = st.columns(2)
        with c3:
            heart_rate = st.slider("Heart Rate (bpm)", 60, 200, 100)
        with c4:
            body_temp = st.slider("Suhu Tubuh (°C)", 36.0, 42.0, 37.5, step=0.1)
            
        st.markdown('</div>', unsafe_allow_html=True)

    predict_btn = st.button("🔥 Prediksi Sekarang", use_container_width=True)

with col_result:
    if predict_btn:
        with st.spinner("🤖 AI sedang menghitung..."):
            time.sleep(0.8) # Artificial delay for better UX
            
            # Get Prediction
            calories = predict_calories(gender_val, age, height, weight, duration, heart_rate, body_temp)
            intensity = get_intensity(calories)
            equivalent = get_equivalent_activity(calories)
            suggestions = get_suggestions(calories, duration, heart_rate, weight)
            
            # Save to history
            new_record = {
                "Waktu": datetime.now().strftime("%H:%M:%S"),
                "Gender": gender,
                "Usia": age,
                "Durasi": duration,
                "Heart Rate": heart_rate,
                "Kalori": calories,
                "Intensitas": intensity["label"]
            }
            st.session_state.prediction_history.append(new_record)
            
            # Display Results
            st.markdown(f"""
            <div class="result-card">
                <div style='color:#7DCFBA; font-size:0.9rem; font-weight:600; text-transform:uppercase; letter-spacing:1px;'>Estimasi Kalori Terbakar</div>
                <div style='font-size:4rem; font-weight:800; color:#00C9A7; font-family:Outfit, sans-serif; line-height:1;'>{calories} <span style='font-size:1.5rem; font-weight:500; color:#7DCFBA;'>kcal</span></div>
                <div class="intensity-badge" style='background:{intensity["color"]}22; color:{intensity["color"]}; border:1px solid {intensity["color"]}44;'>
                    {intensity["emoji"]} Intensitas {intensity["label"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = calories,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "#1D5C5C"},
                    'bar': {'color': intensity["bar_color"]},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#1D5C5C",
                    'steps': [
                        {'range': [0, 150], 'color': 'rgba(6, 214, 160, 0.1)'},
                        {'range': [150, 300], 'color': 'rgba(255, 209, 102, 0.1)'},
                        {'range': [300, 500], 'color': 'rgba(239, 71, 111, 0.1)'}
                    ],
                }
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "#B0D8D8", 'family': "Inter"},
                height=250,
                margin=dict(l=20, r=20, t=30, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Equivalent
            st.markdown(f'<div class="equivalent-box">{equivalent}</div>', unsafe_allow_html=True)
            
            # Suggestions
            st.markdown('<div style="margin-top:20px; font-weight:600; color:#FFFFFF;">💡 Saran Cerdas untuk Anda:</div>', unsafe_allow_html=True)
            for tip in suggestions:
                st.markdown(f'<div class="suggestion-box">{tip}</div>', unsafe_allow_html=True)
                
            st.success("✅ Hasil prediksi telah disimpan ke Riwayat!")
            
    else:
        # Empty State
        st.markdown("""
        <div class="empty-state">
            <div class="icon">👈</div>
            <div class="text">Silakan isi form di samping dan klik <br><b>"Prediksi Sekarang"</b> untuk melihat hasil.</div>
        </div>
        """, unsafe_allow_html=True)

# Footer info
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#5D8C8C; font-size:0.8rem;'>
    Model AI ini menggunakan algoritma <b>Random Forest Regressor</b> dengan akurasi 99.9%.<br>
    Tetap konsultasikan dengan profesional untuk program kesehatan yang lebih akurat.
</div>
""", unsafe_allow_html=True)
