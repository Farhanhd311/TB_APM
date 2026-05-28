import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import time

# Import utilities
from utils.styles import get_custom_css
import utils.database as db
from utils.i18n import t, get_lang

st.set_page_config(
    page_title="Target Kalori — CaloriQ",
    page_icon="🎯",
    layout="wide",
)

# Apply CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)
lang = get_lang()

# Title
st.markdown(f'<div class="section-title">{t("target_title", lang)}</div><div class="section-sub">{t("target_subtitle", lang)}</div>', unsafe_allow_html=True)

col_target, col_progress = st.columns([1, 1.2])

today_str = date.today().isoformat()
current_target = db.get_target(today_str)
burned_today = db.get_today_total_calories()

with col_target:
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="form-section-title">🎯 {t("target_set", lang)}</div>', unsafe_allow_html=True)
        
        target_input = st.number_input(
            t("target_cal", lang), 
            min_value=100, 
            max_value=5000, 
            value=int(current_target) if current_target else 500,
            step=50
        )
        
        if st.button(t("target_save", lang), use_container_width=True):
            db.save_target(target_input, today_str)
            st.success(t("target_saved", lang))
            time.sleep(0.5)
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="form-section-title">{t("target_history", lang)}</div>', unsafe_allow_html=True)
        
        history = db.get_target_history(30)
        daily_burned = db.get_daily_calories(30)
        
        if history and daily_burned:
            df_hist = pd.DataFrame(history)
            df_burn = pd.DataFrame(daily_burned)
            
            # Merge
            df_merged = pd.merge(df_hist, df_burn, on="date", how="outer").fillna(0)
            df_merged = df_merged.sort_values("date")
            
            fig = px.bar(
                df_merged, x="date", y="total_cal",
                labels={"date": "Tanggal", "total_cal": "Kalori Terbakar"},
                color_discrete_sequence=["#00C9A7"]
            )
            # Add target line
            fig.add_scatter(
                x=df_merged["date"], y=df_merged["target_calories"],
                mode="lines", name="Target", line=dict(color="#FFD166", dash="dash")
            )
            
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#B0D8D8"),
                margin=dict(l=0, r=0, t=20, b=0),
                height=250,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada data riwayat yang cukup.")
        st.markdown('</div>', unsafe_allow_html=True)

with col_progress:
    st.markdown(f'<div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin-bottom:15px;">{t("target_progress", lang)}</div>', unsafe_allow_html=True)
    
    if current_target:
        percentage = min(100, int((burned_today / current_target) * 100))
        remaining = max(0, current_target - burned_today)
        
        st.markdown(f"""
<div class="progress-container">
<div style="display:flex; justify-content:space-between; align-items:flex-end;">
<div>
<div style="font-size:3rem; font-weight:800; color:#00C9A7; font-family:Outfit, sans-serif; line-height:1;">
{burned_today:.0f} <span style="font-size:1.5rem; font-weight:500; color:#7DCFBA;">kcal</span>
</div>
<div style="color:#B0D8D8; font-size:0.9rem; margin-top:4px;">
{t('target_burned', lang)} {t('target_of', lang)} {current_target} kcal
</div>
</div>
<div style="text-align:right;">
<div style="font-size:2rem; font-weight:800; color:#FFD166; font-family:Outfit, sans-serif; line-height:1;">
{percentage}%
</div>
</div>
</div>
<div class="progress-bar-bg">
<div class="progress-bar-fill" style="width: {percentage}%;"></div>
</div>
<div style="margin-top:16px; text-align:center; color:#7DCFBA;">
{f"{t('target_remaining', lang)}: <b>{remaining:.0f} kcal</b>" if remaining > 0 else f"<span style='color:#06D6A0;'>{t('target_achieved', lang)}</span>"}
</div>
</div>
""", unsafe_allow_html=True)
        
        if remaining == 0:
            st.balloons()
            
        # List of today's sessions
        st.markdown(f'<div style="font-size:1rem; font-weight:600; color:#FFFFFF; margin:20px 0 10px;">{t("target_today_sessions", lang)}</div>', unsafe_allow_html=True)
        today_sessions = db.get_today_predictions()
        if today_sessions:
            for s in today_sessions:
                st.markdown(f"""
                <div style="background:rgba(13,53,53,0.5); border:1px solid #1D5C5C; border-radius:10px; padding:12px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="color:#00C9A7; font-weight:600;">{s['timestamp'][11:16]}</span>
                        <span style="color:#B0D8D8; margin-left:12px;">{s['duration']} min • {s['intensity']}</span>
                    </div>
                    <div style="font-weight:700; color:#FFFFFF;">
                        +{s['calories']:.0f} kcal
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada sesi olahraga hari ini.")
            
    else:
        st.markdown(f"""
        <div class="empty-state">
            <div class="icon">🎯</div>
            <div class="text">{t("target_no_target", lang)}</div>
        </div>
        """, unsafe_allow_html=True)
