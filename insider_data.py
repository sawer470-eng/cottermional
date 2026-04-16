import streamlit as st
import yfinance as yf
import pandas as pd

def render_insider_data():
    st.markdown("<h2 style='color: #FF9900; font-family: monospace; border-bottom: 1px solid #30363d; padding-bottom:10px;'>[INSIDER TRADING TRACKER]</h2>", unsafe_allow_html=True)
    st.write("Track when CEOs, CFOs, and Directors buy or sell their own company's stock.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        ticker = st.text_input("Enter Ticker Symbol (e.g. AAPL, TSLA, NVDA):", "AAPL").upper()
    
    with st.spinner(f"Scanning SEC filings for {ticker}..."):
        try:
            asset = yf.Ticker(ticker)
            df = asset.insider_transactions
            
            if df is None or df.empty:
                st.warning(f"No recent insider transactions found for {ticker}.")
                return
                
            # Clean and format data
            display_df = df.copy()
            st.markdown(f"#### Recent Transactions for {ticker}")
            
            # Stylize the dataframe
            def highlight_transaction(row):
                color = '#ff0033' if 'Sale' in str(row['Transaction']) else '#66ff00' if 'Buy' in str(row['Transaction']) or 'Grant' in str(row['Transaction']) else '#8b949e'
                return [f'color: {color}'] * len(row)
                
            # Filter columns we want
            cols_to_show = ['Start Date', 'Insider', 'Position', 'Transaction', 'Shares', 'Value']
            # Ensure columns exist
            cols_to_show = [c for c in cols_to_show if c in display_df.columns]
            
            st.dataframe(
                display_df[cols_to_show].style.apply(highlight_transaction, axis=1),
                hide_index=True,
                use_container_width=True,
                height=500
            )
            
            st.markdown(
                "<div style='font-size:12px; color:#8b949e;'>"
                "<b>Note:</b> 'Sale' (Red) indicates selling shares. 'Buy' or 'Grant' (Green) indicates acquiring shares. "
                "Smart money often tracks clustering of C-level buys as a signal of undervalued stock."
                "</div>", unsafe_allow_html=True
            )
            
        except Exception as e:
            st.error(f"Error fetching insider data: {e}")
