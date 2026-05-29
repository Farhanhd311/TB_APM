import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.styles import get_custom_css
from utils.predictor import predict_calories
import utils.database as db
from utils.i18n import t, get_lang
from utils.auth import render_sidebar

st.set_page_config(
    page_title="Simulasi What-If — CaloriQ",
    page_icon="🔬",
    layout="wide",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_sidebar()
lang = get_lang()

# ── Page Header ──
st.markdown(
    '<div class="page-header">'
    '<div class="page-title">Simulasi What-If</div>'
    f'<div class="page-subtitle">{t("sim_subtitle", lang)}</div>'
    '</div>',
    unsafe_allow_html=True
)

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
    st.markdown('<div class="form-section-title">Parameter Simulasi</div>', unsafe_allow_html=True)

    feat_dur = t("feat_duration", lang).replace("⏱ ", "")
    feat_hr = t("feat_heartrate", lang).replace("💓 ", "")
    feat_wt = t("feat_weight", lang).replace("⚖️ ", "")

    sim_var = st.selectbox(
        "Variabel yang disimulasikan",
        [feat_dur, feat_hr, feat_wt]
    )

    base_duration = st.slider("Durasi dasar (menit)", 10, 120, 30)
    base_hr = st.slider("Heart rate dasar (bpm)", 80, 180, 110)
    base_weight = st.slider("Berat badan dasar (kg)", 40, 120, int(p_weight))

    st.markdown('</div>', unsafe_allow_html=True)

with c_result:
    st.markdown(
        '<div style="font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:14px;">Hasil Simulasi</div>',
        unsafe_allow_html=True
    )

    sim_data = []

    if sim_var == feat_dur:
        x_values = list(range(10, 121, 10))
        for x in x_values:
            cal = predict_calories(p_gender_val, p_age, p_height, base_weight, x, base_hr, 37.5)
            sim_data.append({"x": x, "cal": cal})
        x_label = "Durasi (menit)"

    elif sim_var == feat_hr:
        x_values = list(range(80, 181, 10))
        for x in x_values:
            cal = predict_calories(p_gender_val, p_age, p_height, base_weight, base_duration, x, 37.5)
            sim_data.append({"x": x, "cal": cal})
        x_label = "Heart Rate (bpm)"

    else:
        x_values = list(range(40, 121, 5))
        for x in x_values:
            cal = predict_calories(p_gender_val, p_age, p_height, x, base_duration, base_hr, 37.5)
            sim_data.append({"x": x, "cal": cal})
        x_label = "Berat Badan (kg)"

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
        xaxis=dict(showgrid=True, gridcolor="rgba(29,92,92,0.25)", color="#7DCFBA"),
        yaxis=dict(gridcolor="rgba(29,92,92,0.25)", color="#7DCFBA"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=380
    )
    st.plotly_chart(fig, use_container_width=True)

    cal_min = df_sim["cal"].min()
    cal_max = df_sim["cal"].max()
    diff = cal_max - cal_min

    st.info(
        f"**Kesimpulan:** Perubahan {sim_var.lower()} dari batas minimum ke maksimum "
        f"dapat mengubah kalori terbakar hingga **{diff:.0f} kcal**."
    )
