import streamlit as st
from utils.predictor import calculate_bmi

from utils.styles import get_custom_css
import utils.database as db
from utils.i18n import t, get_lang
from utils.workout import get_workout_program, get_nutrition_tips
from utils.auth import render_sidebar

st.set_page_config(
    page_title="Program Olahraga — CaloriQ",
    page_icon="🏋️",
    layout="wide",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_sidebar()
lang = get_lang()

# ── Page Header ──
st.markdown(
    '<div class="page-header">'
    '<div class="page-title">Rekomendasi Program Olahraga</div>'
    f'<div class="page-subtitle">{t("prog_subtitle", lang)}</div>'
    '</div>',
    unsafe_allow_html=True
)

# Load profile
profile = db.get_profile() or {}
p_height = profile.get('height', 170.0)
p_weight = profile.get('weight', 70.0)
target = db.get_target() or 500

bmi_val, _, _ = calculate_bmi(p_height, p_weight)

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    level = st.selectbox(
        t("prog_level", lang),
        [t("prog_beginner", lang), t("prog_intermediate", lang), t("prog_advanced", lang)]
    )
    level_key = "beginner"
    if level == t("prog_intermediate", lang):
        level_key = "intermediate"
    elif level == t("prog_advanced", lang):
        level_key = "advanced"

with c2:
    st.markdown(f"""
    <div style="background:rgba(10,41,41,0.7); border:1px solid #1D5C5C; border-radius:10px; padding:14px; display:flex; justify-content:space-around; align-items:center;">
        <div style="text-align:center;">
            <div style="font-size:0.75rem; color:#4D9E8F; margin-bottom:2px;">BMI Anda</div>
            <div style="font-weight:700; color:#00C9A7; font-size:1.1rem;">{bmi_val}</div>
        </div>
        <div style="width:1px; height:28px; background:#1D5C5C;"></div>
        <div style="text-align:center;">
            <div style="font-size:0.75rem; color:#4D9E8F; margin-bottom:2px;">Target Harian</div>
            <div style="font-weight:700; color:#FFD166; font-size:1.1rem;">{target} kcal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

program = get_workout_program(bmi_val, target, level_key, lang)
tips = get_nutrition_tips(level_key, lang)

col_prog, col_tips = st.columns([2, 1])

with col_prog:
    st.markdown(
        '<div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:14px;">Jadwal Mingguan</div>',
        unsafe_allow_html=True
    )

    total_weekly_cal = 0
    for day in program:
        total_weekly_cal += day['est_cal']

        is_rest = day['duration'] == 0
        bg_color = "rgba(10,41,41,0.7)" if not is_rest else "rgba(255,255,255,0.03)"
        border_color = "#1D5C5C" if not is_rest else "#1A2A2A"
        cal_color = "#00C9A7" if not is_rest else "#444"

        st.markdown(f"""
        <div style="background:{bg_color}; border:1px solid {border_color}; border-radius:10px; padding:14px; margin-bottom:10px; display:flex; align-items:center;">
            <div style="width:90px; font-weight:700; color:#FFFFFF; font-size:0.9rem;">{day['day']}</div>
            <div style="flex-grow:1;">
                <div style="font-weight:600; color:#7DCFBA; font-size:0.9rem;">{day['exercise']}</div>
                <div style="font-size:0.8rem; color:#4D9E8F; margin-top:3px;">{day['tips']}</div>
            </div>
            <div style="text-align:right; min-width:80px;">
                <div style="font-weight:700; color:{cal_color}; font-size:0.9rem;">{day['est_cal']} kcal</div>
                <div style="font-size:0.78rem; color:#4D9E8F;">{day['duration']} menit</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:right; padding:8px; font-weight:600; color:#00C9A7; font-size:0.88rem;">
        Total estimasi minggu ini: {total_weekly_cal} kcal
    </div>
    """, unsafe_allow_html=True)

with col_tips:
    st.markdown(
        '<div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:14px;">Tips Nutrisi</div>',
        unsafe_allow_html=True
    )

    for tip in tips:
        st.markdown(f"""
        <div style="background:rgba(255,209,102,0.07); border-left:3px solid #FFD166; border-radius:0 10px 10px 0; padding:12px 14px; margin-bottom:10px; color:#D4C08A; font-size:0.85rem; line-height:1.5;">
            {tip}
        </div>
        """, unsafe_allow_html=True)
