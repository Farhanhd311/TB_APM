import streamlit as st

# Import utilities
from utils.styles import get_custom_css
import utils.database as db
from utils.i18n import t, get_lang
from utils.badges import get_all_badges

st.set_page_config(
    page_title="Pencapaian — CaloriQ",
    page_icon="🏆",
    layout="wide",
)

# Apply CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)
lang = get_lang()

# Title
st.markdown(f'<div class="section-title">{t("badge_title", lang)}</div><div class="section-sub">{t("badge_subtitle", lang)}</div>', unsafe_allow_html=True)

# Load Badges
all_badges = get_all_badges()
earned_badge_ids = [b['badge_id'] for b in db.get_earned_badges()]

st.markdown(f'<div style="margin-bottom: 24px; text-align:center;"><span style="font-size:1.5rem; font-weight:700; color:#00C9A7;">{len(earned_badge_ids)}</span> <span style="color:#7DCFBA;">/ {len(all_badges)} {t("badge_earned_label", lang)}</span></div>', unsafe_allow_html=True)

# Group by category (optional, here we just list them in a grid)
cols = st.columns(4)

for i, badge in enumerate(all_badges):
    col = cols[i % 4]
    
    is_unlocked = badge['id'] in earned_badge_ids
    
    status_class = "unlocked" if is_unlocked else "locked"
    status_text = "Terkunci"
    if is_unlocked:
        status_text = "Terbuka"
        
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
