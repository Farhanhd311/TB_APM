import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta

from utils.styles import get_custom_css
import utils.database as db
from utils.i18n import t, get_lang
from utils.pdf_export import generate_pdf
from utils.auth import render_sidebar, is_logged_in

st.set_page_config(
    page_title="Riwayat & Statistik — CaloriQ",
    page_icon="📊",
    layout="wide",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_sidebar()
lang = get_lang()

# ── Page Header ──
st.markdown(
    '<div class="page-header">'
    '<div class="page-title">Riwayat & Statistik</div>'
    f'<div class="page-subtitle">{t("hist_subtitle", lang)}</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Guard Login ──
if not is_logged_in():
    st.warning(t("hist_login_required", lang))
    st.page_link("pages/9_🔐_Login.py", label="Masuk ke akun")
    st.stop()

# ── Filter Date ──
c_filt1, c_filt2, _ = st.columns([1, 1, 2])
with c_filt1:
    date_from = st.date_input(t("hist_from", lang), date.today() - timedelta(days=7))
with c_filt2:
    date_to = st.date_input(t("hist_to", lang), date.today())

history_data = db.get_predictions(date_from, date_to)

# ── Reminder Card ──
last_date_str = db.get_last_prediction_date()
if last_date_str:
    last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
    days_ago = (date.today() - last_date).days

    if days_ago == 0:
        reminder_text = f"Terakhir olahraga: <b>hari ini</b>"
        reminder_color = "#06D6A0"
    elif days_ago <= 2:
        reminder_text = f"Terakhir olahraga: <b>{days_ago} hari yang lalu</b>"
        reminder_color = "#FFD166"
    else:
        reminder_text = f"Terakhir olahraga: <b>{days_ago} hari yang lalu</b>. Waktunya mulai lagi!"
        reminder_color = "#EF476F"
else:
    reminder_text = "Belum ada data olahraga."
    reminder_color = "#00C9A7"

st.markdown(f"""
<div class="reminder-card" style="border-left-color: {reminder_color}; background: {reminder_color}0D;">
    <div style="font-weight: 600; color: #FFFFFF; font-size:0.9rem;">Pengingat Olahraga</div>
    <div style="color: #B0D8D8; font-size: 0.85rem; margin-top: 4px;">{reminder_text}</div>
</div>
""", unsafe_allow_html=True)

# ── Empty State ──
if not history_data:
    st.markdown(f"""
    <div class="empty-state">
        <div class="icon">📁</div>
        <div class="text">{t("hist_empty", lang)}<br>{t("hist_empty2", lang)}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    df_history = pd.DataFrame(history_data)

    # ── Summary Stats ──
    st.markdown(
        '<div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:12px;">Ringkasan Periode</div>',
        unsafe_allow_html=True
    )

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        total_cal = round(df_history["calories"].sum(), 1)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_cal}</div>
            <div class="stat-label">{t("hist_total_cal", lang)}</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        avg_cal = round(df_history["calories"].mean(), 1)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{avg_cal}</div>
            <div class="stat-label">{t("hist_avg_cal", lang)}</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        max_cal = df_history["calories"].max()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{max_cal}</div>
            <div class="stat-label">{t("hist_max_cal", lang)}</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        total_count = len(df_history)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_count}</div>
            <div class="stat-label">{t("hist_total_act", lang)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown(
            '<div style="color:#4D9E8F; font-size:0.82rem; font-weight:600; margin-bottom:8px;">Tren Kalori</div>',
            unsafe_allow_html=True
        )
        df_chart = df_history.iloc[::-1].reset_index(drop=True)
        fig_trend = px.line(
            df_chart,
            x=df_chart.index + 1,
            y="calories",
            markers=True,
            color_discrete_sequence=["#00C9A7"]
        )
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B0D8D8"),
            xaxis=dict(title=t("hist_order", lang), showgrid=False, color="#7DCFBA"),
            yaxis=dict(title="Kalori (kcal)", gridcolor="rgba(29,92,92,0.25)", color="#7DCFBA"),
            margin=dict(l=0, r=0, t=16, b=0),
            height=280
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_chart2:
        st.markdown(
            '<div style="color:#4D9E8F; font-size:0.82rem; font-weight:600; margin-bottom:8px;">Distribusi Intensitas</div>',
            unsafe_allow_html=True
        )
        intensity_counts = df_history["intensity"].value_counts().reset_index()
        intensity_counts.columns = ["Intensitas", "Jumlah"]
        color_map = {
            "Ringan": "#06D6A0", "Sedang": "#FFD166", "Tinggi": "#FF6B6B",
            "Light": "#06D6A0", "Medium": "#FFD166", "High": "#FF6B6B"
        }
        fig_pie = px.pie(
            intensity_counts,
            values="Jumlah",
            names="Intensitas",
            color="Intensitas",
            color_discrete_map=color_map,
            hole=0.45
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B0D8D8"),
            margin=dict(l=0, r=0, t=16, b=0),
            height=280,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── History Table ──
    st.markdown(
        '<div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:12px;">Detail Riwayat</div>',
        unsafe_allow_html=True
    )

    display_df = df_history[["timestamp", "gender", "age", "duration", "heart_rate", "calories", "intensity"]].copy()
    display_df.columns = ["Waktu", "Gender", "Usia", "Durasi (min)", "Heart Rate", "Kalori", "Intensitas"]

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # ── Actions ──
    st.markdown("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2, c_btn3, _ = st.columns([1, 1, 1, 1])

    with c_btn1:
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Unduh CSV",
            data=csv,
            file_name=f'caloriq_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
            mime='text/csv',
            use_container_width=True
        )

    with c_btn2:
        stats = {
            "total_count": total_count,
            "total_cal": total_cal,
            "avg_cal": avg_cal,
            "max_cal": max_cal,
            "min_cal": df_history["calories"].min()
        }
        pdf_bytes = generate_pdf(history_data, stats)
        if pdf_bytes:
            st.download_button(
                label="Unduh PDF",
                data=bytes(pdf_bytes),
                file_name=f'caloriq_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf',
                mime='application/pdf',
                use_container_width=True
            )

    with c_btn3:
        if st.button("Hapus Riwayat", use_container_width=True):
            db.delete_all_predictions()
            st.rerun()

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center; color:#2D7070; font-size:0.78rem;'>
    {t("hist_data_note", lang)}
</div>
""", unsafe_allow_html=True)
