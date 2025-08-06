import requests
import pandas as pd
import json
import os

def get_ohlcv(ticker, api_key, cache_file='cache.json'):
    # Check if cached data exists
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            if ticker in cache:
                print("Retrieving cached data...")
                return pd.DataFrame(cache[ticker])

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    print(f"Requesting URL: {url}")
    response = requests.get(url)
    data = response.json()

    print(data)

    if "Time Series (Daily)" not in data:
        print("No data found for this ticker.")
        return pd.DataFrame()

    # Convert the data into a DataFrame
    df = pd.DataFrame(data["Time Series (Daily)"]).T
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)

    # Convert columns to numeric
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    df.dropna(inplace=True)

    # Cache the data
    if not os.path.exists(cache_file):
        cache = {}
    cache[ticker] = df.to_dict()
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

    return df