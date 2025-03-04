import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import requests

# Streamlit App Title
st.title("📊 GBP/JPY Live Trading Dashboard")

# Function to simulate live data (replace with real-time data integration later)
def get_fake_data():
    return pd.DataFrame({
        "Time": pd.date_range(start="2025-03-01", periods=50, freq='T'),
        "Price": [150 + i * 0.1 for i in range(50)]
    })

data = get_fake_data()

# Auto-refresh every 5 seconds (use st.experimental_rerun() to trigger a rerun)
time.sleep(5)  # Sleep for 5 seconds before rerun
st.experimental_rerun()  # Trigger a rerun of the script

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=data["Time"], y=data["Price"], mode='lines', name='GBP/JPY Price'))
fig.update_layout(title="Live Price Chart", xaxis_title="Time", yaxis_title="Price")

st.plotly_chart(fig)

# Placeholder for Trading Metrics
st.subheader("Trading Metrics")
st.metric(label="Account Balance", value="$10,000")
st.metric(label="Open P/L", value="$200", delta="+2%")

# Placeholder for Open Trades
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

# Realized Profit Display
realized_profit = 500  # Replace with real profit data
profit_color = "green" if realized_profit >= 0 else "red"
st.markdown(f"<h2 style='color:{profit_color};'>$ {realized_profit}</h2>", unsafe_allow_html=True)

# Future: Connect to MetaTrader 5 to fetch real-time trades and market data
