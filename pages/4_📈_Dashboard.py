import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

from utils.styles import get_custom_css
import utils.database as db
from utils.i18n import t, get_lang
from utils.auth import render_sidebar, is_logged_in

st.set_page_config(
    page_title="Dashboard Analitik — CaloriQ",
    page_icon="📈",
    layout="wide",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_sidebar()
lang = get_lang()

# ── Page Header ──
st.markdown(
    '<div class="page-header">'
    '<div class="page-title">Dashboard Analitik</div>'
    f'<div class="page-subtitle">{t("dash_subtitle", lang)}</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Guard Login ──
if not is_logged_in():
    st.warning("Masuk terlebih dahulu untuk melihat dashboard analitik.")
    st.page_link("pages/9_🔐_Login.py", label="Masuk ke akun")
    st.stop()

# Load data
df_daily = pd.DataFrame(db.get_daily_calories(30))
all_preds = db.get_all_predictions()

if df_daily.empty or not all_preds:
    st.markdown(f"""
    <div class="empty-state">
        <div class="icon">📈</div>
        <div class="text">{t("dash_no_data", lang)}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # ── Top Stats ──
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{df_daily['total_cal'].max():.0f}</div>
            <div class="stat-label">Hari Terbaik (kcal)</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{df_daily['total_cal'].mean():.0f}</div>
            <div class="stat-label">Rata-rata Harian (kcal)</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{db.get_streak()}</div>
            <div class="stat-label">Streak Aktif (hari)</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(all_preds)}</div>
            <div class="stat-label">Total Sesi</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown(
            '<div style="color:#4D9E8F; font-size:0.82rem; font-weight:600; margin-bottom:8px;">Tren 30 Hari Terakhir</div>',
            unsafe_allow_html=True
        )
        fig_trend = px.area(
            df_daily, x="date", y="total_cal",
            labels={"date": t("dash_date", lang), "total_cal": t("dash_cal_per_day", lang)},
            color_discrete_sequence=["#00C9A7"]
        )
        fig_trend.update_traces(fillcolor="rgba(0,201,167,0.15)", line=dict(width=2.5))
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B0D8D8"),
            xaxis=dict(showgrid=False, color="#7DCFBA"),
            yaxis=dict(gridcolor="rgba(29,92,92,0.25)", color="#7DCFBA"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=280
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with c2:
        st.markdown(
            '<div style="color:#4D9E8F; font-size:0.82rem; font-weight:600; margin-bottom:8px;">Aktivitas 7 Hari</div>',
            unsafe_allow_html=True
        )
        fig_heat = px.bar(
            df_daily.tail(7), x="date", y="total_cal",
            color="total_cal", color_continuous_scale="Teal",
            labels={"date": "Tanggal", "total_cal": "Kalori"}
        )
        fig_heat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B0D8D8"),
            xaxis=dict(showgrid=False, color="#7DCFBA"),
            yaxis=dict(showgrid=False, visible=False),
            coloraxis_showscale=False,
            margin=dict(l=0, r=0, t=10, b=0),
            height=280
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Session Comparison ──
    st.markdown(
        '<div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:12px;">Perbandingan Sesi</div>',
        unsafe_allow_html=True
    )

    if len(all_preds) >= 2:
        options = {f"{p['timestamp']} — {p['calories']:.0f} kcal": p for p in all_preds}

        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            sel_a = st.selectbox("Sesi A", list(options.keys()), index=0)
        with col_sel2:
            sel_b = st.selectbox("Sesi B", list(options.keys()), index=1)

        data_a = options[sel_a]
        data_b = options[sel_b]

        categories = ['Durasi (min)', 'Heart Rate', 'Suhu Tubuh', 'Kalori (scaled)']
        cal_scale = 0.5

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[data_a['duration'], data_a['heart_rate'], data_a['body_temp'], data_a['calories'] * cal_scale],
            theta=categories,
            fill='toself',
            name="Sesi A",
            line_color="#00C9A7"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[data_b['duration'], data_b['heart_rate'], data_b['body_temp'], data_b['calories'] * cal_scale],
            theta=categories,
            fill='toself',
            name="Sesi B",
            line_color="#FFD166"
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(200, data_a['calories'] * cal_scale, data_b['calories'] * cal_scale)]),
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B0D8D8"),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, t=20, b=20),
            height=380
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    else:
        st.info("Butuh minimal 2 sesi untuk melakukan perbandingan.")
