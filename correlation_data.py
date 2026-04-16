import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

def render_correlation_matrix():
    st.markdown("<h2 style='color: #FF9900; font-family: monospace; border-bottom: 1px solid #30363d; padding-bottom:10px;'>[ASSET CORRELATION MATRIX]</h2>", unsafe_allow_html=True)
    st.write("Cross-Asset Correlation Heatmap (Trailing 90 Days)")

    tickers_dict = {
        "DXY Index": "DX-Y.NYB",
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "GER 40": "^GDAXI",
        "S&P 500": "SPY",
        "Nasdaq": "QQQ",
        "Gold": "GLD",
        "Crude Oil": "USO",
        "Treasuries": "TLT",
        "Bitcoin": "BTC-USD"
    }
    
    tickers = list(tickers_dict.values())
    
    with st.spinner("Calculating full correlation matrix..."):
        try:
            df = yf.download(tickers, period="3mo", progress=False)
            
            if df.empty or 'Close' not in df:
                st.error("Failed to download correlation data. Financial markets might be closed or API limits reached.")
                return
                
            close_prices = df['Close']
            
            # Map column names to readable names
            close_prices = close_prices.rename(columns={v: k for k, v in tickers_dict.items()})
            
            # Calculate daily percentage returns
            returns = close_prices.pct_change().dropna()
            
            # Calculate Pearson correlation matrix
            corr = returns.corr()
            
            # Plot Heatmap
            fig = px.imshow(
                corr,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale=[[0, '#ff0033'], [0.5, '#161b22'], [1, '#66ff00']],
                zmin=-1, zmax=1
            )
            
            fig.update_layout(
                height=600,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#8b949e', family="monospace"),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### Precision Correlation Table")
            st.dataframe(corr.style.background_gradient(cmap='RdYlGn', axis=None).format("{:.4f}"), use_container_width=True)
            
            st.markdown(
                "<div style='font-size:12px; color:#8b949e; margin-top:20px;'>"
                "<b>Institutional Insight:</b> Trading EURUSD often requires tracking its inverse correlation with the DXY. "
                "The GER 40 (DAX) is highly sensitive to Euro strength and US Index (SPY) sentiment. "
                "Smart Money uses these 'Intermarket' links to confirm trends."
                "</div>", unsafe_allow_html=True
            )
                
        except Exception as e:
            st.error(f"Error computing matrix: {e}")
