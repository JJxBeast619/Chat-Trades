import MetaTrader5 as mt5
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# Ensure `st.set_page_config` is the FIRST Streamlit command
st.set_page_config(
    page_title="GBP/JPY Live Trading Dashboard", 
    page_icon="📊", 
    layout="wide"
)

# Add Baskerville font from Google Fonts
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Baskervville&display=swap');
        html, body, [class*="css"] {
            font-family: 'Baskervville', serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize MT5 and check the connection
if not mt5.initialize():
    st.error("Failed to initialize MetaTrader 5. Please check the connection.")
else:
    st.write("Connected to MetaTrader 5 successfully!")

# Function to get live data from MetaTrader 5 for GBP/JPY
def get_live_data():
    # Get last 50 data points (replace with any number or range of data you need)
    rates = mt5.copy_rates_from_pos("GBPJPY", mt5.TIMEFRAME_M1, 0, 50)
    # Convert to pandas DataFrame
    rates_frame = pd.DataFrame(rates)
    # Convert timestamps to datetime
    rates_frame['Time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame

# Fetch live data from MT5
data = get_live_data()

# Layout: Trading Metrics and News Side by Side
st.title("📊 GBP/JPY Live Trading Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Trading Metrics")
    st.metric(label="Account Balance", value="$10,000")
    st.metric(label="Open P/L", value="$200", delta="+2%")

with col2:
    st.subheader("📢 Financial News on GBP/JPY")
    def get_forex_news():
        api_key = "YOUR_NEWSAPI_KEY"  # Replace with your valid NewsAPI key
        url = f"https://newsapi.org/v2/everything?q=GBPJPY&sortBy=publishedAt&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [(article["title"], article["url"]) for article in articles[:5]]
        return []

    news_articles = get_forex_news()
    if news_articles:
        for title, url in news_articles:
            st.markdown(f"- [{title}]({url})")
    else:
        st.write("No recent news found.")

# Live Open Trades Table
st.subheader("Live Open Trades")
trades = pd.DataFrame({"Trade ID": [1, 2], "Type": ["Buy", "Sell"], "Price": [150.5, 151.0], "Profit": [10, -5]})
st.dataframe(trades)

# Account Value Over Time Graph (Simulated)
st.subheader("Account Value Over Time")
account_values = [10000 + (i * 50) for i in range(50)]
account_data = pd.DataFrame({"Time": data["Time"], "Account Value": account_values})

fig_account = go.Figure()
fig_account.add_trace(go.Scatter(x=account_data["Time"], y=account_data["Account Value"], mode='lines', name='Account Value'))
fig_account.update_layout(title="Account Value Over Time", xaxis_title="Time", yaxis_title="Account Value")

st.plotly_chart(fig_account)

# Display Price Chart
st.subheader("Live GBP/JPY Price Chart")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data["Time"], y=data["close"], mode='lines', name='GBP/JPY Price'))
fig.update_layout(xaxis_title="Time", yaxis_title="Price")
st.plotly_chart(fig)

# Make sure to shut down MT5 after you finish
mt5.shutdown()
