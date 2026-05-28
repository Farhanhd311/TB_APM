import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import utilities
from utils.styles import get_custom_css
from utils.predictor import predict_calories
import utils.database as db
from utils.i18n import t, get_lang

st.set_page_config(
    page_title="Simulasi Skenario — CaloriQ",
    page_icon="🔬",
    layout="wide",
)

# Apply CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)
lang = get_lang()

# Title
st.markdown(f'<div class="section-title">{t("sim_title", lang)}</div><div class="section-sub">{t("sim_subtitle", lang)}</div>', unsafe_allow_html=True)

# Load profile
profile = db.get_profile() or {}
p_gender = profile.get('gender', 'Male')
p_gender_val = 1 if p_gender == 'Male' else 0
p_age = profile.get('age', 25)
p_height = profile.get('height', 170.0)
p_weight = profile.get('weight', 70.0)

c_input, c_result = st.columns([1, 1.5])

with c_input:
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown(f'<div class="form-section-title">🛠️ {t("sim_params", lang)}</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div style="font-size:0.8rem; color:#7DCFBA; margin-bottom:12px;">{t("sim_note", lang)}</div>', unsafe_allow_html=True)
    
    sim_var = st.selectbox(
        t("sim_variable", lang),
        [t("feat_duration", lang), t("feat_heartrate", lang), t("feat_weight", lang)]
    )
    
    # Base values
    base_duration = st.slider(f'{t("sim_base", lang)} {t("feat_duration", lang)}', 10, 120, 30)
    base_hr = st.slider(f'{t("sim_base", lang)} {t("feat_heartrate", lang)}', 80, 180, 110)
    base_weight = st.slider(f'{t("sim_base", lang)} {t("feat_weight", lang)}', 40, 120, int(p_weight))
    
    st.markdown('</div>', unsafe_allow_html=True)

with c_result:
    st.markdown(f'<div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin-bottom:15px;">📊 {t("sim_results", lang)}</div>', unsafe_allow_html=True)
    
    # Generate simulation data
    sim_data = []
    
    if sim_var == t("feat_duration", lang):
        x_values = list(range(10, 121, 10))
        for x in x_values:
            cal = predict_calories(p_gender_val, p_age, p_height, base_weight, x, base_hr, 37.5)
            sim_data.append({"x": x, "cal": cal})
        x_label = t("feat_duration", lang) + " (min)"
        
    elif sim_var == t("feat_heartrate", lang):
        x_values = list(range(80, 181, 10))
        for x in x_values:
            cal = predict_calories(p_gender_val, p_age, p_height, base_weight, base_duration, x, 37.5)
            sim_data.append({"x": x, "cal": cal})
        x_label = t("feat_heartrate", lang) + " (bpm)"
        
    else: # Weight
        x_values = list(range(40, 121, 5))
        for x in x_values:
            cal = predict_calories(p_gender_val, p_age, p_height, x, base_duration, base_hr, 37.5)
            sim_data.append({"x": x, "cal": cal})
        x_label = t("feat_weight", lang) + " (kg)"

    df_sim = pd.DataFrame(sim_data)
    
    fig = px.line(
        df_sim, x="x", y="cal",
        labels={"x": x_label, "cal": "Prediksi Kalori (kcal)"},
        markers=True,
        color_discrete_sequence=["#FFD166"]
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B0D8D8"),
        xaxis=dict(showgrid=True, gridcolor="rgba(29,92,92,0.3)", color="#7DCFBA"),
        yaxis=dict(gridcolor="rgba(29,92,92,0.3)", color="#7DCFBA"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Conclusion
    cal_min = df_sim["cal"].min()
    cal_max = df_sim["cal"].max()
    diff = cal_max - cal_min
    
    st.info(f"**Kesimpulan:** Peningkatan {sim_var.lower()} dari batas minimum ke maksimum dapat meningkatkan pembakaran kalori hingga **{diff:.0f} kcal**.")
