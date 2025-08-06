import requests
import pandas as pd
import json
import os

def get_ohlcv(ticker, api_key, start_date=None, end_date=None, cache_file='cache.json'):
    # Vérifier si des données en cache existent
    cache_key = f"{ticker}_{start_date}_{end_date}"
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
            if cache_key in cache:
                print("Retrieving cached data...")
                return pd.DataFrame(cache[cache_key])

    # Construire l'URL en fonction des dates fournies
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    if start_date and end_date:
        # Note: Alpha Vantage's free tier does not support custom date ranges directly.
        # This is a conceptual example; you might need to filter data post-request.
        print(f"Requesting URL: {url} with date range from {start_date} to {end_date}")
    else:
        print(f"Requesting URL: {url}")

    response = requests.get(url)
    data = response.json()

    print(data)

    if "Time Series (Daily)" not in data:
        print("No data found for this ticker.")
        return pd.DataFrame()

    # Convertir les données en DataFrame
    df = pd.DataFrame(data["Time Series (Daily)"]).T
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)

    # Filtrer les données en fonction de la plage de dates si elle est spécifiée
    if start_date and end_date:
        df = df.loc[start_date:end_date]

    # Convertir les colonnes en numérique
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    df.dropna(inplace=True)

    # Mettre en cache les données
    if not os.path.exists(cache_file):
        cache = {}
    cache[cache_key] = df.to_dict()
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

    return df
