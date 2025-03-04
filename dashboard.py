import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# Embed Google Font in Streamlit
st.markdown("""
    <style>
        /* Apply the Google font Baskervville */
        @import url('https://fonts.googleapis.com/css2?family=Baskervville:ital@0;1&display=swap');
        
        body {
            font-family: 'Baskervville', serif;
        }
    </style>
    """, unsafe_allow_html=True)

# Streamlit App Title with custom font
st.title("📊 GBP/JPY Live Trading Dashboard")

# Function to simulate live data for GBP/JPY price
def get_fake_data():
    return pd.DataFrame({
        "Time": pd.date_range(start="2025-03-01", periods=50, freq='T'),
        "Price": [150 + i * 0.1 for i in range(50)]
    })

# Generate initial data for GBP/JPY
data = get_fake_data()

# Account value data for the line graph (simulating account value change over time)
account_value_data = pd.DataFrame({
    "Time": pd.date_range(start="2025-03-01", periods=50, freq='T'),
    "Account Value": [10000 + i * 10 for i in range(50)]  # Simulating account value growth
})

# Plotly Chart for GBP/JPY price
fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=data["Time"], y=data["Price"], mode='lines', name='GBP/JPY Price'))
fig_price.update_layout(title="Live Price Chart", xaxis_title="Time", yaxis_title="Price")

# Plotly Chart for Account Value over time
fig_account_value = go.Figure()
fig_account_value.add_trace(go.Scatter(x=account_value_data["Time"], y=account_value_data["Account Value"], mode='lines', name='Account Value'))
fig_account_value.update_layout(title="Account Value Over Time", xaxis_title="Time", yaxis_title="Account Value ($)")

# Layout: Trading Metrics and Financial News side by side
col1, col2 = st.columns([2, 3])  # Adjust columns width as needed

with col1:
    # Trading Metrics
    st.subheader("Trading Metrics")
    st.metric(label="Account Balance", value="$10,000")
    st.metric(label="Open P/L", value="$200", delta="+2%")

with col2:
    # Financial News
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

# Display the charts
st.plotly_chart(fig_price)  # Display the price chart
st.plotly_chart(fig_account_value)  # Display the account value chart
