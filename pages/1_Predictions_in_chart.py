import streamlit as st
import deploy
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('dataset-auto-collect.csv')
df_pred = deploy.hello()

st.subheader("Prediction of next 15 Days")


option_tab3 = st.selectbox(
    'Choose time period',
    ('Previous year','Last 2 months', 'Last 1 month', 'Last 10 Days'))

if option_tab3 == 'Last 2 months':
    train_data = df[-60:]
elif option_tab3 == 'Last 10 Days':
    train_data = df[-10:]
elif option_tab3 == 'Last 1 month':
    train_data = df[-30:]
elif option_tab3 == 'Previous year':
    train_data = df[-365:]

fig1 = go.Figure()

#fig1.add_trace(go.Scatter(x=train_data['Date'], y=train_data['close'], mode='lines', name='Price'))
fig1.add_trace(go.Candlestick(x=train_data['Date'],
                open=train_data['Open'],
                high=train_data['High'],
                low=train_data['Low'],
                close=train_data['close'],  name='Price'))
fig1.add_trace(go.Scatter(x=df_pred['Date'], y=df_pred['predicted'], line_color='red', mode='lines', name='Predicted'))

fig1.update_layout( xaxis_title='Date', yaxis_title='Price',height=600)

st.plotly_chart(fig1, use_container_width=True)