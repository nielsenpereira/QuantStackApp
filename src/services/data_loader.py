import requests
import pandas as pd

def get_ohlcv(ticker, api_key):
    """
    Récupère les données OHLCV pour un ticker donné en utilisant l'API Alpha Vantage.

    :param ticker: Le symbole du ticker pour lequel récupérer les données.
    :param api_key: La clé API pour accéder à Alpha Vantage.
    :return: Un DataFrame pandas contenant les données OHLCV.
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # Convertir les données en DataFrame
    df = pd.DataFrame(data.get("Time Series (Daily)", {})).T
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)
    df = df.apply(pd.to_numeric, errors='ignore')

    return df

# Exemple d'utilisation
# df = get_ohlcv("AAPL", "votre_api_key")
