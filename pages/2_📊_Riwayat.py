import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import utilities
from utils.styles import get_custom_css

st.set_page_config(
    page_title="Riwayat & Statistik — CaloriQ",
    page_icon="📊",
    layout="wide",
)

# Apply CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Session State for history
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# Title
st.markdown('<div class="section-title">📊 Riwayat & Statistik Sesi</div><div class="section-sub">Pantau progres dan analisis aktivitas fisik Anda selama sesi ini</div>', unsafe_allow_html=True)

# Check if history exists
if not st.session_state.prediction_history:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">📁</div>
        <div class="text">Belum ada riwayat prediksi.<br>Lakukan prediksi di halaman <b>"🔥 Prediksi"</b> terlebih dahulu.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Convert history to DataFrame
    df_history = pd.DataFrame(st.session_state.prediction_history)
    
    # ══════════════════════════════════════════════
    #  SUMMARY STATS
    # ══════════════════════════════════════════════
    st.markdown('<div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin-bottom:15px; display:flex; align-items:center; gap:8px;">📈 Ringkasan Sesi</div>', unsafe_allow_html=True)
    
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        total_cal = round(df_history["Kalori"].sum(), 1)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_cal}</div>
            <div class="stat-label">Total Kalori (kcal)</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        avg_cal = round(df_history["Kalori"].mean(), 1)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{avg_cal}</div>
            <div class="stat-label">Rata-rata / Sesi</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        max_cal = df_history["Kalori"].max()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{max_cal}</div>
            <div class="stat-label">Kalori Tertinggi</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        total_count = len(df_history)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_count}</div>
            <div class="stat-label">Total Aktivitas</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    #  CHARTS SECTION
    # ══════════════════════════════════════════════
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div style="color:#7DCFBA; font-size:0.85rem; font-weight:600; margin-bottom:10px;">📉 Tren Kalori Sesi Ini</div>', unsafe_allow_html=True)
        fig_trend = px.line(
            df_history, 
            x=df_history.index + 1, 
            y="Kalori", 
            markers=True,
            color_discrete_sequence=["#00C9A7"]
        )
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B0D8D8"),
            xaxis=dict(title="Urutan Prediksi", showgrid=False, color="#7DCFBA"),
            yaxis=dict(title="Kalori (kcal)", gridcolor="rgba(29,92,92,0.3)", color="#7DCFBA"),
            margin=dict(l=0, r=0, t=20, b=0),
            height=300
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_chart2:
        st.markdown('<div style="color:#7DCFBA; font-size:0.85rem; font-weight:600; margin-bottom:10px;">📊 Distribusi Intensitas</div>', unsafe_allow_html=True)
        intensity_counts = df_history["Intensitas"].value_counts().reset_index()
        intensity_counts.columns = ["Intensitas", "Jumlah"]
        
        # Color mapping for consistency
        color_map = {"Ringan": "#06D6A0", "Sedang": "#FFD166", "Tinggi": "#FF6B6B"}
        
        fig_pie = px.pie(
            intensity_counts, 
            values="Jumlah", 
            names="Intensitas",
            color="Intensitas",
            color_discrete_map=color_map,
            hole=0.4
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B0D8D8"),
            margin=dict(l=0, r=0, t=20, b=0),
            height=300,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    #  HISTORY TABLE
    # ══════════════════════════════════════════════
    st.markdown('<div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin-bottom:15px; display:flex; align-items:center; gap:8px;">📋 Tabel Detail Riwayat</div>', unsafe_allow_html=True)
    
    # Custom styling for the table display
    styled_df = df_history.copy()
    
    # Show the table
    st.dataframe(
        styled_df, 
        use_container_width=True,
        hide_index=True,
    )
    
    # ══════════════════════════════════════════════
    #  EXPORT & ACTIONS
    # ══════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2, _ = st.columns([1, 1, 2])
    
    with c_btn1:
        csv = df_history.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f'caloriq_history_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
            mime='text/csv',
            use_container_width=True
        )
        
    with c_btn2:
        if st.button("🗑️ Hapus Riwayat", use_container_width=True):
            st.session_state.prediction_history = []
            st.rerun()

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#5D8C8C; font-size:0.8rem;'>
    Data riwayat hanya tersimpan selama sesi browser ini berlangsung.<br>
    Refresh halaman atau tutup browser akan menghapus riwayat sementara.
</div>
""", unsafe_allow_html=True)
