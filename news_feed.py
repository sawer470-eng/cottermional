import streamlit as st
import feedparser
import textwrap

def render_news_feed():
    st.markdown(textwrap.dedent("""
        <h2 style='color: #FF9900; font-family: monospace; border-bottom: 1px solid #30363d; padding-bottom:10px;'>
            [LIVE NEWS FEED & INTELLIGENCE]
        </h2>
    """), unsafe_allow_html=True)
    
    # Example RSS feeds
    rss_urls = [
        ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
        ("Wall Street Journal", "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"),
    ]
    
    c1, c2 = st.columns([1, 2])
    with c1:
        selected_feed = st.radio("Select Source", [n for n, u in rss_urls], horizontal=True)
    
    feed_url = next(u for n, u in rss_urls if n == selected_feed)
    
    with st.spinner("Fetching Live Market Intelligence..."):
        try:
            feed = feedparser.parse(feed_url)
        except:
            st.error("Network error: Could not reach news server.")
            return
            
    if not feed.entries:
        st.error("Could not load news feed entries.")
        return
        
    st.markdown("---")
    
    for entry in feed.entries[:15]:
        published = entry.get('published', 'No Date')
        title = entry.get('title', 'No Title')
        summary = entry.get('summary', '')
        link = entry.get('link', '#')
        
        with st.expander(f"📰 {title}"):
            st.markdown(textwrap.dedent(f"""
                <div style="font-family: 'Inter', sans-serif;">
                    <div style="color: #45a29e; font-size: 11px; margin-bottom: 5px;">Published: {published}</div>
                    <p style="color: #c5c6c7; font-size: 14px;">{summary[:300]}...</p>
                    <a href="{link}" target="_blank" style="color: #FF9900; font-size: 13px; text-decoration: none;">[Read Full Article]</a>
                </div>
            """), unsafe_allow_html=True)
            
            st.write("") # Spacer
            # Analyze Impact Button
            # We use the link as a unique key
            if st.button(f"🔍 ANALYZE 5Y IMPACT: {title[:20]}...", key=link[:100]):
                st.session_state.selected_news_event = title
                st.session_state.current_page = "9. News Impact Lab (ELITE)"
                st.rerun()
