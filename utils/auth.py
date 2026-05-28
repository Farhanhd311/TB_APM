import streamlit as st
import utils.database as db
from utils.i18n import t, get_lang


def init_auth_state():
    if "user" not in st.session_state:
        st.session_state.user = None


def get_current_user():
    init_auth_state()
    return st.session_state.user


def get_current_user_id():
    user = get_current_user()
    return user.get("id") if user else None


def is_logged_in():
    return get_current_user() is not None


def login(username: str, password: str):
    user = db.authenticate_user(username, password)
    if not user:
        return False, "Username atau password salah."
    st.session_state.user = user
    db.get_profile(user_id=user["id"])
    return True, "Login berhasil."


def register(username: str, password: str):
    return db.create_user(username, password)


def logout():
    st.session_state.user = None


def render_account_sidebar():
    """Compact account status in sidebar (no login/register forms)."""
    init_auth_state()
    lang = get_lang()
    user = get_current_user()

    with st.sidebar:
        st.markdown("<hr style='border-color:#1D5C5C; margin:12px 0;'>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:0.75rem; color:#7DCFBA; font-weight:600; text-transform:uppercase; letter-spacing:1px;'>"
            f"{t('auth_account', lang)}</div>",
            unsafe_allow_html=True,
        )

        if user:
            st.markdown(
                f"<div style='color:#FFFFFF; font-size:0.9rem; margin:8px 0;'>"
                f"👋 {t('auth_hello', lang)}, <b>{user['username']}</b></div>",
                unsafe_allow_html=True,
            )
            if st.button(t("auth_logout", lang), use_container_width=True, key="sidebar_logout"):
                logout()
                st.rerun()
        else:
            st.markdown(
                f"<div style='color:#7DCFBA; font-size:0.85rem; margin:8px 0 12px;'>"
                f"{t('auth_guest_hint', lang)}</div>",
                unsafe_allow_html=True,
            )
            st.page_link("pages/9_🔐_Login.py", label=f"🔐 {t('auth_login', lang)}", use_container_width=True)
            st.page_link("pages/10_📝_Daftar.py", label=f"📝 {t('auth_register', lang)}", use_container_width=True)
