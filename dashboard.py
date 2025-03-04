import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# Color themes (CSS styles) with full background update
themes = {
    "Classic Blue": """
        <style>
            body { background-color: #f0f4f8; color: #1e3d58; }
            .stButton>button { background-color: #007bff; color: white; }
            .stMetric>div { background-color: #007bff; color: white; }
            .stMarkdown { color: #007bff; }
            .stSidebar { background-color: #003366; color: white; }
            .css-1d391kg { background-color: #f0f4f8; }  /* Sidebar background */
        </style>
    """,
    "Dark Mode": """
        <style>
            body { background-color: #181818; color: #f5f5f5; }
            .stButton>button { background-color: #1e1e1e; color: #f5f5f5; }
            .stMetric>div { background-color: #1e1e1e; color: #f5f5f5; }
            .stMarkdown { color: #f5f5f5; }
            .stSidebar { background-color: #121212; color: white; }
            .css-1d391kg { background-color: #121212; }  /* Sidebar background */
        </style>
    """,
    "Sunset Orange": """
        <style>
            body { background-color: #ffe0e0; color: #f44336; }
            .stButton>button { background-color: #f44336; color: white; }
            .stMetric>div { background-color: #f44336; color: white; }
            .stMarkdown { color: #f44336; }
            .stSidebar { background-color: #ff7043; color: white; }
            .css-1d391kg { background-color: #ff7043; }  /* Sidebar background */
        </style>
    """,
    "Forest Green": """
        <style>
            body { background-color: #f0f8f0; color: #388e3c; }
            .stButton>button { background-color: #388e3c; color: white; }
            .stMetric>div { background-color: #388e3c; color: white; }
            .stMarkdown { color: #388e3c; }
            .stSidebar { background-color: #2c6b2f; color: white; }
            .css-1d391kg { background-color: #2c6b2f; }  /* Sidebar background */
        </style>
    """,
    "Ocean Breeze": """
        <style>
            body { background-color: #e0f7fa; color: #00796b; }
            .stButton>button { background-color: #00796b; color: white; }
            .stMetric>div { background-color: #00796b; color: white; }
            .stMarkdown { color: #00796b; }
            .stSidebar { background-color: #004d40; color: white; }
            .css-1d391kg { background-color: #004d40; }  /* Sidebar background */
        </style>
    """,
    "Purple Haze": """
        <style>
            body { background-color: #f3e5f5; color: #9c27b0; }
            .stButton>button { background-color: #9c27b0; color: white; }
            .stMetric>div { background-color: #9c27b0; color: white; }
            .stMarkdown { color: #9c27b0; }
            .stSidebar { background-color: #7b1fa2; color: white; }
            .css-1d391kg { background-color: #7b1fa2; }  /* Sidebar background */
        </style>
    """,
    "Coral Red": """
        <style>
            body { background-color: #ffebee; color: #e57373; }
            .stButton>button { background-color: #e57373; color: white; }
            .stMetric>div { background-color: #e57373; color: white; }
            .stMarkdown { color: #e57373; }
            .stSidebar { background-color: #f44336; color: white; }
            .css-1d391kg { background-color: #f44336; }  /* Sidebar background */
        </style>
    """,
    "Mint Green": """
        <style>
            body { background-color: #e8f5e9; color: #4caf50; }
            .stButton>button { background-color: #4caf50; color: white; }
            .stMetric>div { background-color: #4caf50; color: white; }
            .stMarkdown { color: #4caf50; }
            .stSidebar { background-color: #388e3c; color: white; }
            .css-1d391kg { background-color: #388e3c; }  /* Sidebar background */
        </style>
    """,
    "Lavender Bliss": """
        <style>
            body { background-color: #f3e5f5; color: #8e24aa; }
            .stButton>button { background-color: #8e24aa; color: white; }
            .stMetric>div { background-color: #8e24aa; color: white; }
            .stMarkdown { color: #8e24aa; }
            .stSidebar { background-color: #7b1fa2; color: white; }
            .css-1d391kg { background-color: #7b1fa2; }  /* Sidebar background */
        </style>
    """,
    "Golden Yellow": """
        <style>
            body { background-color: #fff9c4; color: #fbc02d; }
            .stButton>button { background-color: #fbc02d; color: white; }
            .stMetric>div { background-color: #fbc02d; color: white; }
            .stMarkdown { color: #fbc02d; }
            .stSidebar { background-color: #f57f17; color: white; }
            .css-1d391kg { background-color: #f57f17; }  /* Sidebar background */
        </style>
    """
}

# Streamlit App Title with custom font
st.title("📊 GBP/JPY Live Trading Dashboard")

# Color theme selector
theme_choice = st.selectbox("Select a Theme:", list(themes.keys()))

# Apply the selected theme
st.markdown(themes[theme_choice], unsafe_allow_html=True)

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
