import streamlit as st
import requests
from PIL import Image
import io

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Titanic Intelligence",
    page_icon="🚢",
    layout="centered"
)

# ─── Styling ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=IM+Fell+English:ital@0;1&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Crimson Pro', Georgia, serif;
    color: #e2d9c5;
}

/* ── Animated Background ── */
@keyframes ocean-drift {
    0%   { background-position: 0% 50%;   }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%;   }
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #050e1a, #091828, #0d1f35, #061220);
    background-size: 400% 400%;
    animation: ocean-drift 20s ease infinite;
    min-height: 100vh;
}

/* Noise overlay */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
}

[data-testid="stMain"] > div { position: relative; z-index: 1; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Decorative top bar ── */
.top-bar {
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, transparent 0%, #4a90c4 30%, #c4a85a 50%, #4a90c4 70%, transparent 100%);
    margin-bottom: 0;
}

/* ── Hero ── */
.hero-wrapper {
    text-align: center;
    padding: 3rem 1rem 1.5rem;
}

.hero-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.55em;
    text-transform: uppercase;
    color: #7ab3d4;
    margin-bottom: 1.2rem;
    font-family: 'Crimson Pro', serif;
    font-weight: 600;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 6vw, 4.8rem);
    font-weight: 900;
    line-height: 1.05;
    color: #7ab3d4;
    text-shadow:
        0 0 60px rgba(74, 144, 196, 0.25),
        0 4px 16px rgba(0, 0, 0, 0.7);
    margin: 0 0 0.3rem;
    letter-spacing: -0.01em;
}

.hero-title .accent {
    color: #7ab3d4;
}

.hero-rule {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.8rem;
    margin: 1.4rem auto 1rem;
}

.hero-rule-line {
    width: 80px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #4a7a9b);
}

.hero-rule-line.right {
    background: linear-gradient(90deg, #4a7a9b, transparent);
}

.hero-rule-diamond {
    color: #c4a85a;
    font-size: 0.65rem;
}

.hero-sub {
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: 1.05rem;
    color: #a8bccc;
    letter-spacing: 0.02em;
    margin-bottom: 0;
}

/* ── Stats Row ── */
.stat-row {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 2rem 0 2.5rem;
    flex-wrap: wrap;
}

.stat-pill {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(122, 179, 212, 0.25);
    padding: 0.75rem 1.4rem;
    text-align: center;
    border-radius: 3px;
    transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease;
    backdrop-filter: blur(6px);
}

.stat-pill:hover {
    transform: translateY(-3px);
    border-color: rgba(122, 179, 212, 0.55);
    background: rgba(122, 179, 212, 0.07);
}

.stat-pill .num {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: #7ab3d4;
    display: block;
    line-height: 1.1;
}

.stat-pill .lbl {
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #8aafc8;
    display: block;
    margin-top: 0.25rem;
}

/* ── Section Label ── */
.section-label {
    font-size: 0.68rem;
    letter-spacing: 0.38em;
    text-transform: uppercase;
    color: #7ab3d4;
    margin-bottom: 0.6rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(122, 179, 212, 0.25), transparent);
}

/* ── All Streamlit Buttons (chips) ── */
div.stButton > button {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(122, 179, 212, 0.3) !important;
    color: #b8d4e8 !important;
    font-family: 'Crimson Pro', serif !important;
    font-style: italic !important;
    font-size: 0.88rem !important;
    border-radius: 100px !important;
    padding: 0.3rem 0.7rem !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
    line-height: 1.4 !important;
}

div.stButton > button:hover {
    background: rgba(122, 179, 212, 0.1) !important;
    border-color: rgba(122, 179, 212, 0.65) !important;
    color: #daeeff !important;
    box-shadow: 0 4px 18px rgba(74, 144, 196, 0.18) !important;
    transform: translateY(-1px) !important;
}

