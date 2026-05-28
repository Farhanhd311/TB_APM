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
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; }

/* ══ SIDEBAR ══ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071E1E 0%, #0A2929 100%) !important;
    border-right: 1px solid #1D5C5C !important;
}
[data-testid="stSidebar"] * { color: #B0D8D8 !important; }
[data-testid="stSidebarNavLink"] {
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin: 2px 8px !important;
    transition: all 0.2s ease !important;
    color: #B0D8D8 !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background: rgba(0,201,167,0.12) !important;
    color: #00C9A7 !important;
}
[data-testid="stSidebarNavLink"][aria-selected="true"] {
    background: rgba(0,201,167,0.2) !important;
    color: #00C9A7 !important;
    border-left: 3px solid #00C9A7 !important;
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
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 12px 28px !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00DDB8 0%, #00C9A7 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,201,167,0.45) !important;
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
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #00C9A7 !important;
    border-bottom-color: #00C9A7 !important;
}

/* ══ CUSTOM COMPONENTS ══ */
.hero-section {
    background: linear-gradient(135deg, rgba(0,201,167,0.08) 0%, rgba(13,53,53,0.95) 100%);
    border: 1px solid rgba(0,201,167,0.3);
    border-radius: 24px;
    padding: 52px 40px;
    text-align: center;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -40%; left: -40%;
    width: 180%; height: 180%;
    background: radial-gradient(circle, rgba(0,201,167,0.06) 0%, transparent 65%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 3.8rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #00C9A7, #FFFFFF 60%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px !important;
    line-height: 1.1 !important;
}
.hero-subtitle {
    font-size: 1.35rem !important;
    color: #FFFFFF !important;
    font-weight: 500 !important;
    margin-bottom: 8px !important;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,201,167,0.15);
    border: 1px solid rgba(0,201,167,0.4);
    color: #00C9A7 !important;
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.85rem;
    font-weight: 500;
    margin: 4px;
}

.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 0.9rem;
    color: #7DCFBA;
    margin-bottom: 20px;
}

