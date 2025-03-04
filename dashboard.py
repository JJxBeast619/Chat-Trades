import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# Embed Google Font in Streamlit
st.markdown("""
    <style>
        /* Preconnect to Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Baskervville:ital@0;1&display=swap');
        
        /* Apply the font to title and text */
        .title {
            font-family: 'Baskervville', serif;
            font-size: 40px;
            color: #1f77b4;
        }

        .stMetric {
            font-family: 'Baskervville', serif;
        }

        h2 {
            font-family: 'Baskervville', serif;
        }
    </style>
    """, unsafe_allow_html=True)

# Streamlit App Title with custom font
st.title("📊 GBP/JPY Live Trading Dashboard")

# Function to simulate live data
def get_fake_data():
    return pd.DataFrame({
        "Time": pd.date_range(start="2025-03-01", periods=50, freq='T'),
        "Price": [150 + i * 0.1 for i in range(50)]
    })

# Generate initial data
data = get_fake_data()

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=data["Time"], y=data["Price"], mode='lines', name='GBP/JPY Price'))
fig.update_layout(title="Live Price Chart", xaxis_title="Time", yaxis_title="Price")

st.plotly_chart(fig)

# Trading Metrics and Open Trades - Vertical arrangement
st.subheader("Trading Metrics")
st.metric(label="Account Balance", value="$10,000")
st.metric(label="Open P/L", value="$200", delta="+2%")

st.subheader("Open Trades")
trades = pd.DataFrame({"Trade ID": [1, 2], "Type": ["Buy", "Sell"], "Price": [150.5, 151.0], "Profit": [10, -5]})
st.dataframe(trades)

# Fetch Financial News from API
def get_forex_news():
    api_key = "YOUR_NEWSAPI_KEY"  # Replace with a valid NewsAPI key
    url = f"https://newsapi.org/v2/everything?q=GBPJPY&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [(article["title"], article["url"]) for article in articles[:5]]  # Get top 5 articles
    return []

# Display Financial News
st.subheader("📢 Financial News on GBP/JPY")
news_articles = get_forex_news()
if news_articles:
    for title, url in news_articles:
        st.markdown(f"- [{title}]({url})")
else:
    st.write("No recent news found.")

# Realized Profit Display with custom font
realized_profit = 500  # Replace with real profit data
profit_color = "green" if realized_profit >= 0 else "red"
st.markdown(f"<h2 style='color:{profit_color}; font-family: \"Baskervville\", serif;'>$ {realized_profit}</h2>", unsafe_allow_html=True)
