import base64
import html
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import streamlit as st
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Margin Manor, Decoded",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SUPABASE CONNECTION
# ============================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@st.cache_data(ttl=60)
def load_strategies():
    response = (
        supabase
        .table("strategies")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


try:
    strategies = load_strategies()
except Exception as e:
    strategies = []
    st.error("Could not connect to Supabase.")
    st.caption(str(e))


# ============================================================
# LOGO
# ============================================================

LOGO_PATH = Path("assets/margin_manor_logo.png")


def image_to_base64(path):
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()


logo_base64 = image_to_base64(LOGO_PATH)

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b0d10;
    --panel: #12161d;
    --panel-soft: #171c24;
    --border: rgba(214, 174, 94, 0.15);
    --border-soft: rgba(255, 255, 255, 0.07);
    --gold: #d6ae5e;
    --gold-soft: #f2d38b;
    --text: #f5efe6;
    --muted: #a9a29a;
    --muted2: #7f7870;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at top center, rgba(214,174,94,0.08), transparent 35%),
        linear-gradient(180deg, #0b0d10 0%, #08090b 100%);
    color: var(--text);
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hide sidebar completely */
section[data-testid="stSidebar"] {
    display: none;
}

button[kind="header"] {
    display: none;
}

/* Hide Streamlit chrome */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Header */
.site-header {
    text-align: center;
    padding: 1.2rem 0 0.8rem 0;
}

.logo-wrap {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
}

.logo-img {
    width: 155px;
    height: 155px;
    object-fit: contain;
    border-radius: 999px;
    filter: drop-shadow(0 18px 42px rgba(214,174,94,0.18));
}

.site-title {
    font-size: 3.1rem;
    font-weight: 850;
    letter-spacing: -0.07em;
    line-height: 1;
    color: var(--text);
    margin-bottom: 0.65rem;
}

.site-subtitle {
    color: var(--gold-soft);
    font-size: 1.05rem;
    font-weight: 600;
}

.site-description {
    max-width: 760px;
    margin: 1rem auto 0 auto;
    color: #cfc6b9;
    font-size: 0.95rem;
    line-height: 1.8;
    text-align: center;
}

/* Center radio nav */
div[role="radiogroup"] {
    display: flex !important;
    justify-content: center !important;
    gap: 0.8rem;
    margin-top: 1.2rem;
    margin-bottom: 2rem;
}

div[role="radiogroup"] label {
    background: rgba(18,22,29,0.96);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.55rem 1rem;
    color: var(--text) !important;
    transition: 0.15s ease;
}

div[role="radiogroup"] label:hover {
    border-color: rgba(214,174,94,0.35);
    background: rgba(214,174,94,0.07);
}

/* Hero card */
.hero-card {
    background:
        linear-gradient(135deg, rgba(18,22,29,0.98), rgba(12,14,18,0.98));
    border: 1px solid var(--border);
    border-radius: 28px;
    padding: 2rem;
    box-shadow: 0 24px 70px rgba(0,0,0,0.30);
    margin-bottom: 1.5rem;
}

.section-kicker {
    color: var(--gold);
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-weight: 800;
    margin-bottom: 0.4rem;
}

.section-title {
    color: var(--text);
    font-size: 1.7rem;
    font-weight: 820;
    letter-spacing: -0.045em;
    margin-bottom: 0.6rem;
}

.section-text {
    color: #cfc6b9;
    font-size: 0.95rem;
    line-height: 1.75;
}

/* Search */
.stTextInput input {
    background-color: rgba(18,22,29,0.96) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}

/* Clickable strategy cards */
.card-link {
    text-decoration: none !important;
    color: inherit !important;
    display: block;
}

.strategy-card {
    background:
        linear-gradient(180deg, rgba(18,22,29,0.98), rgba(12,15,20,0.98));
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.25rem;
    min-height: 250px;
    margin-bottom: 1rem;
    transition: 0.15s ease;
    cursor: pointer;
}

.strategy-card:hover {
    transform: translateY(-2px);
    border-color: rgba(214,174,94,0.40);
    background:
        linear-gradient(180deg, rgba(22,27,36,0.98), rgba(14,17,23,0.98));
}

.strategy-title {
    color: var(--text);
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.25;
    margin-bottom: 0.75rem;
}

.strategy-summary {
    color: #cfc6b9;
    font-size: 0.88rem;
    line-height: 1.6;
    margin-top: 0.8rem;
}

.open-hint {
    color: var(--gold-soft);
    font-size: 0.76rem;
    font-weight: 700;
    margin-top: 1rem;
}

.tag {
    display: inline-block;
    border: 1px solid rgba(214,174,94,0.18);
    background: rgba(214,174,94,0.06);
    color: var(--gold-soft);
    border-radius: 999px;
    padding: 0.32rem 0.55rem;
    margin-right: 0.35rem;
    margin-bottom: 0.35rem;
    font-size: 0.68rem;
    font-weight: 750;
}

/* Detail page */
.back-link {
    display: inline-block;
    color: var(--gold-soft) !important;
    text-decoration: none !important;
    border: 1px solid rgba(214,174,94,0.20);
    background: rgba(214,174,94,0.06);
    padding: 0.6rem 0.9rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 750;
    margin-bottom: 1.2rem;
}

.back-link:hover {
    border-color: rgba(214,174,94,0.40);
    background: rgba(214,174,94,0.10);
}

.strategy-detail-header {
    background:
        linear-gradient(135deg, rgba(18,22,29,0.98), rgba(12,14,18,0.98));
    border: 1px solid var(--border);
    border-radius: 28px;
    padding: 2rem;
    box-shadow: 0 24px 70px rgba(0,0,0,0.30);
    margin-bottom: 1.5rem;
}

.detail-title {
    color: var(--text);
    font-size: 2rem;
    font-weight: 850;
    letter-spacing: -0.055em;
    line-height: 1.1;
    margin-bottom: 0.9rem;
}

.detail-summary {
    color: #cfc6b9;
    font-size: 0.98rem;
    line-height: 1.75;
    margin-top: 0.9rem;
}

.detail-box {
    background: rgba(18,22,29,0.92);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}

.detail-label {
    color: var(--gold);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 800;
    margin-bottom: 0.55rem;
}

.detail-text {
    color: #d8d0c5;
    font-size: 0.92rem;
    line-height: 1.75;
    white-space: pre-line;
}

.footer-note {
    color: var(--muted2);
    text-align: center;
    font-size: 0.8rem;
    margin-top: 2rem;
}

@media (max-width: 768px) {
    .site-title {
        font-size: 2.25rem;
    }

    .logo-img {
        width: 125px;
        height: 125px;
    }

    .detail-title {
        font-size: 1.55rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def safe(value):
    if value is None:
        return ""
    return html.escape(str(value))


def render_tags(items):
    tags = ""
    for item in items:
        if item:
            tags += f"<span class='tag'>{safe(item)}</span>"
    return tags


def detail_box(label, text):
    st.markdown(
        f"""
<div class="detail-box">
    <div class="detail-label">{safe(label)}</div>
    <div class="detail-text">{safe(text) if text else "—"}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def get_query_value(name, default=None):
    value = st.query_params.get(name, default)

    if isinstance(value, list):
        return value[0] if value else default

    return value


def get_strategy_by_id(strategy_id):
    for strategy in strategies:
        if str(strategy.get("id")) == str(strategy_id):
            return strategy

    return None


def render_header():
    logo_html = ""

    if logo_base64:
        logo_html = (
            '<div class="logo-wrap">'
            f'<img class="logo-img" src="data:image/png;base64,{logo_base64}">'
            '</div>'
        )

    header_html = (
        '<div class="site-header">'
        f'{logo_html}'
        '<div class="site-title">Margin Manor, Decoded</div>'
        '<div class="site-subtitle">A Strategy Library for Price, Time & Macro</div>'
        '<div class="site-description">'
        'A personal archive of trading strategies, time-cycle models, macro frameworks, '
        'XAUUSD playbooks, SSMT logic, trade reviews, and lessons collected throughout my trading journey.'
        '</div>'
        '</div>'
    )

    st.markdown(header_html, unsafe_allow_html=True)


def render_strategy_card(strategy):
    strategy_id = quote(str(strategy.get("id", "")))

    card_html = f"""
<a class="card-link" href="?strategy_id={strategy_id}" target="_self">
    <div class="strategy-card">
        <div class="strategy-title">{safe(strategy.get("title", "Untitled Strategy"))}</div>
        {render_tags([strategy.get("category"), strategy.get("asset"), strategy.get("timeframe")])}
        <div class="strategy-summary">{safe(strategy.get("summary", ""))}</div>
        <div class="open-hint">Open full strategy →</div>
    </div>
</a>
"""

    st.markdown(card_html, unsafe_allow_html=True)


def render_strategy_detail(strategy):
    st.markdown(
        '<a class="back-link" href="?page=strategies" target="_self">← Back to Strategies Library</a>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="strategy-detail-header">
    <div class="section-kicker">Full Strategy</div>
    <div class="detail-title">{safe(strategy.get("title", "Untitled Strategy"))}</div>
    {render_tags([strategy.get("category"), strategy.get("asset"), strategy.get("timeframe")])}
    <div class="detail-summary">{safe(strategy.get("summary", ""))}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    image_url = strategy.get("image_url")

    if image_url:
        st.image(image_url, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        detail_box("Setup Rules", strategy.get("setup_rules", ""))
        detail_box("Entry Trigger", strategy.get("entry_trigger", ""))
        detail_box("Stop Loss", strategy.get("stop_loss", ""))
        detail_box("Take Profit", strategy.get("take_profit", ""))

    with c2:
        detail_box("Do Not Trade When", strategy.get("do_not_trade_when", ""))
        detail_box("Beginner Explanation", strategy.get("beginner_explanation", ""))
        detail_box("Institutional Explanation", strategy.get("institutional_explanation", ""))


# ============================================================
# DATA PREP
# ============================================================

df = pd.DataFrame(strategies) if strategies else pd.DataFrame()


# ============================================================
# HEADER
# ============================================================

render_header()


# ============================================================
# STRATEGY DETAIL PAGE
# ============================================================

selected_strategy_id = get_query_value("strategy_id")

if selected_strategy_id:
    selected_strategy = get_strategy_by_id(selected_strategy_id)

    if selected_strategy:
        render_strategy_detail(selected_strategy)
    else:
        st.warning("Strategy not found.")
        st.markdown(
            '<a class="back-link" href="?page=strategies" target="_self">← Back to Strategies Library</a>',
            unsafe_allow_html=True,
        )

    st.stop()


# ============================================================
# NAVIGATION
# ============================================================

page_param = get_query_value("page", "home")
default_page = "Strategies Library" if page_param == "strategies" else "Home"

nav_left, nav_center, nav_right = st.columns([1, 2, 1])

with nav_center:
    page = st.radio(
        "Navigation",
        ["Home", "Strategies Library"],
        index=0 if default_page == "Home" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":
    st.markdown(
        """
<div class="hero-card">
    <div class="section-kicker">Personal Trading Knowledge Base</div>
    <div class="section-title">A clean archive for every strategy, model, and lesson.</div>
    <div class="section-text">
        Margin Manor, Decoded is designed to organise everything learnt throughout a trading journey.
        The goal is simple: turn scattered notes, screenshots, concepts, and market observations into
        one structured strategy library that can be searched, reviewed, refined, and expanded over time.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# STRATEGIES LIBRARY PAGE
# ============================================================

elif page == "Strategies Library":
    st.markdown(
        """
<div class="hero-card">
    <div class="section-kicker">Strategy Database</div>
    <div class="section-title">Strategies Library</div>
    <div class="section-text">
        Browse every archived strategy in grid form. Click any card to open the full strategy page.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if not strategies:
        st.warning("No strategies found. Add strategy rows inside Supabase first.")
    else:
        search = st.text_input(
            "Search",
            placeholder="Search strategy name, summary, category, asset, setup rules...",
        )

        filtered = strategies

        if search:
            q = search.lower()
            filtered = [
                s for s in filtered
                if q in str(s.get("title", "")).lower()
                or q in str(s.get("summary", "")).lower()
                or q in str(s.get("category", "")).lower()
                or q in str(s.get("asset", "")).lower()
                or q in str(s.get("timeframe", "")).lower()
                or q in str(s.get("setup_rules", "")).lower()
                or q in str(s.get("entry_trigger", "")).lower()
            ]

        st.caption(f"Showing {len(filtered)} of {len(strategies)} strategy item(s).")

        grid = st.columns(3)

        for i, strategy in enumerate(filtered):
            with grid[i % 3]:
                render_strategy_card(strategy)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer-note">
    Margin Manor, Decoded — A Strategy Library for Price, Time & Macro<br>
    Educational and journaling purposes only. Not financial advice.
</div>
""",
    unsafe_allow_html=True,
)