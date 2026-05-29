def get_custom_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

/* ══ BASE ══ */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #0A2929 !important;
}
.stApp {
    background: linear-gradient(160deg, #071E1E 0%, #0A2929 40%, #0D3535 100%) !important;
    min-height: 100vh;
}

/* ══ HIDE STREAMLIT DEFAULTS ══ */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; }

/* ══ HIDE STREAMLIT AUTO-NAV (kita pakai sidebar custom) ══ */
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebarNavItems"] { display: none !important; }
[data-testid="stSidebarNavSeparator"] { display: none !important; }

/* ══ SIDEBAR ══ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071E1E 0%, #071E1E 100%) !important;
    border-right: 1px solid #142F2F !important;
}
[data-testid="stSidebar"] * { color: #B0D8D8 !important; }

/* Sidebar nav links — page_link styling */
[data-testid="stSidebar"] [data-testid="stPageLink"] a,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
    border-radius: 8px !important;
    padding: 8px 10px !important;
    margin: 1px 0 !important;
    transition: all 0.15s ease !important;
    color: #8ABABA !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    text-decoration: none !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
    background: rgba(0,201,167,0.1) !important;
    color: #00C9A7 !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"] {
    background: rgba(0,201,167,0.15) !important;
    color: #00C9A7 !important;
    border-left: 3px solid #00C9A7 !important;
}

/* Sidebar selectbox styling */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(10,41,41,0.8) !important;
    border: 1px solid #1D5C5C !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}

/* Sidebar button */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(29,92,92,0.4) !important;
    border: 1px solid #1D5C5C !important;
    color: #B0D8D8 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 6px 12px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(239,71,111,0.15) !important;
    border-color: rgba(239,71,111,0.4) !important;
    color: #EF476F !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ══ TEXT ══ */
