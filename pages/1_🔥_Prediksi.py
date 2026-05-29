import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, date
import time

from utils.styles import get_custom_css
from utils.predictor import (
    predict_calories,
    get_intensity,
    get_equivalent_activity,
    get_suggestions,
    calculate_bmi
)
import utils.database as db
from utils.i18n import t, get_lang
from utils.hydration import calculate_hydration
from utils.food_equiv import get_food_equivalents, get_burn_time_for_food
from utils.badges import check_badges
from utils.auth import render_sidebar, is_logged_in

st.set_page_config(
    page_title="Prediksi Kalori — CaloriQ",
    page_icon="🔥",
    layout="wide",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_sidebar()
lang = get_lang()

# ── Page Header ──
st.markdown(
    '<div class="page-header">'
    f'<div class="page-title">Prediksi Kalori Terbakar</div>'
    f'<div class="page-subtitle">{t("pred_subtitle", lang)}</div>'
    '</div>',
    unsafe_allow_html=True
)

col_input, col_result = st.columns([1.2, 1])

# Load profile for auto-fill
profile = db.get_profile() if is_logged_in() else {}
p_gender = profile.get("gender", "Male") if profile else "Male"
p_age = int(profile.get("age", 25)) if profile else 25
p_height = int(profile.get("height", 170)) if profile else 170
p_weight = int(profile.get("weight", 70)) if profile else 70

with col_input:
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="form-section-title">Data Personal</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            gender_idx = 0 if p_gender == 'Male' else 1
            gender = st.radio(t("pred_gender", lang), ["Male", "Female"], index=gender_idx, horizontal=True)
            gender_val = 1 if gender == "Male" else 0
            age = st.slider(t("pred_age", lang), 10, 80, int(p_age))

        with c2:
            height = st.slider(t("pred_height", lang), 140, 210, int(p_height))
            weight = st.slider(t("pred_weight", lang), 30, 150, int(p_weight))

            bmi_val, bmi_cat, bmi_col = calculate_bmi(height, weight)
            if lang == "en":
                cat_map = {"Kurus": "Underweight", "Normal": "Normal", "Berlebih": "Overweight", "Obesitas": "Obese", "—": "—"}
                bmi_cat = cat_map.get(bmi_cat, bmi_cat)

            st.markdown(f"""
                <div style='margin-top: 10px;'>
                    <span style='color:#4D9E8F; font-size:0.82rem;'>{t('pred_bmi_label', lang)} </span>
                    <span style='color:#FFFFFF; font-weight:700;'>{bmi_val}</span>
                    <span class="bmi-pill" style='background:{bmi_col}18; color:{bmi_col}; border: 1px solid {bmi_col}33; margin-left:4px;'>{bmi_cat}</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="form-section-title">Detail Aktivitas</div>', unsafe_allow_html=True)

        duration = st.slider(t("pred_duration", lang), 1, 120, 30)

        c3, c4 = st.columns(2)
        with c3:
            heart_rate = st.slider(t("pred_heartrate", lang), 60, 200, 100)
        with c4:
            body_temp = st.slider(t("pred_bodytemp", lang), 36.0, 42.0, 37.5, step=0.1)

        st.markdown('</div>', unsafe_allow_html=True)

    predict_btn = st.button("Prediksi Sekarang", use_container_width=True)

    if is_logged_in() and profile:
        st.success(t("pred_profile_loaded", lang), icon="✅")
    elif not is_logged_in():
        st.info("Masuk untuk menyimpan riwayat prediksi Anda.")

with col_result:
    if predict_btn:
        with st.spinner("Menghitung prediksi..."):
            time.sleep(0.6)

            calories = predict_calories(gender_val, age, height, weight, duration, heart_rate, body_temp)
            intensity = get_intensity(calories)

            intensity_key = f"intensity_{intensity['label'].lower()}"
            intensity_label_translated = t(intensity_key, lang)

            equivalent = get_equivalent_activity(calories)
            suggestions = get_suggestions(calories, duration, heart_rate, weight)

            new_record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "date": date.today().isoformat(),
                "gender": gender,
                "gender_val": gender_val,
                "age": age,
                "height": height,
                "weight": weight,
                "duration": duration,
                "heart_rate": heart_rate,
                "body_temp": body_temp,
                "calories": calories,
                "intensity": intensity_label_translated,
                "bmi": bmi_val,
                "bmi_category": bmi_cat
            }
            is_saved = db.save_prediction(new_record)

            if is_saved:
                new_badges = check_badges(new_record, db)
                if new_badges:
                    for b in new_badges:
                        b_name = b['name_id'] if lang == 'id' else b['name_en']
                        st.toast(f"Pencapaian baru: {b_name}!", icon="🏆")

            # Result Card
            st.markdown(f"""
<div class="result-card">
    <div style='color:#4D9E8F; font-size:0.78rem; font-weight:600; text-transform:uppercase; letter-spacing:1px;'>{t('pred_result_label', lang)}</div>
    <div style='font-size:3.5rem; font-weight:800; color:#00C9A7; font-family:Outfit, sans-serif; line-height:1; margin: 8px 0;'>{calories} <span style='font-size:1.2rem; font-weight:500; color:#7DCFBA;'>kcal</span></div>
    <div class="intensity-badge" style='background:{intensity["color"]}18; color:{intensity["color"]}; border:1px solid {intensity["color"]}33;'>
        {t('pred_intensity_label', lang)}: {intensity_label_translated}
    </div>
</div>
""", unsafe_allow_html=True)

            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=calories,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [None, max(500, calories + 50)], 'tickwidth': 1, 'tickcolor': "#1D5C5C"},
                    'bar': {'color': intensity["bar_color"]},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#1D5C5C",
                    'steps': [
                        {'range': [0, 150], 'color': 'rgba(6,214,160,0.08)'},
                        {'range': [150, 300], 'color': 'rgba(255,209,102,0.08)'},
                        {'range': [300, max(500, calories + 50)], 'color': 'rgba(239,71,111,0.08)'}
                    ],
                }
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "#B0D8D8", 'family': "Inter"},
                height=230,
                margin=dict(l=20, r=20, t=28, b=0),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Tabs
            tab1, tab2, tab3 = st.tabs(["Saran", "Hidrasi", "Setara Makanan"])

            with tab1:
                for tip in suggestions:
                    st.markdown(f'<div class="suggestion-box">{tip}</div>', unsafe_allow_html=True)

            with tab2:
                hydro = calculate_hydration(weight, calories)
                st.markdown(f"""
                <div style="background:rgba(0,201,167,0.08); border:1px solid rgba(0,201,167,0.2); border-radius:12px; padding:16px; margin-top:8px;">
                    <div style="text-align:center; margin-bottom:10px;">
                        <span style="color:#7DCFBA; font-size:0.85rem;">{t('hydration_need', lang)}</span><br>
                        <span style="font-size:1.8rem; font-weight:700; color:#00C9A7;">{hydro['total_liters']} L</span><br>
                        <span style="color:#B0D8D8; font-size:0.82rem;">≈ {hydro['glasses']} {t('hydration_glasses', lang)}</span>
                    </div>
                    <div style="font-size:0.8rem; color:#4D9E8F; border-top:1px dashed rgba(0,201,167,0.2); padding-top:8px; display:flex; justify-content:space-between;">
                        <span>Kebutuhan dasar: {hydro['base_liters']}L</span>
                        <span>+{hydro['exercise_extra_ml']}ml dari olahraga</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with tab3:
                foods = get_food_equivalents(calories, lang)
                if foods:
                    food_html = ""
                    for f in foods[:3]:
                        burn_time = get_burn_time_for_food(f['food_cal'], duration, calories)
                        food_html += f"""
                        <div style="background:rgba(10,41,41,0.7); border:1px solid #1D5C5C; border-radius:10px; padding:12px; margin-bottom:8px; display:flex; align-items:center;">
                            <div style="font-size:1.8rem; margin-right:14px;">{f['emoji']}</div>
                            <div style="flex-grow:1;">
                                <div style="font-weight:600; color:#FFFFFF; font-size:0.9rem;">{f['name']}</div>
                                <div style="font-size:0.78rem; color:#4D9E8F;">{f['food_cal']} kcal · {f['portions']} porsi</div>
                            </div>
                            <div style="text-align:right; font-size:0.8rem; color:#FFD166;">
                                {burn_time} min
                            </div>
                        </div>
                        """
                    st.markdown(food_html, unsafe_allow_html=True)

            if is_saved:
                st.success(t("pred_saved", lang))
            elif not is_logged_in():
                st.warning("Prediksi tidak disimpan. Masuk untuk menyimpan riwayat.")

    else:
        st.markdown(f"""
<div class="empty-state">
    <div class="icon" style="font-size:2.5rem; opacity:0.4;">←</div>
    <div class="text">Isi form di samping lalu klik<br><b>Prediksi Sekarang</b></div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center; color:#2D7070; font-size:0.78rem;'>
    {t('model_footer', lang)}<br>{t('consult_footer', lang)}
</div>
""", unsafe_allow_html=True)
