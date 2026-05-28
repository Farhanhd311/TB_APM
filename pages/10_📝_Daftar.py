import streamlit as st
from utils.styles import get_custom_css
from utils.auth import init_auth_state, is_logged_in, register
from utils.i18n import t, get_lang, render_language_selector

st.set_page_config(page_title="Daftar — CaloriQ", page_icon="📝", layout="centered")

st.markdown(get_custom_css(), unsafe_allow_html=True)
init_auth_state()

with st.sidebar:
    render_language_selector()

lang = get_lang()

if is_logged_in():
    st.success(t("auth_already_logged_in", lang))
    st.page_link("pages/8_👤_Profil.py", label=t("auth_go_profile", lang))
    st.stop()

_, center, _ = st.columns([1, 1.2, 1])
with center:
    st.markdown(
        f"""
        <div class="auth-card">
            <div style="text-align:center; margin-bottom:20px;">
                <div style="font-size:2.5rem;">📝</div>
                <div class="section-title" style="margin:0;">{t("auth_register_title", lang)}</div>
                <div class="section-sub" style="margin-top:8px;">{t("auth_register_sub", lang)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("register_page_form"):
        username = st.text_input(t("auth_username", lang))
        password = st.text_input(t("auth_password", lang), type="password")
        confirm = st.text_input(t("auth_confirm_password", lang), type="password")
        submitted = st.form_submit_button(t("auth_register_btn", lang), use_container_width=True)

        if submitted:
            if not username.strip() or not password or not confirm:
                st.error(t("auth_fill_all", lang))
            elif password != confirm:
                st.error(t("auth_password_mismatch", lang))
            else:
                ok, msg = register(username.strip(), password)
                if ok:
                    st.success(msg)
                    st.page_link("pages/9_🔐_Login.py", label=t("auth_go_login", lang))
                else:
                    st.error(msg)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='text-align:center; color:#7DCFBA;'>{t('auth_have_account', lang)}</div>",
        unsafe_allow_html=True,
    )
    st.page_link("pages/9_🔐_Login.py", label=t("auth_login_link", lang), use_container_width=True)
