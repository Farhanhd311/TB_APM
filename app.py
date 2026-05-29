import streamlit as st
import plotly.graph_objects as go
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from utils.styles import get_custom_css
from utils.predictor import get_feature_importances
import utils.database as db
from utils.i18n import t, get_lang
from utils.auth import render_sidebar

st.set_page_config(
    page_title="CaloriQ — Prediksi Kalori",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_sidebar()

lang = get_lang()

# ══════════════════════════════════════════════
#  HERO SECTION
# ══════════════════════════════════════════════
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title">CaloriQ</div>
    <div class="hero-subtitle">{t('home_subtitle', lang)}</div>
    <div style='margin-top:16px;'>
        <span class="hero-badge">Random Forest</span>
        <span class="hero-badge">R² 99.99%</span>
        <span class="hero-badge">15.000 Data</span>
        <span class="hero-badge">Real-time</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  METRIC CARDS
# ══════════════════════════════════════════════
st.markdown(
    f'<div class="section-title">{t("home_perf", lang)}</div>'
    f'<div class="section-sub">{t("home_perf_sub", lang)}</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric(t("home_accuracy", lang).replace("🎯 ", ""), "99.99%", "R² Score")
with c2:
    st.metric(t("home_mae", lang).replace("📉 ", ""), "~1.77 kcal", "Mean Abs. Error")
with c3:
    st.metric(t("home_trees", lang).replace("🌲 ", ""), "100 pohon", "n_estimators")
with c4:
    total_preds = db.get_prediction_count()
    st.metric(t("home_total_pred", lang).replace("🔮 ", ""), f"{total_preds}x", "Total Database")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  FEATURE IMPORTANCE CHART
# ══════════════════════════════════════════════
st.markdown(
    f'<div class="section-title">{t("home_fi_title", lang).replace("🔍 ", "")}</div>'
    f'<div class="section-sub">{t("home_fi_sub", lang)}</div>',
    unsafe_allow_html=True
)

col_fi, col_eval = st.columns([3, 2])

with col_fi:
    with st.spinner("Memuat data model..."):
        fi = get_feature_importances()

    label_map = {
        "Duration":   t("feat_duration", lang).replace("⏱ ", ""),
        "Heart_Rate": t("feat_heartrate", lang).replace("💓 ", ""),
        "Body_Temp":  t("feat_bodytemp", lang).replace("🌡 ", ""),
        "Weight":     t("feat_weight", lang).replace("⚖️ ", ""),
        "Age":        t("feat_age", lang).replace("🎂 ", ""),
        "Height":     t("feat_height", lang).replace("📏 ", ""),
        "Gender":     t("feat_gender", lang).replace("👤 ", ""),
    }
    fi_labels = [label_map.get(f, f) for f in fi.index]
    colors = ["#00C9A7" if i == 0 else f"rgba(0,201,167,{0.7 - i*0.08})" for i in range(len(fi))]

    fig_fi = go.Figure(go.Bar(
        x=fi.values[::-1],
        y=fi_labels[::-1],
        orientation="h",
        marker=dict(color=colors[::-1], line=dict(width=0)),
        text=[f"{v:.3f}" for v in fi.values[::-1]],
        textposition="outside",
        textfont=dict(color="#7DCFBA", size=11),
    ))
    fig_fi.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#B0D8D8", family="Inter"),
        xaxis=dict(showgrid=True, gridcolor="rgba(29,92,92,0.3)", color="#7DCFBA", zeroline=False),
        yaxis=dict(showgrid=False, color="#B0D8D8"),
        margin=dict(l=10, r=60, t=10, b=10),
        height=270,
    )
    st.plotly_chart(fig_fi, use_container_width=True)

with col_eval:
    st.markdown(
        f'<div style="color:#7DCFBA; font-size:0.85rem; font-weight:600; margin-bottom:10px;">'
        f'{t("home_eval", lang).replace("📊 ", "")}</div>',
        unsafe_allow_html=True
    )
    eval_img = os.path.join(os.path.dirname(__file__), "hasil_evaluasi", "evaluasi_model.png")
    if os.path.exists(eval_img):
        st.image(eval_img, use_container_width=True, caption=t("home_eval_caption", lang))
    else:
        st.info(t("home_eval_missing", lang))

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  HOW TO USE
# ══════════════════════════════════════════════
st.markdown(
    f'<div class="section-title">{t("home_usage", lang).replace("🚀 ", "")}</div>'
    f'<div class="section-sub">{t("home_usage_sub", lang)}</div>',
    unsafe_allow_html=True
)

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-number">01</div>
        <div class="step-title">{t("home_step1_title", lang)}</div>
        <div class="step-desc">{t("home_step1_desc", lang)}</div>
    </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-number">02</div>
        <div class="step-title">{t("home_step2_title", lang)}</div>
        <div class="step-desc">{t("home_step2_desc", lang)}</div>
    </div>
    """, unsafe_allow_html=True)
with s3:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-number">03</div>
        <div class="step-title">{t("home_step3_title", lang)}</div>
        <div class="step-desc">{t("home_step3_desc", lang)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  CTA
# ══════════════════════════════════════════════
st.markdown(f"""
<div style='text-align:center; background:linear-gradient(135deg,rgba(0,201,167,0.07),rgba(7,30,30,0.9));
border:1px solid rgba(0,201,167,0.2); border-radius:16px; padding:32px;'>
    <div style='font-family:Outfit,sans-serif; font-size:1.4rem; font-weight:700; color:#FFFFFF; margin-bottom:8px;'>
        {t("home_cta", lang).replace(" 🔥", "")}
    </div>
    <div style='color:#4D9E8F; font-size:0.9rem;'>{t("home_cta_sub", lang)}</div>
</div>
""", unsafe_allow_html=True)
