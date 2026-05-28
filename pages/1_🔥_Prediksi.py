import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, date
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
import utils.database as db
from utils.i18n import t, get_lang
from utils.hydration import calculate_hydration
from utils.food_equiv import get_food_equivalents, get_burn_time_for_food
from utils.badges import check_badges
from utils.auth import init_auth_state, is_logged_in, render_account_sidebar

st.set_page_config(
    page_title="Prediksi Kalori — CaloriQ",
    page_icon="🔥",
    layout="wide",
)

# Apply CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)
init_auth_state()
lang = get_lang()
render_account_sidebar()

# Title
st.markdown(f'<div class="section-title">{t("pred_title", lang)}</div><div class="section-sub">{t("pred_subtitle", lang)}</div>', unsafe_allow_html=True)

# Form Layout
col_input, col_result = st.columns([1.2, 1])

# Load profile for auto-fill (logged-in users)
profile = db.get_profile() if is_logged_in() else {}
p_gender = profile.get("gender", "Male") if profile else "Male"
p_age = int(profile.get("age", 25)) if profile else 25
p_height = int(profile.get("height", 170)) if profile else 170
p_weight = int(profile.get("weight", 70)) if profile else 70

with col_input:
    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="form-section-title">{t("pred_personal", lang)}</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            gender_idx = 0 if p_gender == 'Male' else 1
            gender = st.radio(t("pred_gender", lang), ["Male", "Female"], index=gender_idx, horizontal=True)
            gender_val = 1 if gender == "Male" else 0
            
            age = st.slider(t("pred_age", lang), 10, 80, int(p_age))
        
        with c2:
            height = st.slider(t("pred_height", lang), 140, 210, int(p_height))
            weight = st.slider(t("pred_weight", lang), 30, 150, int(p_weight))
            
            # Real-time BMI Calculation
            bmi_val, bmi_cat, bmi_col = calculate_bmi(height, weight)
            
            # Translate BMI Category if needed
            if lang == "en":
                cat_map = {"Kurus": "Underweight", "Normal": "Normal", "Berlebih": "Overweight", "Obesitas": "Obese", "—": "—"}
                bmi_cat = cat_map.get(bmi_cat, bmi_cat)
                
            st.markdown(f"""
                <div style='margin-top: 10px;'>
                    <span style='color:#7DCFBA; font-size:0.85rem;'>{t('pred_bmi_label', lang)} </span>
                    <span style='color:#FFFFFF; font-weight:700;'>{bmi_val}</span>
                    <span class="bmi-pill" style='background:{bmi_col}22; color:{bmi_col}; border: 1px solid {bmi_col}44;'>{bmi_cat}</span>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="form-section-title">{t("pred_activity", lang)}</div>', unsafe_allow_html=True)
        
        duration = st.slider(t("pred_duration", lang), 1, 120, 30)
        
        c3, c4 = st.columns(2)
        with c3:
            heart_rate = st.slider(t("pred_heartrate", lang), 60, 200, 100)
        with c4:
            body_temp = st.slider(t("pred_bodytemp", lang), 36.0, 42.0, 37.5, step=0.1)
            
        st.markdown('</div>', unsafe_allow_html=True)

    predict_btn = st.button(t("pred_button", lang), use_container_width=True)
    if is_logged_in() and profile:
        st.success(t("pred_profile_loaded", lang))
    elif not is_logged_in():
        st.info(t("auth_guest_hint", lang))
        st.page_link("pages/9_🔐_Login.py", label=f"🔐 {t('auth_login', lang)}")

with col_result:
    if predict_btn:
        with st.spinner(t("pred_computing", lang)):
            time.sleep(0.8) # Artificial delay for better UX
            
            # Get Prediction
            calories = predict_calories(gender_val, age, height, weight, duration, heart_rate, body_temp)
            intensity = get_intensity(calories)
            
            # Translate intensity label
            intensity_key = f"intensity_{intensity['label'].lower()}"
            intensity_label_translated = t(intensity_key, lang)
            
            equivalent = get_equivalent_activity(calories)
            suggestions = get_suggestions(calories, duration, heart_rate, weight)
            
            # Save to Database
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
            
            # Check badges only for logged in users with saved history
            if is_saved:
                new_badges = check_badges(new_record, db)
                if new_badges:
                    for b in new_badges:
                        b_name = b['name_id'] if lang == 'id' else b['name_en']
                        st.toast(f"{t('pred_badge_new', lang)} {b['emoji']} {b_name}!", icon="🎉")
            
            # Display Results
            st.markdown(f"""
<div class="result-card">
    <div style='color:#7DCFBA; font-size:0.9rem; font-weight:600; text-transform:uppercase; letter-spacing:1px;'>{t('pred_result_label', lang)}</div>
    <div style='font-size:4rem; font-weight:800; color:#00C9A7; font-family:Outfit, sans-serif; line-height:1;'>{calories} <span style='font-size:1.5rem; font-weight:500; color:#7DCFBA;'>kcal</span></div>
    <div class="intensity-badge" style='background:{intensity["color"]}22; color:{intensity["color"]}; border:1px solid {intensity["color"]}44;'>
        {intensity["emoji"]} {t('pred_intensity_label', lang)} {intensity_label_translated}
    </div>
</div>
""", unsafe_allow_html=True)
            
            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = calories,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, max(500, calories + 50)], 'tickwidth': 1, 'tickcolor': "#1D5C5C"},
                    'bar': {'color': intensity["bar_color"]},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "#1D5C5C",
                    'steps': [
                        {'range': [0, 150], 'color': 'rgba(6, 214, 160, 0.1)'},
                        {'range': [150, 300], 'color': 'rgba(255, 209, 102, 0.1)'},
                        {'range': [300, max(500, calories + 50)], 'color': 'rgba(239, 71, 111, 0.1)'}
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
            
            # Tabs for details
            tab1, tab2, tab3 = st.tabs([t("pred_suggestions", lang).replace("💡 ", ""), t("pred_hydration", lang).replace("💧 ", ""), t("pred_food", lang).replace("🍽️ ", "")])
            
            with tab1:
                # Suggestions
                st.markdown(f'<div style="margin-top:10px; font-weight:600; color:#FFFFFF;">💡 {t("pred_suggestions", lang).replace("💡 ", "")}</div>', unsafe_allow_html=True)
                for tip in suggestions:
                    st.markdown(f'<div class="suggestion-box">{tip}</div>', unsafe_allow_html=True)
                    
            with tab2:
                # Hydration
                hydro = calculate_hydration(weight, calories)
                st.markdown(f'<div style="margin-top:10px; font-weight:600; color:#FFFFFF;">💧 {t("pred_hydration", lang).replace("💧 ", "")}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:rgba(0,201,167,0.1); border:1px solid rgba(0,201,167,0.3); border-radius:12px; padding:16px; margin-top:8px;">
                    <div style="text-align:center; margin-bottom:12px;">
                        <span style="font-size:2rem;">💧</span><br>
                        <span style="color:#7DCFBA;">{t('hydration_need', lang)}</span><br>
                        <span style="font-size:1.5rem; font-weight:700; color:#00C9A7;">{hydro['total_liters']} Liter</span><br>
                        <span style="color:#B0D8D8; font-size:0.85rem;">≈ {hydro['glasses']} {t('hydration_glasses', lang)}</span>
                    </div>
                    <div style="font-size:0.85rem; color:#7DCFBA; border-top:1px dashed rgba(0,201,167,0.3); padding-top:8px; display:flex; justify-content:space-between;">
                        <span>{t('hydration_base', lang)}: {hydro['base_liters']}L</span>
                        <span>{t('hydration_extra', lang)}: +{hydro['exercise_extra_ml']}ml</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with tab3:
                # Food Equivalents
                foods = get_food_equivalents(calories, lang)
                st.markdown(f'<div style="margin-top:10px; font-weight:600; color:#FFFFFF;">🍽️ {t("pred_food", lang).replace("🍽️ ", "")}</div>', unsafe_allow_html=True)
                
                if foods:
                    food_html = ""
                    for f in foods[:3]:  # Show top 3
                        burn_time = get_burn_time_for_food(f['food_cal'], duration, calories)
                        food_html += f"""
                        <div style="background:rgba(13,53,53,0.6); border:1px solid #1D5C5C; border-radius:10px; padding:12px; margin-bottom:8px; display:flex; align-items:center;">
                            <div style="font-size:2rem; margin-right:16px;">{f['emoji']}</div>
                            <div style="flex-grow:1;">
                                <div style="font-weight:600; color:#FFFFFF;">{f['name']}</div>
                                <div style="font-size:0.8rem; color:#7DCFBA;">{f['food_cal']} kcal • {t('food_equal', lang)} {f['portions']} {t('food_portions', lang)}</div>
                            </div>
                            <div style="text-align:right; font-size:0.85rem; color:#FFD166;">
                                ⏱️ {burn_time}<br>min
                            </div>
                        </div>
                        """
                    st.markdown(food_html, unsafe_allow_html=True)
                
            if is_saved:
                st.success(t("pred_saved", lang))
            else:
                st.warning("Hasil prediksi tidak disimpan. Login terlebih dahulu jika ingin menyimpan riwayat.")
            
    else:
        # Empty State
        st.markdown(f"""
<div class="empty-state">
    <div class="icon">👈</div>
    <div class="text">{t("pred_fill_form", lang)} <br><b>"{t('pred_button', lang).replace('🔥 ', '')}"</b> {t('pred_to_see', lang).replace('"', '')}</div>
</div>
""", unsafe_allow_html=True)

# Footer info
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align:center; color:#5D8C8C; font-size:0.8rem;'>
    {t('model_footer', lang)}<br>
    {t('consult_footer', lang)}
</div>
""", unsafe_allow_html=True)
