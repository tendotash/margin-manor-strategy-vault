import streamlit as st
from supabase import create_client
import pandas as pd

st.set_page_config(
    page_title="Margin Manor Strategy Vault",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# CONNECT TO SUPABASE
# -----------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# LOAD STRATEGIES
# -----------------------------
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

strategies = load_strategies()

# -----------------------------
# DESIGN
# -----------------------------
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }

    h1, h2, h3 {
        color: #f5c542;
    }

    .strategy-card {
        background-color: #161b22;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }

    .tag {
        display: inline-block;
        background-color: #21262d;
        color: #f5c542;
        padding: 4px 10px;
        border-radius: 20px;
        margin-right: 6px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📚 Margin Manor")
page = st.sidebar.radio(
    "Choose section",
    [
        "Home",
        "Strategy Library",
        "XAUUSD Playbook",
        "SSMT Models",
        "Time Cycle Models",
        "Macro Notes",
        "Mistake Library"
    ]
)

# -----------------------------
# HOME
# -----------------------------
if page == "Home":
    st.title("📈 Margin Manor Strategy Vault")
    st.subheader("My personal trading strategy library.")

    st.write("""
    This website compiles the trading strategies, market models, SSMT logic,
    time cycle concepts, macro notes, and trading mistakes I have learnt.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Strategies", len(strategies))

    with col2:
        categories = [s.get("category") for s in strategies if s.get("category")]
        st.metric("Categories", len(set(categories)))

    with col3:
        assets = [s.get("asset") for s in strategies if s.get("asset")]
        st.metric("Assets Covered", len(set(assets)))

    st.divider()

    st.header("How to use this vault")
    st.write("""
    Use this as a trading playbook. Each strategy should explain:
    
    1. What the setup is
    2. When it works best
    3. What confirms the entry
    4. Where the stop loss goes
    5. Where take profit goes
    6. When not to trade
    """)

# -----------------------------
# STRATEGY LIBRARY
# -----------------------------
elif page == "Strategy Library":
    st.title("📚 Strategy Library")

    if not strategies:
        st.warning("No strategies found. Add a strategy inside Supabase first.")
    else:
        df = pd.DataFrame(strategies)

        categories = sorted(df["category"].dropna().unique()) if "category" in df else []
        selected_category = st.selectbox("Filter by category", ["All"] + list(categories))

        search = st.text_input("Search strategy")

        filtered = strategies

        if selected_category != "All":
            filtered = [s for s in filtered if s.get("category") == selected_category]

        if search:
            filtered = [
                s for s in filtered
                if search.lower() in str(s.get("title", "")).lower()
                or search.lower() in str(s.get("summary", "")).lower()
                or search.lower() in str(s.get("category", "")).lower()
            ]

        st.write(f"Showing **{len(filtered)}** strategy post(s).")

        for s in filtered:
            st.markdown("<div class='strategy-card'>", unsafe_allow_html=True)

            st.subheader(s.get("title", "Untitled Strategy"))

            tags = []
            if s.get("category"):
                tags.append(s.get("category"))
            if s.get("asset"):
                tags.append(s.get("asset"))
            if s.get("timeframe"):
                tags.append(s.get("timeframe"))

            tag_html = "".join([f"<span class='tag'>{tag}</span>" for tag in tags])
            st.markdown(tag_html, unsafe_allow_html=True)

            st.write("")
            st.write(s.get("summary", ""))

            with st.expander("Open full strategy"):
                st.markdown("### Setup Rules")
                st.write(s.get("setup_rules", "—"))

                st.markdown("### Entry Trigger")
                st.write(s.get("entry_trigger", "—"))

                st.markdown("### Stop Loss")
                st.write(s.get("stop_loss", "—"))

                st.markdown("### Take Profit")
                st.write(s.get("take_profit", "—"))

                st.markdown("### Do Not Trade When")
                st.write(s.get("do_not_trade_when", "—"))

                st.markdown("### Beginner Explanation")
                st.write(s.get("beginner_explanation", "—"))

                st.markdown("### Institutional Explanation")
                st.write(s.get("institutional_explanation", "—"))

            st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# OTHER PAGES
# -----------------------------
elif page == "XAUUSD Playbook":
    st.title("🟡 XAUUSD Playbook")
    st.write("""
    This section is for gold-specific knowledge:
    
    - DXY
    - US yields
    - Fed expectations
    - VIX
    - Oil
    - Safe-haven flows
    - Red-folder news reactions
    """)

elif page == "SSMT Models":
    st.title("🔀 SSMT Models")
    st.write("""
    This section is for:
    
    - Aggressive vs defensive assets
    - XAUUSD vs XAUEUR vs XAUGBP vs XAGUSD
    - High/low alignment
    - Sweep logic
    - When SSMT is valid
    - When SSMT has resolved
    """)

elif page == "Time Cycle Models":
    st.title("⏰ Time Cycle Models")
    st.write("""
    This section is for:
    
    - Asia cycle
    - London cycle
    - NY AM cycle
    - NY PM cycle
    - Daily cycle
    - Interdaily cycle
    - Quarters
    """)

elif page == "Macro Notes":
    st.title("🌍 Macro Notes")
    st.write("""
    This section is for macro and fundamental notes:
    
    - Inflation
    - Jobs data
    - Fed speeches
    - Interest rates
    - Bonds and yields
    - Risk-on / risk-off
    - Tailwinds and headwinds
    """)

elif page == "Mistake Library":
    st.title("❌ Mistake Library")
    st.write("""
    This section is for repeated trading mistakes:
    
    - Entering during mixed/wait verdict
    - Ignoring macro headwind
    - Trading without confirmation
    - Entering too early
    - Holding through high-impact news
    - Moving stop loss emotionally
    """)

st.divider()
st.caption(
    "Disclaimer: This website is for educational and journaling purposes only. "
    "It is not financial advice. Trading involves risk."
)