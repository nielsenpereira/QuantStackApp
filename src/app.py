import streamlit as st
from services.data_loader import get_ohlcv

# Titre de l'application
st.title("Quant Stack App - Analyse Technique")

# Entrées utilisateur
ticker = st.text_input("Entrez le ticker :", "AAPL")
api_key = st.text_input("Entrez votre clé API Alpha Vantage :", type="password")

# Bouton pour charger les données
if st.button("Charger les données"):
    if ticker and api_key:
        try:
            # Charger les données OHLCV
            df = get_ohlcv(ticker, api_key)

            # Afficher les données
            if not df.empty:
                st.write("### Données OHLCV")
                st.write(df)

                # Afficher un graphique simple
                st.write("### Graphique des Prix de Clôture")
                st.line_chart(df['Close'])
            else:
                st.error("Aucune donnée trouvée pour ce ticker.")
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
    else:
        st.error("Veuillez entrer un ticker et une clé API valides.")
