import streamlit as st
import pandas as pd
import requests
import plotly.graph_objs as go

st.set_page_config(
    page_title="Crypto Market",
)

st.subheader('Bitcoin Dominance')
res = requests.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/quotes/historical?range=ALL').json()
a = list([i["timestamp"],i['quote'][0]['marketCap'],i['quote'][1]['marketCap'],i['quote'][2]['marketCap'],i['quote'][3]['marketCap'],i['quote'][4]['marketCap'],i['quote'][5]['marketCap'],i['quote'][6]['marketCap'],i['quote'][7]['marketCap'],i['quote'][8]['marketCap'],i['quote'][9]['marketCap'],i['quote'][10]['marketCap']] for i in res['data']['quotes'])
df = pd.DataFrame(a,columns = ['Date','BTC','ETH','Tether','BNB','USD Coin','XRP','Cardano','Dogecoin','TRON','Solana','Others'])
df['Date'] = pd.to_datetime(df['Date'])
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['Date'], y=df['BTC'], mode='lines',name='BTC'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['ETH'], mode='lines',name='ETH'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['Tether'], mode='lines',name='Tether'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['BNB'], mode='lines',name='BNB'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['USD Coin'], mode='lines',name='USD Coin'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['XRP'], mode='lines',name='XRP'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['Cardano'], mode='lines',name='Cardano'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['Dogecoin'], mode='lines',name='Dogecoin'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['TRON'], mode='lines',name='TRON'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['Solana'], mode='lines',name='Solana'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['Others'], mode='lines',name='Others'))
fig1.update_layout( xaxis_title='Date', yaxis_title='Market Capitalization',height=600)

st.plotly_chart(fig1, use_container_width=True)




