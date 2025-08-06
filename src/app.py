import streamlit as st
from services.data_loader import get_ohlcv
from core.indicators import calculate_sma, calculate_rsi, calculate_bollinger_bands
from components.price_chart import plot_price_with_indicators, plot_rsi

# Titre de l'application
st.title("Quant Stack App - Analyse Technique")

# Entrées utilisateur
ticker = st.text_input("Entrez le ticker :", "AAPL")
api_key = st.text_input("Entrez votre clé API Alpha Vantage :", type="password")

if st.button("Charger les données"):
    if ticker and api_key:
        try:
            df = get_ohlcv(ticker, api_key)
            if not df.empty:
                st.write("### Données OHLCV")
                st.write(df)

                # Calculer les indicateurs techniques
                df['SMA_20'] = calculate_sma(df['Close'])
                df['RSI_14'] = calculate_rsi(df['Close'])
                df['Upper_Band'], df['Lower_Band'] = calculate_bollinger_bands(df['Close'])

                # Afficher le graphique des chandeliers avec les indicateurs
                st.plotly_chart(plot_price_with_indicators(df), key="candlestick_chart")

                # Afficher le graphique du RSI
                rsi_fig = plot_rsi(df)
                if rsi_fig:
                    st.plotly_chart(rsi_fig, key="rsi_chart")
            else:
                st.error("Aucune donnée trouvée pour ce ticker.")
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
    else:
        st.error("Veuillez entrer un ticker et une clé API valides.")
