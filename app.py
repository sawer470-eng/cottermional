import streamlit as st
import yfinance as yf
import textwrap
from cot_dashboard import render_cot_dashboard
from market_data import render_market_data
from macro_data import render_macro_data
from news_feed import render_news_feed
from options_data import render_options_data
from correlation_data import render_correlation_matrix
from insider_data import render_insider_data
from tpo_data import render_tpo_data
from fair_value import render_fair_value_data
from news_impact import render_news_impact_data

st.set_page_config(page_title="Bloomberg Terminal Pro", layout="wide", page_icon="🏦")

@st.cache_data(ttl=300)
def get_tape_prices():
    tickers = {"ES=F": "S&P500", "NQ=F": "NASDAQ", "GC=F": "GOLD", "CL=F": "OIL", "BTC-USD": "BTC", "^TNX": "US10Y"}
    try:
        df = yf.download(list(tickers.keys()), period="2d", progress=False)
        items = []
        for raw_tkr, name in tickers.items():
            if 'Close' in df.columns:
                prices = df['Close'][raw_tkr].dropna()
                if len(prices) >= 2:
                    last = prices.iloc[-1]
                    prev = prices.iloc[-2]
                    chg = last - prev
                    pct = (chg/prev)*100
                    color = "#66ff00" if chg >= 0 else "#ff0033"
                    arrow = "▲" if chg >= 0 else "▼"
                    items.append(f"<span style='color:#c5c6c7'>{name}</span> <span style='color:{color}'>{last:.2f} {arrow} {abs(pct):.2f}%</span>")
        return " &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; ".join(items)
    except:
        return "S&P500 5,000 ▲ | NASDAQ 18,000 ▲ | GOLD 2,300 ▲"

# Global CSS for Bloomberg Elite look
css_style = textwrap.dedent("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Outfit:wght@500;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(0, 0, 0) 0%, rgb(11, 12, 16) 90.2%);
        font-family: 'Inter', sans-serif;
        color: #c5c6c7;
    }
    
    /* Metrics and Cards as Glassmorphism */
    .metric-card {
        background: rgba(31, 40, 51, 0.4);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(69, 162, 158, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(69, 162, 158, 0.5);
    }
    
    .metric-title {
        color: #45a29e;
        font-family: 'Outfit', sans-serif;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(69, 162, 158, 0.3);
    }
    
    /* TICKER TAPE CSS */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: rgba(11, 12, 16, 0.8);
        backdrop-filter: blur(10px);
        box-sizing: content-box;
        border-bottom: 2px solid rgba(255, 153, 0, 0.5);
        white-space: nowrap;
        padding: 8px 0;
        margin-bottom: 25px;
        position: sticky;
        top: 0;
        z-index: 999;
    }
    .ticker {
        display: inline-block;
        padding-left: 100%;
        animation: ticker 40s linear infinite;
        font-weight: 600;
        font-size: 13px;
        font-family: 'JetBrains Mono', monospace;
    }
    @keyframes ticker {
        0%   { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(11, 12, 16, 0.95) !important;
        border-right: 1px solid rgba(69, 162, 158, 0.2);
    }
    
    /* Tabs and Headers */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #ffffff, #45a29e) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
</style>
""")

st.markdown(css_style, unsafe_allow_html=True)

# Inject Ticker Tape
tape_prices = get_tape_prices()
tape_html = textwrap.dedent(f"""
<div class="ticker-wrap">
    <div class="ticker">
        {tape_prices} &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; {tape_prices} &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; {tape_prices}
    </div>
</div>
""")
st.markdown(tape_html, unsafe_allow_html=True)


st.sidebar.title("BBG TERMINAL V2")
st.sidebar.markdown("---")

# Page Routing
menu = [
    "1. SMC & COT Analysis",
    "2. Market Heatmap & Treemap",
    "3. Macro Data & Calendar",
    "4. Correlation Matrix (ELITE)",
    "5. Options Sentiment (PRO)",
    "6. Insider Tracker (ELITE)",
    "7. Volume Profile TPO (ELITE)",
    "8. Fair Value & DCF (ELITE)",
    "9. News Impact Lab (ELITE)",
    "10. Live News Feed"
]

# State Management for Navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = menu[0]

choice = st.sidebar.radio("NAVIGATION", menu, index=menu.index(st.session_state.current_page))
st.session_state.current_page = choice # Update state

if choice == "1. SMC & COT Analysis":
    render_cot_dashboard()
elif choice == "2. Market Heatmap & Treemap":
    render_market_data()
elif choice == "3. Macro Data & Calendar":
    render_macro_data()
elif choice == "4. Correlation Matrix (ELITE)":
    render_correlation_matrix()
elif choice == "5. Options Sentiment (PRO)":
    render_options_data()
elif choice == "6. Insider Tracker (ELITE)":
    render_insider_data()
elif choice == "7. Volume Profile TPO (ELITE)":
    render_tpo_data()
elif choice == "8. Fair Value & DCF (ELITE)":
    render_fair_value_data()
elif choice == "9. News Impact Lab (ELITE)":
    render_news_impact_data()
elif choice == "10. Live News Feed":
    render_news_feed()
