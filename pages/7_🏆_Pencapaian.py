import streamlit as st

from utils.styles import get_custom_css
import utils.database as db
from utils.i18n import t, get_lang
from utils.badges import get_all_badges
from utils.auth import render_sidebar

st.set_page_config(
    page_title="Pencapaian — CaloriQ",
    page_icon="🏆",
    layout="wide",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_sidebar()
lang = get_lang()

# ── Page Header ──
st.markdown(
    '<div class="page-header">'
    '<div class="page-title">Pencapaian</div>'
    f'<div class="page-subtitle">{t("badge_subtitle", lang)}</div>'
    '</div>',
    unsafe_allow_html=True
)

# Load Badges
all_badges = get_all_badges()
earned_badge_ids = [b['badge_id'] for b in db.get_earned_badges()]

# Summary bar
earned_pct = int((len(earned_badge_ids) / len(all_badges)) * 100) if all_badges else 0
st.markdown(f"""
<div style="background:rgba(10,41,41,0.7); border:1px solid #1D5C5C; border-radius:12px; padding:16px; margin-bottom:20px; display:flex; align-items:center; gap:20px;">
    <div style="text-align:center; min-width:60px;">
        <div style="font-size:1.8rem; font-weight:800; color:#00C9A7; font-family:Outfit,sans-serif;">{len(earned_badge_ids)}</div>
        <div style="font-size:0.75rem; color:#4D9E8F;">dari {len(all_badges)}</div>
    </div>
    <div style="flex-grow:1;">
        <div style="font-size:0.82rem; color:#7DCFBA; margin-bottom:6px;">Badge diperoleh</div>
        <div style="background:#142F2F; border-radius:6px; height:8px; overflow:hidden;">
            <div style="background:linear-gradient(90deg,#00C9A7,#00DDB8); width:{earned_pct}%; height:100%; border-radius:6px;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Badge grid
cols = st.columns(4)

for i, badge in enumerate(all_badges):
    col = cols[i % 4]
    is_unlocked = badge['id'] in earned_badge_ids
    status_class = "unlocked" if is_unlocked else "locked"
    status_text = "Terbuka" if is_unlocked else "Terkunci"
    b_name = badge['name_id'] if lang == 'id' else badge['name_en']
    b_desc = badge['desc_id'] if lang == 'id' else badge['desc_en']

    with col:
        st.markdown(f"""
<div class="badge-card {status_class}">
    <div class="badge-emoji">{badge['emoji']}</div>
    <div class="badge-title">{b_name}</div>
    <div class="badge-desc">{b_desc}</div>
    <div class="badge-status status-{status_class}">{status_text}</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
