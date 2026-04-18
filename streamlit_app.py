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
from smc_scanner import render_smc_scanner
from ai_intelligence import render_ai_intelligence
from watchlists import render_watchlists
from liquidity_data import render_liquidity_data

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

css_style = textwrap.dedent("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Outfit:wght@500;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(0, 0, 0) 0%, rgb(11, 12, 16) 90.2%);
        font-family: 'Inter', sans-serif;
        color: #c5c6c7;
    }
    .metric-card {
        background: rgba(31, 40, 51, 0.4);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(69, 162, 158, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
    .ticker-wrap {
        width: 100%; overflow: hidden; background: rgba(11, 12, 16, 0.8); backdrop-filter: blur(10px);
        border-bottom: 2px solid rgba(255, 153, 0, 0.5); padding: 8px 0; margin-bottom: 25px;
        position: sticky; top: 0; z-index: 999;
    }
    .ticker {
        display: inline-block; padding-left: 100%; animation: ticker 40s linear infinite;
        font-weight: 600; font-size: 13px; font-family: 'JetBrains Mono', monospace;
    }
    @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
</style>
""")
st.markdown(css_style, unsafe_allow_html=True)

tape_prices = get_tape_prices()
st.markdown(f'<div class="ticker-wrap"><div class="ticker">{tape_prices} &nbsp;|&nbsp; {tape_prices}</div></div>', unsafe_allow_html=True)

st.sidebar.title("BBG TERMINAL V3")
menu = [
    "1. SMC & COT Analysis", "2. Market Heatmap", "3. Macro Data", "4. Correlation Matrix", 
    "5. Options Sentiment", "6. Insider Tracker", "7. Volume Profile TPO", "8. Fair Value & DCF", 
    "9. SMC Scanner (ELITE)", "10. Liquidity & Footprint", "11. AI Intelligence Lab", 
    "12. News Impact Lab", "13. Live News Feed", "14. Custom Watchlists"
]
choice = st.sidebar.radio("NAVIGATION", menu)

if choice == "1. SMC & COT Analysis": render_cot_dashboard()
elif choice == "2. Market Heatmap": render_market_data()
elif choice == "3. Macro Data": render_macro_data()
elif choice == "4. Correlation Matrix": render_correlation_matrix()
elif choice == "5. Options Sentiment": render_options_data()
elif choice == "6. Insider Tracker": render_insider_data()
elif choice == "7. Volume Profile TPO": render_tpo_data()
elif choice == "8. Fair Value & DCF": render_fair_value_data()
elif choice == "9. SMC Scanner (ELITE)": render_smc_scanner()
elif choice == "10. Liquidity & Footprint": render_liquidity_data()
elif choice == "11. AI Intelligence Lab": render_ai_intelligence()
elif choice == "12. News Impact Lab": render_news_impact_data()
elif choice == "13. Live News Feed": render_news_feed()
elif choice == "14. Custom Watchlists": render_watchlists()