h1, h2, h3, h4 { font-family: 'Outfit', sans-serif !important; color: #FFFFFF !important; }
p, span, label, .stMarkdown { color: #B0D8D8 !important; }

/* ══ METRICS ══ */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(15,61,61,0.85), rgba(10,41,41,0.95)) !important;
    border: 1px solid #1D5C5C !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: #00C9A7 !important;
    box-shadow: 0 6px 24px rgba(0,201,167,0.18) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricValue"] { color: #00C9A7 !important; font-size: 1.7rem !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #B0D8D8 !important; font-weight: 500 !important; }
[data-testid="stMetricDelta"] { color: #7DCFBA !important; }

/* ══ BUTTONS ══ */
.stButton > button {
    background: linear-gradient(135deg, #00C9A7 0%, #009E82 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 10px 24px !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00DDB8 0%, #00C9A7 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0,201,167,0.35) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ══ SLIDERS ══ */
[data-testid="stSlider"] .st-bk { background: #1D5C5C !important; }
[data-testid="stSlider"] .st-bo { background: #00C9A7 !important; }
[data-testid="stSlider"] .st-br { background: #00C9A7 !important; }
.stSlider [data-testid="stThumbValue"] { color: #00C9A7 !important; }

/* ══ RADIO ══ */
[data-testid="stRadio"] label { color: #B0D8D8 !important; }
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p { color: #B0D8D8 !important; }

/* ══ SELECT / INPUT ══ */
.stSelectbox > div > div {
    background: rgba(13,53,53,0.8) !important;
    border: 1px solid #1D5C5C !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
}
.stTextInput input, .stNumberInput input {
    background: rgba(13,53,53,0.8) !important;
    border: 1px solid #1D5C5C !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
}

/* ══ DATAFRAME ══ */
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; }
[data-testid="stDataFrame"] th {
    background: rgba(0,201,167,0.15) !important;
    color: #00C9A7 !important;
    font-weight: 600 !important;
}
[data-testid="stDataFrame"] td { color: #B0D8D8 !important; }

/* ══ DIVIDER ══ */
hr { border-color: #1D5C5C !important; margin: 24px 0 !important; }

/* ══ EXPANDER ══ */
[data-testid="stExpander"] {
    background: rgba(13,53,53,0.5) !important;
    border: 1px solid #1D5C5C !important;
    border-radius: 12px !important;
}

/* ══ TABS ══ */
[data-testid="stTabs"] [role="tab"] {
    color: #B0D8D8 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #00C9A7 !important;
    border-bottom-color: #00C9A7 !important;
}

/* ══ HERO SECTION ══ */
.hero-section {
    background: linear-gradient(135deg, rgba(0,201,167,0.06) 0%, rgba(7,30,30,0.98) 100%);
    border: 1px solid rgba(0,201,167,0.2);
    border-radius: 20px;
    padding: 44px 40px;
    text-align: center;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 50% 40%, rgba(0,201,167,0.05) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #00C9A7, #FFFFFF 60%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px !important;
    line-height: 1.1 !important;
}
.hero-subtitle {
    font-size: 1.1rem !important;
    color: #7DCFBA !important;
    font-weight: 400 !important;
    margin-bottom: 20px !important;
    max-width: 540px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,201,167,0.1);
    border: 1px solid rgba(0,201,167,0.25);
    color: #7DCFBA !important;
    border-radius: 6px;
    padding: 3px 12px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 3px;
    letter-spacing: 0.2px;
}

/* ══ PAGE HEADER ══ */
.page-header {
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #1D5C5C33;
}
.page-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 0.875rem;
    color: #4D9E8F;
    font-weight: 400;
}

/* ══ SECTION TITLE (legacy) ══ */
.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 0.875rem;
    color: #4D9E8F;
    margin-bottom: 20px;
}

/* ══ CARD ══ */
.card {
    background: linear-gradient(135deg, rgba(15,61,61,0.9), rgba(10,41,41,0.95));
    border: 1px solid #1D5C5C;
    border-radius: 14px;
    padding: 20px;
    margin: 8px 0;
    transition: all 0.25s ease;
    backdrop-filter: blur(8px);
}
.card:hover {
    border-color: rgba(0,201,167,0.4);
    box-shadow: 0 6px 24px rgba(0,201,167,0.12);
    transform: translateY(-2px);
}
.card-icon { font-size: 1.6rem; margin-bottom: 8px; }
.card-title { font-size: 0.78rem; color: #4D9E8F; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.card-value { font-size: 2rem; font-weight: 800; color: #FFFFFF; font-family: 'Outfit', sans-serif; }
.card-unit { font-size: 0.95rem; font-weight: 500; color: #7DCFBA; }

/* ══ RESULT CARD ══ */
.result-card {
    background: linear-gradient(135deg, rgba(0,201,167,0.08), rgba(7,30,30,0.98));
    border: 1px solid rgba(0,201,167,0.25);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    animation: fadeInUp 0.4s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ══ INTENSITY BADGE ══ */
.intensity-badge {
    display: inline-block;
    border-radius: 6px;
    padding: 5px 18px;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    margin-top: 8px;
}

/* ══ EQUIVALENT BOX ══ */
.equivalent-box {
    background: rgba(0,201,167,0.06);
    border: 1px solid rgba(0,201,167,0.15);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.9rem;
    color: #B0D8D8;
    text-align: center;
    margin: 8px 0;
}

/* ══ SUGGESTION BOX ══ */
.suggestion-box {
    background: rgba(255,209,102,0.06);
    border: 1px solid rgba(255,209,102,0.2);
    border-left: 3px solid #FFD166;
    border-radius: 0 10px 10px 0;
    padding: 10px 14px;
    font-size: 0.875rem;
    color: #D4C08A;
    margin: 5px 0;
    line-height: 1.5;
}

/* ══ STEP CARD ══ */
.step-card {
    background: rgba(13,53,53,0.5);
    border: 1px solid #1D5C5C;
    border-radius: 14px;
    padding: 24px 18px;
    text-align: center;
    height: 100%;
    transition: all 0.25s ease;
}
.step-card:hover { border-color: rgba(0,201,167,0.4); transform: translateY(-3px); }
.step-number { font-size: 2rem; font-weight: 800; color: rgba(0,201,167,0.2); font-family: 'Outfit', sans-serif; line-height: 1; }
.step-title { font-size: 1rem; font-weight: 700; color: #FFFFFF; margin: 10px 0 6px; }
.step-desc { font-size: 0.82rem; color: #4D9E8F; line-height: 1.55; }

/* ══ FORM SECTION ══ */
.form-section {
    background: transparent;
    border: none;
    padding: 10px 0;
    margin-bottom: 16px;
}
.auth-card {
    background: linear-gradient(135deg, rgba(15,61,61,0.9), rgba(10,41,41,0.95));
    border: 1px solid #1D5C5C;
    border-radius: 18px;
    padding: 28px 24px 12px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.25);
}

.form-section-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #00C9A7;
    margin-bottom: 18px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0, 201, 167, 0.2);
    letter-spacing: 0.3px;
}

/* ══ BMI PILL ══ */
.bmi-pill {
    display: inline-block;
    border-radius: 5px;
    padding: 2px 10px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ══ STAT CARD ══ */
.stat-card {
    background: linear-gradient(135deg, rgba(15,61,61,0.8), rgba(10,41,41,0.9));
    border: 1px solid #1D5C5C;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    transition: border-color 0.2s ease;
}
.stat-card:hover { border-color: rgba(0,201,167,0.35); }
.stat-value { font-size: 1.7rem; font-weight: 800; color: #00C9A7; font-family: 'Outfit', sans-serif; }
.stat-label { font-size: 0.78rem; color: #4D9E8F; font-weight: 500; margin-top: 4px; }

/* ══ EMPTY STATE ══ */
.empty-state {
    text-align: center;
    padding: 56px 20px;
    color: #1D5C5C;
}
.empty-state .icon { font-size: 3rem; margin-bottom: 14px; opacity: 0.6; }
.empty-state .text { font-size: 1rem; color: #2D7070; line-height: 1.6; }

/* ══ PROGRESS BAR ══ */
.progress-container {
    background: rgba(10,41,41,0.6);
    border: 1px solid #1D5C5C;
    border-radius: 14px;
    padding: 20px;
    margin: 14px 0;
}
.progress-bar-bg {
    background: #142F2F;
    border-radius: 8px;
    height: 10px;
    width: 100%;
    overflow: hidden;
    margin-top: 10px;
}
.progress-bar-fill {
    background: linear-gradient(90deg, #00C9A7, #00DDB8);
    height: 100%;
    transition: width 0.6s ease;
    border-radius: 8px;
}

/* ══ BADGES ══ */
.badge-card {
    background: rgba(10,41,41,0.7);
    border: 1px solid #1D5C5C;
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    height: 100%;
    transition: all 0.25s ease;
}
.badge-card.unlocked {
    border-color: rgba(0,201,167,0.4);
    box-shadow: 0 3px 12px rgba(0,201,167,0.1);
}
.badge-card.locked {
    opacity: 0.5;
    filter: grayscale(80%);
}
.badge-emoji { font-size: 2.2rem; margin-bottom: 8px; }
.badge-title { font-size: 0.95rem; font-weight: 700; color: #FFFFFF; }
.badge-desc { font-size: 0.78rem; color: #4D9E8F; margin: 4px 0 8px; line-height: 1.4; }
.badge-status { font-size: 0.72rem; font-weight: 600; padding: 2px 8px; border-radius: 5px; display: inline-block; }
.status-unlocked { background: rgba(0,201,167,0.15); color: #00C9A7; }
.status-locked { background: rgba(255,255,255,0.07); color: #4D9E8F; }

/* ══ PROFILE ══ */
.profile-card {
    background: rgba(10,41,41,0.7);
    border: 1px solid #1D5C5C;
    border-radius: 14px;
    padding: 24px;
    text-align: center;
}
.profile-avatar {
    font-size: 3.5rem;
    background: rgba(0,201,167,0.08);
    border-radius: 50%;
    width: 88px;
    height: 88px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 14px;
    border: 2px solid rgba(0,201,167,0.3);
}

/* ══ REMINDER ══ */
.reminder-card {
    background: rgba(239,71,111,0.08);
    border-left: 3px solid #EF476F;
    border-radius: 0 10px 10px 0;
    padding: 14px 16px;
    margin: 14px 0;
}
</style>
"""
