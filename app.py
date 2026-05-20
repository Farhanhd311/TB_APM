import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from utils.styles import get_custom_css
from utils.predictor import load_model, get_feature_importances

st.set_page_config(
    page_title="CaloriQ — Prediksi Kalori Aktivitas Fisik",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

# ── Init session state ──
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 24px;'>
        <div style='font-size:2.5rem;'>🔥</div>
        <div style='font-family:Outfit,sans-serif; font-size:1.4rem; font-weight:700; color:#00C9A7;'>CaloriQ</div>
        <div style='font-size:0.75rem; color:#7DCFBA; margin-top:4px;'>AI Calorie Predictor</div>
    </div>
    <hr style='border-color:#1D5C5C; margin:0 0 16px;'>
    """, unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.75rem; color:#7DCFBA; padding:0 8px 8px; font-weight:600; text-transform:uppercase; letter-spacing:1px;'>Navigasi</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  HERO SECTION
# ══════════════════════════════════════════════
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🔥 CaloriQ</div>
    <div class="hero-subtitle">Prediksi Kalori Aktivitas Fisik dengan Kecerdasan Buatan</div>
    <div style='margin-top:14px;'>
        <span class="hero-badge">🌲 Random Forest</span>
        <span class="hero-badge">🎯 R² 99.99%</span>
        <span class="hero-badge">📊 15.000 Data</span>
        <span class="hero-badge">⚡ Real-time</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  METRIC CARDS
# ══════════════════════════════════════════════
st.markdown('<div class="section-title">📈 Performa Model</div><div class="section-sub">Statistik akurasi model Random Forest yang digunakan</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("🎯 Akurasi (R²)", "99.99%", "Test Score")
with c2:
    st.metric("📉 MAE", "~1.77 kcal", "Mean Abs. Error")
with c3:
    st.metric("🌲 Pohon Keputusan", "100 trees", "n_estimators")
with c4:
    sessions = len(st.session_state.prediction_history)
    st.metric("🔮 Prediksi Sesi Ini", f"{sessions}x", "Riwayat tersimpan")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  FEATURE IMPORTANCE CHART
# ══════════════════════════════════════════════
st.markdown('<div class="section-title">🔍 Feature Importance</div><div class="section-sub">Seberapa besar pengaruh tiap faktor terhadap prediksi kalori</div>', unsafe_allow_html=True)

col_fi, col_eval = st.columns([3, 2])

with col_fi:
    with st.spinner("Memuat model..."):
        fi = get_feature_importances()

    label_map = {
        "Duration":   "⏱ Durasi Olahraga",
        "Heart_Rate": "💓 Heart Rate",
        "Body_Temp":  "🌡 Suhu Tubuh",
        "Weight":     "⚖️ Berat Badan",
        "Age":        "🎂 Usia",
        "Height":     "📏 Tinggi Badan",
        "Gender":     "👤 Jenis Kelamin",
    }
    fi_labels = [label_map.get(f, f) for f in fi.index]
    colors = ["#00C9A7" if i == 0 else f"rgba(0,201,167,{0.7 - i*0.08})" for i in range(len(fi))]

    fig_fi = go.Figure(go.Bar(
        x=fi.values[::-1],
        y=fi_labels[::-1],
        orientation="h",
        marker=dict(color=colors[::-1], line=dict(width=0)),
        text=[f"{v:.3f}" for v in fi.values[::-1]],
        textposition="outside",
        textfont=dict(color="#B0D8D8", size=11),
    ))
    fig_fi.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B0D8D8", family="Inter"),
        xaxis=dict(showgrid=True, gridcolor="rgba(29,92,92,0.4)", color="#7DCFBA", zeroline=False),
        yaxis=dict(showgrid=False, color="#B0D8D8"),
        margin=dict(l=10, r=60, t=10, b=10),
        height=280,
    )
    st.plotly_chart(fig_fi, use_container_width=True)

with col_eval:
    st.markdown('<div style="color:#7DCFBA; font-size:0.85rem; font-weight:600; margin-bottom:10px;">📊 Grafik Evaluasi Model</div>', unsafe_allow_html=True)
    eval_img = os.path.join(os.path.dirname(__file__), "hasil_evaluasi", "evaluasi_model.png")
    if os.path.exists(eval_img):
        st.image(eval_img, use_container_width=True, caption="Evaluasi Model: Aktual vs Prediksi, Feature Importance, Residual")
    else:
        st.info("Grafik evaluasi tidak ditemukan. Jalankan `model_training.py` terlebih dahulu.")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  HOW TO USE
# ══════════════════════════════════════════════
st.markdown('<div class="section-title">🚀 Cara Penggunaan</div><div class="section-sub">3 langkah mudah untuk mendapatkan prediksi kalori Anda</div>', unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">01</div>
        <div class="step-icon">📝</div>
        <div class="step-title">Isi Data Aktivitas</div>
        <div class="step-desc">Masukkan jenis kelamin, usia, tinggi, berat badan, durasi olahraga, heart rate, dan suhu tubuh Anda.</div>
    </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">02</div>
        <div class="step-icon">🤖</div>
        <div class="step-title">AI Memproses Data</div>
        <div class="step-desc">Model Random Forest kami menganalisis 7 fitur input dan menghasilkan prediksi kalori yang akurat secara real-time.</div>
    </div>
    """, unsafe_allow_html=True)
with s3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">03</div>
        <div class="step-icon">📊</div>
        <div class="step-title">Dapatkan Insight</div>
        <div class="step-desc">Lihat kalori terbakar, kategori intensitas, aktivitas setara, saran personal, dan simpan riwayat Anda.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  CTA
# ══════════════════════════════════════════════
st.markdown("""
<div style='text-align:center; background:linear-gradient(135deg,rgba(0,201,167,0.1),rgba(13,53,53,0.8));
border:1px solid rgba(0,201,167,0.3); border-radius:20px; padding:36px;'>
    <div style='font-family:Outfit,sans-serif; font-size:1.6rem; font-weight:700; color:#FFFFFF; margin-bottom:8px;'>
        Siap Cek Kalori Anda? 🔥
    </div>
    <div style='color:#7DCFBA; margin-bottom:20px;'>Klik menu <b style="color:#00C9A7;">🔥 Prediksi</b> di sidebar untuk mulai.</div>
</div>
""", unsafe_allow_html=True)