/* ── Analyze button override (full-width, last button) ── */
div[data-testid="stButton"]:has(button[kind="secondary"]):last-of-type > button,
.analyze-row div.stButton > button {
    border-radius: 3px !important;
    font-style: normal !important;
    background: linear-gradient(135deg, #1e4d7a 0%, #0f2a44 100%) !important;
    border: 1px solid #4a90c4 !important;
    color: #d8ecf8 !important;
    letter-spacing: 0.28em !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    padding: 0.8rem 2rem !important;
    text-transform: uppercase !important;
}

/* ── Text Input ── */
[data-testid="stTextInput"] input {
    background: rgba(8, 20, 36, 0.75) !important;
    border: 1px solid rgba(122, 179, 212, 0.3) !important;
    border-radius: 3px !important;
    color: #f0e8d5 !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1.1rem !important;
    padding: 0.9rem 1.2rem !important;
    caret-color: #7ab3d4 !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: rgba(122, 179, 212, 0.7) !important;
    box-shadow: 0 0 0 3px rgba(74, 144, 196, 0.1), 0 0 24px rgba(74, 144, 196, 0.12) !important;
    outline: none !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #4a6a80 !important;
    font-style: italic;
}

[data-testid="stTextInput"] label { display: none !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    color: #a8ccdf !important;
    font-family: 'IM Fell English', serif !important;
    font-style: italic !important;
    font-size: 1rem !important;
}

/* ── Answer Card ── */
.answer-card {
    background: rgba(12, 28, 48, 0.65);
    border: 1px solid rgba(122, 179, 212, 0.2);
    border-left: 4px solid #4a90c4;
    border-radius: 0 6px 6px 0;
    padding: 1.6rem 2rem;
    font-size: 1.12rem;
    line-height: 1.82;
    color: #e2d9c5;
    font-family: 'Crimson Pro', serif;
    backdrop-filter: blur(8px);
    box-shadow:
        0 12px 40px rgba(0, 0, 0, 0.45),
        inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

/* ── Image ── */
[data-testid="stImage"] {
    border: 1px solid rgba(122, 179, 212, 0.2) !important;
    border-radius: 6px !important;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.55);
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: rgba(25, 10, 10, 0.6) !important;
    border: 1px solid rgba(200, 100, 100, 0.35) !important;
    border-radius: 3px !important;
    color: #e0b0b0 !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1rem !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 3rem 1rem 2rem;
    margin-top: 4rem;
    border-top: 1px solid rgba(74, 122, 155, 0.12);
}

.footer-badges {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 1.2rem;
}

.footer-badge {
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #6a9ab5;
    border: 1px solid rgba(74, 122, 155, 0.3);
    padding: 0.22rem 0.65rem;
    border-radius: 2px;
}

.footer-coords {
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    color: #4a7090;
    margin-bottom: 0.5rem;
}

.footer-quote {
    font-family: 'IM Fell English', serif;
    font-style: italic;
    font-size: 0.88rem;
    color: #5a8099;
}
</style>
""", unsafe_allow_html=True)

# ─── Top Decorative Bar ───────────────────────────────────────────────────────
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-eyebrow">RMS Titanic · 1912 · Passenger Intelligence</div>
    <h1 class="hero-title"> <span class="accent">Titanic Intelligence</span></h1>
    <div class="hero-rule">
        <div class="hero-rule-line"></div>
        <span class="hero-rule-diamond">✦</span>
        <div class="hero-rule-line right"></div>
    </div>
    <p class="hero-sub">Uncover stories hidden within the passenger manifest</p>
</div>

""", unsafe_allow_html=True)


# ─── Main Input ───────────────────────────────────────────────────────────────
st.markdown('<div style="margin-top: 1.4rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">◈ Your Inquiry</div>', unsafe_allow_html=True)

question = st.text_input(
    "question",
    placeholder="e.g. How many survived in 1st class?",
    label_visibility="collapsed"
)

st.markdown("<div style='margin-top: 0.9rem;'></div>", unsafe_allow_html=True)

ask_clicked = st.button("⚓  Analyze Manifest", use_container_width=True)

# ─── Logic ────────────────────────────────────────────────────────────────────
if ask_clicked:
    query_to_send = question.strip() or st.session_state.query.strip()

    if not query_to_send:
        st.warning("Please enter an inquiry before setting sail.")
    else:
        with st.spinner("Deciphering the passenger records…"):
            try:
                response = requests.post(
                    "http://localhost:8000/ask",
                    json={"question": query_to_send},
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()

                st.markdown('<div style="margin-top: 2.5rem;"></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-label">◈ Telegraph Received</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="answer-card">{data.get("answer", "No data found.")}</div>',
                    unsafe_allow_html=True
                )

                if data.get("plot_available"):
                    plot_response = requests.get("http://localhost:8000/plot", timeout=30)
                    plot_response.raise_for_status()
                    image = Image.open(io.BytesIO(plot_response.content))

                    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-label">◈ Visual Evidence</div>', unsafe_allow_html=True)
                    st.image(image, use_container_width=True)

            except requests.exceptions.ConnectionError:
                st.error("⚓ Backend unreachable — is the FastAPI server running on port 8000?")
            except requests.exceptions.Timeout:
                st.error("The tide of patience ran out. Request timed out.")
            except Exception as e:
                st.error(f"The signal was lost: {e}")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-badges">
        <span class="footer-badge">FastAPI</span>
        <span class="footer-badge">LangChain</span>
        <span class="footer-badge">Gemini</span>
        <span class="footer-badge">Streamlit</span>
    </div>
    <div class="footer-coords">LAT 41°43'N · LON 49°56'W · 15 April 1912 · 02:20</div>
    <div class="footer-quote">"Nearer, My God, to Thee"</div>
</div>
""", unsafe_allow_html=True)