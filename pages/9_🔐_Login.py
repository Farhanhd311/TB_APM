import streamlit as st
from utils.styles import get_custom_css
from utils.auth import render_sidebar, is_logged_in, login
from utils.i18n import t, get_lang

st.set_page_config(page_title="Masuk — CaloriQ", page_icon="🔐", layout="centered")

st.markdown(get_custom_css(), unsafe_allow_html=True)
render_sidebar()
lang = get_lang()

if is_logged_in():
    st.success(t("auth_already_logged_in", lang))
    st.page_link("pages/1_🔥_Prediksi.py", label=t("auth_go_predict", lang))
    st.page_link("pages/8_👤_Profil.py", label=t("auth_go_profile", lang))
    st.stop()

_, center, _ = st.columns([1, 2.5, 1])
with center:
    st.markdown("""
        <style>
        /* Unify the form to look like the main auth card */
        [data-testid="stForm"] {
            background: linear-gradient(135deg, rgba(15,61,61,0.9), rgba(10,41,41,0.95)) !important;
            border: 1px solid #1D5C5C !important;
            border-radius: 18px !important;
            padding: 40px 36px !important;
            box-shadow: 0 16px 50px rgba(0,0,0,0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.form("login_page_form"):
        st.markdown(
            f"""
            <div style="text-align:center; margin-bottom:24px;">
                <div style="
                    width:56px; height:56px;
                    background:rgba(0,201,167,0.1);
                    border:1px solid rgba(0,201,167,0.25);
                    border-radius:14px;
                    display:inline-flex;
                    align-items:center;
                    justify-content:center;
                    font-size:1.6rem;
                    margin-bottom:14px;
                ">🔐</div>
                <div class="section-title" style="margin:0; font-size:1.4rem;">{t("auth_login_title", lang)}</div>
                <div class="section-sub" style="margin-top:6px;">{t("auth_login_sub", lang)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


        username = st.text_input(t("auth_username", lang))
        password = st.text_input(t("auth_password", lang), type="password")
        submitted = st.form_submit_button("Masuk", use_container_width=True)

        if submitted:
            if not username.strip() or not password:
                st.error(t("auth_fill_all", lang))
            else:
                ok, msg = login(username.strip(), password)
                if ok:
                    st.success(msg)
                    st.switch_page("pages/8_👤_Profil.py")
                else:
                    st.error(msg)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='text-align:center; color:#4D9E8F; font-size:0.9rem; margin-bottom:8px;'>{t('auth_no_account', lang)}</div>",
        unsafe_allow_html=True,
    )
    # Using columns to center the st.page_link cleanly
    _, link_col, _ = st.columns([1, 2, 1])
    with link_col:
        st.page_link("pages/10_📝_Daftar.py", label=t("auth_register_link", lang), use_container_width=True)
