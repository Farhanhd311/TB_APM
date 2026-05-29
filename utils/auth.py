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


def render_sidebar():
    """
    Satu-satunya fungsi sidebar terpusat.
    Panggil ini di setiap halaman, TIDAK perlu memanggil init_auth_state() terpisah.
    """
    init_auth_state()
    lang = get_lang()
    user = get_current_user()

    with st.sidebar:
        # ── Logo & Brand ──────────────────────────────
        st.markdown("""
<div style='text-align:center; padding: 20px 0 16px;'>
    <div style='
        font-family: Outfit, sans-serif;
        font-size: 1.7rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00C9A7, #7DCFBA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        letter-spacing: -0.5px;
    '>CaloriQ</div>
    <div style='font-size: 0.72rem; color: #4D9E8F; margin-top: 4px; letter-spacing: 0.5px;'>
        AI Calorie Predictor
    </div>
</div>
<div style='height: 1px; background: linear-gradient(90deg, transparent, #1D5C5C, transparent); margin: 0 8px 12px;'></div>
""", unsafe_allow_html=True)

        # ── Menu Utama ─────────────────────────────────
        st.markdown(
            "<div style='font-size:0.68rem; color:#4D9E8F; font-weight:700; "
            "text-transform:uppercase; letter-spacing:1.2px; padding: 0 8px 6px;'>Menu Utama</div>",
            unsafe_allow_html=True
        )

        st.page_link("app.py", label="Beranda", icon=":material/home:")
        st.page_link("pages/1_🔥_Prediksi.py", label="Prediksi Kalori", icon=":material/monitor_heart:")
        st.page_link("pages/2_📊_Riwayat.py", label="Riwayat & Statistik", icon=":material/history:")
        st.page_link("pages/3_🎯_Target.py", label="Target Harian", icon=":material/flag:")
        st.page_link("pages/4_📈_Dashboard.py", label="Dashboard Analitik", icon=":material/bar_chart:")

        # ── Fitur Lainnya ─────────────────────────────
        st.markdown(
            "<div style='height:1px; background:#1D5C5C33; margin: 8px 8px;'></div>"
            "<div style='font-size:0.68rem; color:#4D9E8F; font-weight:700; "
            "text-transform:uppercase; letter-spacing:1.2px; padding: 4px 8px 6px;'>Fitur Lainnya</div>",
            unsafe_allow_html=True
        )

        st.page_link("pages/5_🏋️_Program.py", label="Program Olahraga", icon=":material/fitness_center:")
        st.page_link("pages/6_🔬_Simulasi.py", label="Simulasi What-If", icon=":material/science:")
        st.page_link("pages/7_🏆_Pencapaian.py", label="Pencapaian", icon=":material/emoji_events:")

        # ── Akun ──────────────────────────────────────
        st.markdown(
            "<div style='height:1px; background:#1D5C5C33; margin: 8px 8px;'></div>"
            "<div style='font-size:0.68rem; color:#4D9E8F; font-weight:700; "
            "text-transform:uppercase; letter-spacing:1.2px; padding: 4px 8px 6px;'>Akun</div>",
            unsafe_allow_html=True
        )

        if user:
            st.markdown(
                f"<div style='padding: 8px 12px; background: rgba(0,201,167,0.08); "
                f"border: 1px solid rgba(0,201,167,0.2); border-radius: 10px; margin-bottom: 8px;'>"
                f"<div style='font-size:0.75rem; color:#7DCFBA;'>Masuk sebagai</div>"
                f"<div style='font-weight:700; color:#FFFFFF; font-size:0.95rem;'>{user['username']}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            col_prof, col_out = st.columns(2)
            with col_prof:
                st.page_link("pages/8_👤_Profil.py", label="Profil", icon=":material/person:", use_container_width=True)
            with col_out:
                if st.button("Keluar", use_container_width=True, key="sidebar_logout"):
                    logout()
                    st.rerun()
        else:
            st.markdown(
                "<div style='font-size:0.82rem; color:#4D9E8F; padding: 0 4px 8px; line-height:1.4;'>"
                "Masuk untuk menyimpan riwayat dan profil Anda.</div>",
                unsafe_allow_html=True,
            )
            st.page_link("pages/9_🔐_Login.py", label="Masuk", icon=":material/login:", use_container_width=True)
            st.page_link("pages/10_📝_Daftar.py", label="Daftar Akun", icon=":material/person_add:", use_container_width=True)

        # ── Bahasa ────────────────────────────────────
        st.markdown(
            "<div style='height:1px; background:#1D5C5C33; margin: 10px 8px 8px;'></div>",
            unsafe_allow_html=True
        )
        _lang = get_lang()
        options = ["Indonesia", "English"]
        idx = 0 if _lang == "id" else 1
        choice = st.selectbox(
            "Bahasa / Language",
            options,
            index=idx,
            key="global_lang_selector",
            label_visibility="collapsed"
        )
        new_lang = "id" if choice == "Indonesia" else "en"
        if new_lang != _lang:
            st.session_state.language = new_lang
            try:
                profile = db.get_profile()
                if profile:
                    db.save_profile(
                        profile.get("name", "User"),
                        profile.get("gender", "Male"),
                        profile.get("age", 25),
                        profile.get("height", 170),
                        profile.get("weight", 70),
                        new_lang
                    )
            except Exception:
                pass
            st.rerun()


# Alias lama tetap bisa dipakai supaya tidak perlu ubah semua panggilan sekaligus
def render_account_sidebar():
    render_sidebar()
