import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Streamlit App Title
st.title("📊 GBP/JPY Live Trading Dashboard")

# Placeholder for real-time data (To be replaced with live data integration later)
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

st.plotly_chart(fig)

# Placeholder for Open Trades
st.subheader("Open Trades")
trades = pd.DataFrame({"Trade ID": [1, 2], "Type": ["Buy", "Sell"], "Price": [150.5, 151.0], "Profit": [10, -5]})
st.dataframe(trades)

# Future: Connect to MetaTrader 5 to fetch real-time trades and market data