.card {
    background: linear-gradient(135deg, rgba(15,61,61,0.9), rgba(10,41,41,0.95));
    border: 1px solid #1D5C5C;
    border-radius: 18px;
    padding: 24px;
    margin: 8px 0;
    transition: all 0.3s ease;
    backdrop-filter: blur(8px);
}
.card:hover {
    border-color: rgba(0,201,167,0.5);
    box-shadow: 0 8px 32px rgba(0,201,167,0.15);
    transform: translateY(-2px);
}
.card-icon { font-size: 2rem; margin-bottom: 10px; }
.card-title { font-size: 0.85rem; color: #7DCFBA; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
.card-value { font-size: 2.4rem; font-weight: 800; color: #FFFFFF; font-family: 'Outfit', sans-serif; }
.card-unit { font-size: 1.1rem; font-weight: 500; color: #7DCFBA; }

.result-card {
    background: linear-gradient(135deg, rgba(0,201,167,0.1), rgba(13,53,53,0.95));
    border: 1px solid rgba(0,201,167,0.35);
    border-radius: 20px;
    padding: 28px;
    text-align: center;
    animation: fadeInUp 0.5s ease;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.intensity-badge {
    display: inline-block;
    border-radius: 30px;
    padding: 8px 24px;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-top: 8px;
}

.equivalent-box {
    background: rgba(0,201,167,0.08);
    border: 1px solid rgba(0,201,167,0.2);
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 1rem;
    color: #FFFFFF;
    text-align: center;
    margin: 10px 0;
}

.suggestion-box {
    background: rgba(255,209,102,0.07);
    border: 1px solid rgba(255,209,102,0.25);
    border-left: 4px solid #FFD166;
    border-radius: 0 12px 12px 0;
    padding: 10px 16px;
    font-size: 0.92rem;
    color: #E8D5A3;
    margin: 6px 0;
}

.step-card {
    background: linear-gradient(135deg, rgba(15,61,61,0.8), rgba(10,41,41,0.9));
    border: 1px solid #1D5C5C;
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    height: 100%;
    transition: all 0.3s ease;
}
.step-card:hover { border-color: #00C9A7; transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,201,167,0.15); }
.step-number { font-size: 2.5rem; font-weight: 800; color: rgba(0,201,167,0.25); font-family: 'Outfit', sans-serif; line-height: 1; }
.step-icon { font-size: 2rem; margin: 8px 0; }
.step-title { font-size: 1.05rem; font-weight: 700; color: #FFFFFF; margin: 8px 0 6px; }
.step-desc { font-size: 0.85rem; color: #7DCFBA; line-height: 1.5; }

.form-section {
    background: rgba(13,53,53,0.5);
    border: 1px solid #1D5C5C;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 16px;
}
.auth-card {
    background: linear-gradient(135deg, rgba(15,61,61,0.9), rgba(10,41,41,0.95));
    border: 1px solid #1D5C5C;
    border-radius: 20px;
    padding: 28px 24px 12px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.25);
}

.form-section-title {
    font-size: 1rem;
    font-weight: 600;
    color: #00C9A7;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.bmi-pill {
    display: inline-block;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.85rem;
    font-weight: 600;
}

.stat-card {
    background: linear-gradient(135deg, rgba(15,61,61,0.8), rgba(10,41,41,0.9));
    border: 1px solid #1D5C5C;
    border-radius: 14px;
    padding: 18px 16px;
    text-align: center;
}
.stat-value { font-size: 1.8rem; font-weight: 800; color: #00C9A7; font-family: 'Outfit', sans-serif; }
.stat-label { font-size: 0.8rem; color: #7DCFBA; font-weight: 500; margin-top: 4px; }

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #1D5C5C;
}
.empty-state .icon { font-size: 4rem; margin-bottom: 16px; }
.empty-state .text { font-size: 1.1rem; color: #2D7070; }

/* ══ PROGRESS BAR ══ */
.progress-container {
    background: rgba(13,53,53,0.5);
    border: 1px solid #1D5C5C;
    border-radius: 12px;
    padding: 20px;
    margin: 16px 0;
}
.progress-bar-bg {
    background: #1D5C5C;
    border-radius: 10px;
    height: 12px;
    width: 100%;
    overflow: hidden;
    margin-top: 8px;
}
.progress-bar-fill {
    background: linear-gradient(90deg, #00C9A7, #00DDB8);
    height: 100%;
    transition: width 0.5s ease;
}

/* ══ BADGES ══ */
.badge-card {
    background: linear-gradient(135deg, rgba(15,61,61,0.8), rgba(10,41,41,0.9));
    border: 1px solid #1D5C5C;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    height: 100%;
    transition: all 0.3s ease;
}
.badge-card.unlocked {
    border-color: #00C9A7;
    box-shadow: 0 4px 15px rgba(0,201,167,0.15);
}
.badge-card.locked {
    opacity: 0.6;
    filter: grayscale(100%);
}
.badge-emoji { font-size: 2.5rem; margin-bottom: 8px; }
.badge-title { font-size: 1rem; font-weight: 700; color: #FFFFFF; }
.badge-desc { font-size: 0.8rem; color: #7DCFBA; margin: 4px 0 8px; }
.badge-status { font-size: 0.75rem; font-weight: 600; padding: 2px 8px; border-radius: 10px; display: inline-block; }
.status-unlocked { background: rgba(0,201,167,0.2); color: #00C9A7; }
.status-locked { background: rgba(255,255,255,0.1); color: #B0D8D8; }

/* ══ PROFILE ══ */
.profile-card {
    background: linear-gradient(135deg, rgba(15,61,61,0.8), rgba(10,41,41,0.9));
    border: 1px solid #1D5C5C;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
}
.profile-avatar {
    font-size: 4rem;
    background: rgba(0,201,167,0.1);
    border-radius: 50%;
    width: 100px;
    height: 100px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    border: 2px solid #00C9A7;
}

/* ══ REMINDER ══ */
.reminder-card {
    background: rgba(239, 71, 111, 0.1);
    border-left: 4px solid #EF476F;
    border-radius: 0 12px 12px 0;
    padding: 16px;
    margin: 16px 0;
}
</style>
"""
