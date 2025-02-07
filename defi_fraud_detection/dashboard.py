import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

def load_data(file_path="data/transactions.csv"):
    """Load transaction data from CSV."""
    return pd.read_csv(file_path)

# Streamlit UI
st.title("DeFi Fraud Detection Dashboard")

# Load Data
df = load_data()
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

# Large Transfers
large_tx_threshold = st.slider("Set Large Transfer Threshold (ETH)", min_value=1, max_value=10000, value=1000)
large_tx = df[df['value'] > large_tx_threshold]
st.subheader("Large Transfers")
st.dataframe(large_tx[['timeStamp', 'from', 'to', 'value']])

# Plot Transactions
fig = px.scatter(df, x='timeStamp', y='value', color='value', title="Transaction Values Over Time")
st.plotly_chart(fig)

# Rapid Transactions
df['time_diff'] = df['timeStamp'].diff().dt.seconds.fillna(0)
df['rapid_tx'] = df['time_diff'] < 10
rapid_tx = df[df['rapid_tx']]
st.subheader("Rapid Transactions")
st.dataframe(rapid_tx[['timeStamp', 'from', 'to', 'value', 'time_diff']])

# Zero-Value Transactions
zero_value_tx = df[df['value'] == 0]
st.subheader("Zero-Value Transactions")
st.dataframe(zero_value_tx[['timeStamp', 'from', 'to', 'functionName']])

# Run Streamlit
# To launch, use: streamlit run dashboard.py