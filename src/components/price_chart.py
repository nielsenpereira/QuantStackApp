import plotly.graph_objects as go

def plot_price_with_indicators(df, title="Graphique des Prix avec Indicateurs"):
    """Génère un graphique en chandeliers avec des indicateurs techniques."""
    fig = go.Figure()

    # Ajouter les chandeliers pour les données OHLCV
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Prix OHLC',
        increasing_line_color='green',
        decreasing_line_color='red'
    ))

    # Ajouter SMA
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['SMA_20'],
            name='SMA 20',
            line=dict(color='blue', width=1)
        ))

    # Ajouter les bandes de Bollinger avec une transparence accrue
    if 'Upper_Band' in df.columns and 'Lower_Band' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Upper_Band'],
            line=dict(width=0),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Lower_Band'],
            fillcolor='rgba(68, 68, 220, 0.1)',  # Augmenter la transparence
            fill='tonexty',
            line=dict(width=0),
            name='Bandes de Bollinger'
        ))

    # Mise en page du graphique
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Prix',
        xaxis_rangeslider_visible=False,  # Désactiver la fenêtre de zoom
        plot_bgcolor='rgba(173, 216, 230, 0.5)',  # Fond bleu clair
        xaxis=dict(showgrid=True),  # Montrer le cadrillage pour l'axe x
        yaxis=dict(showgrid=True),  # Montrer le cadrillage pour l'axe y
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

def plot_rsi(df, title="Graphique du RSI"):
    """Génère un graphique du RSI."""
    if 'RSI_14' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['RSI_14'],
            name='RSI 14',
            line=dict(color='purple', width=1)
        ))
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='RSI',
            plot_bgcolor='rgba(173, 216, 230, 0.5)',  # Fond bleu clair
            xaxis=dict(showgrid=True),  # Montrer le cadrillage pour l'axe x
            yaxis=dict(showgrid=True),  # Montrer le cadrillage pour l'axe y
            showlegend=True
        )
        return fig
    return None
