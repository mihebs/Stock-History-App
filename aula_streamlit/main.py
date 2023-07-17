"""A Streamlit app for stock selection and interactive charts."""

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

# título do app
st.title('Stock History App')

st.sidebar.title('Selecione o stock')
ticker_symbol = st.sidebar.text_input('stock', 'AAPL', max_chars=10)

# baixando dados do yahoo
data = yf.download(ticker_symbol, start='2020-01-01', end='2023-06-26')

# exibir os dados
st.subheader('Histórico')
st.dataframe(data)

# gráfico de preço de fechamento
fig = go.Figure()
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Fechamento'))
fig.update_layout(
    title=f"{ticker_symbol}",
    xaxis_title='Data',
    yaxis_title='Preço'
)
st.plotly_chart(fig)

# gráfico de preço máximo
fig_high = go.Figure()
fig_high.add_trace(go.Scatter(x=data.index, y=data['High'], name='Preço Máximo'))
fig_high.update_layout(
    title=f"{ticker_symbol} - Preço Máximo",
    xaxis_title='Data',
    yaxis_title='Preço Máximo'
)
st.plotly_chart(fig_high)

# gráfico de barras para o volume de negociação
fig_volume = px.bar(data, x=data.index, y='Volume', title=f"Volume de Negociação - {ticker_symbol}")
fig_volume.update_layout(
    xaxis_title='Data',
    yaxis_title='Volume'
)
st.plotly_chart(fig_volume)
