import streamlit as st
import time

from utils.styles import get_custom_css
import utils.database as db
from utils.i18n import t, get_lang
from utils.auth import init_auth_state, is_logged_in, render_account_sidebar, get_current_user

st.set_page_config(
    page_title="Profil Pengguna — CaloriQ",
    page_icon="👤",
    layout="wide",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
init_auth_state()
lang = get_lang()
render_account_sidebar()

st.markdown(
    f'<div class="section-title">{t("prof_title", lang)}</div>'
    f'<div class="section-sub">{t("prof_subtitle", lang)}</div>',
    unsafe_allow_html=True,
)

if not is_logged_in():
    st.info(t("prof_login_required", lang))
    st.page_link("pages/9_🔐_Login.py", label=f"🔐 {t('auth_login', lang)}")
    st.page_link("pages/10_📝_Daftar.py", label=f"📝 {t('auth_register', lang)}")
    st.stop()

current_user = get_current_user()
profile = db.get_profile() or {}
p_name = profile.get("name", current_user["username"])
p_gender = profile.get("gender", "Male")
p_age = int(profile.get("age", 25))
p_height = float(profile.get("height", 170))
p_weight = float(profile.get("weight", 70))
p_language = profile.get("language", "id")

c_prof, c_edit = st.columns([1, 2])

with c_prof:
    st.markdown(
        f"""
<div class="profile-card">
<div class="profile-avatar">{"👱‍♂️" if p_gender == "Male" else "👩"}</div>
<div style="font-size:1.4rem; font-weight:700; color:#FFFFFF;">{p_name}</div>
<div style="color:#B0D8D8; font-size:0.85rem; margin-top:4px;">@{current_user['username']}</div>
<div style="color:#00C9A7; font-weight:600; margin-bottom:16px;">{t("prof_member", lang)}</div>
<div style="display:flex; justify-content:space-between; border-top:1px solid #1D5C5C; padding-top:12px; margin-top:12px; font-size:0.9rem;">
<span style="color:#7DCFBA;">{t("pred_age", lang)}</span>
<span style="color:#FFFFFF; font-weight:600;">{p_age}</span>
</div>
<div style="display:flex; justify-content:space-between; border-top:1px solid #1D5C5C; padding-top:12px; margin-top:12px; font-size:0.9rem;">
<span style="color:#7DCFBA;">{t("pred_height", lang)}</span>
<span style="color:#FFFFFF; font-weight:600;">{p_height} cm</span>
</div>
<div style="display:flex; justify-content:space-between; border-top:1px solid #1D5C5C; padding-top:12px; margin-top:12px; font-size:0.9rem;">
<span style="color:#7DCFBA;">{t("pred_weight", lang)}</span>
<span style="color:#FFFFFF; font-weight:600;">{p_weight} kg</span>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with c_edit:
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown(f'<div class="form-section-title">⚙️ {t("prof_edit", lang)}</div>', unsafe_allow_html=True)

    with st.form("profile_form"):
        new_name = st.text_input(t("prof_nickname", lang), value=p_name)

        col1, col2 = st.columns(2)
        with col1:
            gender_idx = 0 if p_gender == "Male" else 1
            new_gender = st.selectbox(t("pred_gender", lang), ["Male", "Female"], index=gender_idx)
            new_age = st.number_input(t("pred_age", lang), min_value=10, max_value=100, value=p_age)
        with col2:
            new_height = st.number_input(t("pred_height", lang), min_value=100, max_value=250, value=int(p_height))
            new_weight = st.number_input(t("pred_weight", lang), min_value=30, max_value=200, value=int(p_weight))

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:0.9rem; color:#7DCFBA; margin-bottom:8px;">🌍 {t("prof_lang", lang)}</div>',
            unsafe_allow_html=True,
        )

        lang_idx = 0 if p_language == "id" else 1
        new_language = st.radio(
            "Bahasa",
            ["id", "en"],
            index=lang_idx,
            format_func=lambda x: "🇮🇩 Indonesia" if x == "id" else "🇬🇧 English",
            horizontal=True,
        )

        submit = st.form_submit_button(t("prof_save", lang), use_container_width=True)

        if submit:
            saved = db.save_profile(new_name, new_gender, new_age, new_height, new_weight, new_language)
            if saved:
                st.session_state.language = new_language
                st.success(t("prof_saved", lang))
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(t("prof_save_failed", lang))

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔴 Reset Seluruh Data & Riwayat (Danger Zone)", use_container_width=True, type="primary"):
        db.reset_all_data()
        st.warning(t("prof_reset_done", lang))
        st.rerun()
