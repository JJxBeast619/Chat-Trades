import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import MetaTrader5 as mt5
import time

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

# Initialize MetaTrader 5
if not mt5.initialize():
    st.error("Failed to initialize MetaTrader 5 connection!")
    st.stop()

# Get live data from MetaTrader 5
def get_live_data(symbol="GBPJPY", timeframe=mt5.TIMEFRAME_M1, n=50):
    # Get the last 'n' 1-minute bars
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    
    # If no data is returned, return an empty DataFrame
    if rates is None:
        return pd.DataFrame()
    
    # Convert the data into a DataFrame
    rates_df = pd.DataFrame(rates)
    
    # Convert time to a datetime format
    rates_df['time'] = pd.to_datetime(rates_df['time'], unit='s')
    return rates_df[['time', 'close']]

# Get live data
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
        api_key = "YOUR_NEWSAPI_KEY"
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

# Account Value Over Time Graph
st.subheader("Account Value Over Time")
account_values = [10000 + (i * 50) for i in range(len(data))]
account_data = pd.DataFrame({"Time": data["time"], "Account Value": account_values})

fig_account = go.Figure()
fig_account.add_trace(go.Scatter(x=account_data["Time"], y=account_data["Account Value"], mode='lines', name='Account Value'))
fig_account.update_layout(title="Account Value Over Time", xaxis_title="Time", yaxis_title="Account Value")

st.plotly_chart(fig_account)

# Display Price Chart
st.subheader("Live GBP/JPY Price Chart")
fig = go.Figure()
fig.add_trace(go.Scatter(x=data["time"], y=data["close"], mode='lines', name='GBP/JPY Price'))
fig.update_layout(xaxis_title="Time", yaxis_title="Price")
st.plotly_chart(fig)

# Shut down the MT5 connection after usage
mt5.shutdown()
