import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

DATA_PATH = "data/transactions.csv"

# Function to fetch transactions
def fetch_transactions(address, start_block=0, end_block=99999999):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={start_block}&endblock={end_block}&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url).json()
    if response["status"] == "1":
        return pd.DataFrame(response["result"])
    else:
        print("Error:", response["message"])
        return None

# Function to ensure data is available
def load_data():
    if not os.path.exists(DATA_PATH):
        print("Fetching new transaction data...")
        df = fetch_transactions("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae")  # Replace with target address
        if df is not None:
            os.makedirs("data", exist_ok=True)
            df.to_csv(DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)

df = load_data()
print(df.head())
