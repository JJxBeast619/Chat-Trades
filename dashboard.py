import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import requests

# Set up the page configuration (theme, title, and favicon)
st.set_page_config(
    page_title="GBP/JPY Live Trading Dashboard", 
    page_icon="📊", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Dropdown for theme selection
theme = st.selectbox("Select Theme", ["Light", "Dark", "Blue", "Purple"])

# Define the theme settings based on selection
if theme == "Light":
    st.markdown(
        """
        <style>
        body {
            background-color: #f7f7f7;
            color: black;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background-color: #f7f7f7;
        }
        .stText {
            color: black;
        }
        </style>
        """, unsafe_allow_html=True
    )
elif theme == "Dark":
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background-color: #121212;
        }
        .stText {
            color: white;
        }
        </style>
        """, unsafe_allow_html=True
    )
elif theme == "Blue":
    st.markdown(
        """
        <style>
        body {
            background-color: #e0f7fa;
            color: #00796b;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background-color: #e0f7fa;
        }
        .stText {
            color: #00796b;
        }
        </style>
        """, unsafe_allow_html=True
    )
elif theme == "Purple":
    st.markdown(
        """
        <style>
        body {
            background-color: #f3e5f5;
            color: #6a1b9a;
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background-color: #f3e5f5;
        }
        .stText {
            color: #6a1b9a;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Function to simulate live data (replace with real-time data integration later)
def get_fake_data():
    return pd.DataFrame({
        "Time": pd.date_range(start="2025-03-01", periods=50, freq='T'),
        "Price": [150 + i * 0.1 for i in range(50)]
    })

data = get_fake_data()

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=data["Time"], y=data["Price"], mode='lines', name='GBP/JPY Price'))
fig.update_layout(title="Live Price Chart", xaxis_title="Time", yaxis_title="Price")

# Trading Metrics and News Section
st.title("📊 GBP/JPY Live Trading Dashboard")

# Place trading metrics and news side by side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Trading Metrics")
    st.metric(label="Account Balance", value="$10,000")
    st.metric(label="Open P/L", value="$200", delta="+2%")

    st.subheader("Open Trades")
    trades = pd.DataFrame({"Trade ID": [1, 2], "Type": ["Buy", "Sell"], "Price": [150.5, 151.0], "Profit": [10, -5]})
    st.dataframe(trades)

with col2:
    st.subheader("📢 Financial News on GBP/JPY")
    def get_forex_news():
        api_key = "YOUR_NEWSAPI_KEY"  # Replace with a valid NewsAPI key
        url = f"https://newsapi.org/v2/everything?q=GBPJPY&sortBy=publishedAt&apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [(article["title"], article["url"]) for article in articles[:5]]  # Get top 5 articles
        return []

    news_articles = get_forex_news()
    if news_articles:
        for title, url in news_articles:
            st.markdown(f"- [{title}]({url})")
    else:
        st.write("No recent news found.")

# Graph for Account Value
st.subheader("Account Value Over Time")
# Simulate some account value data
account_values = [10000 + (i * 50) for i in range(50)]
account_data = pd.DataFrame({"Time": data["Time"], "Account Value": account_values})

fig_account = go.Figure()
fig_account.add_trace(go.Scatter(x=account_data["Time"], y=account_data["Account Value"], mode='lines', name='Account Value'))
fig_account.update_layout(title="Account Value Over Time", xaxis_title="Time", yaxis_title="Account Value")

st.plotly_chart(fig_account)

# Display the price chart
st.plotly_chart(fig)
