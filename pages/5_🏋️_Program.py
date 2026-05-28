import streamlit as st

# Import utilities
from utils.styles import get_custom_css
import utils.database as db
from utils.i18n import t, get_lang
from utils.workout import get_workout_program, get_nutrition_tips

st.set_page_config(
    page_title="Program Olahraga — CaloriQ",
    page_icon="🏋️",
    layout="wide",
)

# Apply CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)
lang = get_lang()

# Title
st.markdown(f'<div class="section-title">{t("prog_title", lang)}</div><div class="section-sub">{t("prog_subtitle", lang)}</div>', unsafe_allow_html=True)

# Load profile
profile = db.get_profile() or {}
p_height = profile.get('height', 170.0)
p_weight = profile.get('weight', 70.0)
target = db.get_target() or 500

# Compute BMI
from utils.predictor import calculate_bmi
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
    <div style="background:rgba(13,53,53,0.5); border:1px solid #1D5C5C; border-radius:10px; padding:12px; height:74px; display:flex; justify-content:space-around; align-items:center;">
        <div style="text-align:center;">
            <div style="font-size:0.8rem; color:#7DCFBA;">{t("prog_bmi_label", lang)}</div>
            <div style="font-weight:700; color:#00C9A7;">{bmi_val}</div>
        </div>
        <div style="width:1px; height:30px; background:#1D5C5C;"></div>
        <div style="text-align:center;">
            <div style="font-size:0.8rem; color:#7DCFBA;">{t("prog_target_label", lang)}</div>
            <div style="font-weight:700; color:#FFD166;">{target} kcal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Generate Program
program = get_workout_program(bmi_val, target, level_key, lang)
tips = get_nutrition_tips(level_key, lang)

col_prog, col_tips = st.columns([2, 1])

with col_prog:
    st.markdown(f'<div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin-bottom:15px;">{t("prog_schedule", lang)}</div>', unsafe_allow_html=True)
    
    total_weekly_cal = 0
    for day in program:
        total_weekly_cal += day['est_cal']
        
        is_rest = day['duration'] == 0
        bg_color = "rgba(13,53,53,0.5)" if not is_rest else "rgba(255,255,255,0.05)"
        border_color = "#1D5C5C" if not is_rest else "#333333"
        cal_color = "#00C9A7" if not is_rest else "#777777"
        
        st.markdown(f"""
        <div style="background:{bg_color}; border:1px solid {border_color}; border-radius:12px; padding:16px; margin-bottom:12px; display:flex; align-items:center;">
            <div style="width:100px; font-weight:700; color:#FFFFFF;">{day['day']}</div>
            <div style="flex-grow:1;">
                <div style="font-weight:600; color:#7DCFBA;">{day['exercise']}</div>
                <div style="font-size:0.85rem; color:#B0D8D8; margin-top:4px;">💡 {day['tips']}</div>
            </div>
            <div style="text-align:right; min-width:80px;">
                <div style="font-weight:700; color:{cal_color};">{day['est_cal']} kcal</div>
                <div style="font-size:0.8rem; color:#7DCFBA;">{day['duration']} min</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"""
    <div style="text-align:right; padding:10px; font-weight:600; color:#00C9A7;">
        {t("prog_total_weekly", lang)}: {total_weekly_cal} kcal
    </div>
    """, unsafe_allow_html=True)

with col_tips:
    st.markdown(f'<div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin-bottom:15px;">{t("prog_nutrition", lang)}</div>', unsafe_allow_html=True)
    
    for tip in tips:
        st.markdown(f"""
        <div style="background:rgba(255,209,102,0.1); border-left:4px solid #FFD166; border-radius:0 12px 12px 0; padding:14px; margin-bottom:12px; color:#E8D5A3; font-size:0.95rem;">
            {tip}
        </div>
        """, unsafe_allow_html=True)
