import pandas as pd

def calculate_sma(data, window=20):
    """Calcule la moyenne mobile simple (SMA) pour une fenêtre donnée."""
    return data.rolling(window=window).mean()

def calculate_rsi(data, window=14):
    """Calcule l'indice de force relative (RSI) pour une fenêtre donnée."""
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

import pandas as pd

# Exemple de calcul des bandes de Bollinger
def calculate_bollinger_bands(data, window=20):
    """Calcule les bandes de Bollinger pour une fenêtre donnée."""
    sma = data.rolling(window=window).mean()
    rolling_std = data.rolling(window=window).std()

    upper_band = sma + (rolling_std * 2)
    lower_band = sma - (rolling_std * 2)

    return upper_band, lower_band
