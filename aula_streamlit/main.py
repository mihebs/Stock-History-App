"""A Streamlit app for stock selection and interactive charts."""

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

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

st.sidebar.title('Selecione o stock - Gráfico 2')
ticker_symbol2 = st.sidebar.text_input('Ação', 'MSFT', max_chars=10)

# baixando dados do yahoo
data2 = yf.download(ticker_symbol2, start='2020-01-01', end='2023-06-26')

# exibir os dados
st.subheader('Histórico')
st.dataframe(data2)

# exibir o gráfico de fechamento - gráfico 2
fig_close2 = go.Figure()
fig_close2.add_trace(go.Scatter(x=data2.index, y=data2['Close'], name='Fechamento'))
fig_close2.update_layout(title=f"{ticker_symbol2}", xaxis_title='Data', yaxis_title='Preço')
st.plotly_chart(fig_close2)

# gráfico de barras para o volume de negociação - gráfico 2
fig_volume2 = go.Figure()
fig_volume2.add_trace(go.Bar(x=data2.index, y=data2['Volume'], name='Volume de Negociação - Gráfico 2'))
fig_volume2.update_layout(title=f"{ticker_symbol2} - Volume de Negociação - Gráfico 2", xaxis_title='Data', yaxis_title='Volume')
st.plotly_chart(fig_volume2)

# calcular irf
returns2 = np.log(data2['Close']).diff().dropna()
model2 = sm.tsa.VAR(returns2)
results2 = model2.fit(maxlags=10, ic='aic')
irf2 = results2.irf(10)

# gráfico do irf
fig_irf2 = go.Figure()
for i in range(len(returns2.columns)):
    fig_irf2.add_trace(go.Scatter(x=irf2.irfperiods, y=irf2.irfs[:, i, i], name=returns2.columns[i]))

fig_irf2.update_layout(title='Função de Resposta ao Impulso - Gráfico 2', xaxis_title='Período', yaxis_title='IRF')
st.plotly_chart(fig_irf2)

# https://stockhistory.streamlit.app/
