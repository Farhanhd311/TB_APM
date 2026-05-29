import streamlit as st
import time

from utils.styles import get_custom_css
import utils.database as db
from utils.i18n import t, get_lang
from utils.auth import render_sidebar, is_logged_in, get_current_user

st.set_page_config(
    page_title="Profil — CaloriQ",
    page_icon="👤",
    layout="wide",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_sidebar()
lang = get_lang()

# ── Page Header ──
st.markdown(
    '<div class="page-header">'
    '<div class="page-title">Profil Pengguna</div>'
    f'<div class="page-subtitle">{t("prof_subtitle", lang)}</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Guard Login ──
if not is_logged_in():
    st.info(t("prof_login_required", lang))
    st.page_link("pages/9_🔐_Login.py", label="Masuk ke akun")
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
    # Avatar icon based on gender (text only, no emoji)
    avatar_initial = (p_name or current_user["username"])[0].upper()

    st.markdown(f"""
<div class="profile-card">
<div style="text-align:center; margin-bottom:16px;">
    <div style="
        width:72px; height:72px;
        background: linear-gradient(135deg, rgba(0,201,167,0.2), rgba(0,201,167,0.05));
        border: 2px solid rgba(0,201,167,0.35);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-family: Outfit, sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #00C9A7;
        margin-bottom: 12px;
    ">{avatar_initial}</div>
    <div style="font-size:1.2rem; font-weight:700; color:#FFFFFF;">{p_name}</div>
    <div style="color:#4D9E8F; font-size:0.82rem; margin-top:2px;">@{current_user['username']}</div>
    <div style="color:#00C9A7; font-size:0.78rem; font-weight:600; margin-top:6px; letter-spacing:0.5px;">Member CaloriQ</div>
</div>
<div style="border-top:1px solid #1D5C5C; padding-top:14px;">
    <div style="display:flex; justify-content:space-between; padding:8px 0; font-size:0.88rem;">
        <span style="color:#4D9E8F;">Usia</span>
        <span style="color:#FFFFFF; font-weight:600;">{p_age} tahun</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:8px 0; font-size:0.88rem; border-top:1px solid #1D5C5C11;">
        <span style="color:#4D9E8F;">Tinggi</span>
        <span style="color:#FFFFFF; font-weight:600;">{p_height} cm</span>
    </div>
    <div style="display:flex; justify-content:space-between; padding:8px 0; font-size:0.88rem; border-top:1px solid #1D5C5C11;">
        <span style="color:#4D9E8F;">Berat</span>
        <span style="color:#FFFFFF; font-weight:600;">{p_weight} kg</span>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

with c_edit:
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown(f'<div class="form-section-title">Edit Profil</div>', unsafe_allow_html=True)

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
            f'<div style="font-size:0.85rem; color:#4D9E8F; margin-bottom:8px;">Bahasa / Language</div>',
            unsafe_allow_html=True,
        )

        lang_idx = 0 if p_language == "id" else 1
        new_language = st.radio(
            "Bahasa",
            ["id", "en"],
            index=lang_idx,
            format_func=lambda x: "Indonesia" if x == "id" else "English",
            horizontal=True,
            label_visibility="collapsed"
        )

        submit = st.form_submit_button(t("prof_save", lang).replace("💾 ", ""), use_container_width=True)

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

    # Danger zone
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("Zona Berbahaya — Reset Data"):
        st.warning("Tindakan ini akan menghapus **semua** riwayat, profil, badge, dan target secara permanen.")
        if st.button("Hapus Semua Data", type="primary"):
            db.reset_all_data()
            st.warning(t("prof_reset_done", lang))
            st.rerun()
