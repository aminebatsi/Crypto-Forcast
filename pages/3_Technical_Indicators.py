import streamlit as st
import deploy
import pandas as pd
import plotly.graph_objs as go
import numpy as np

st.set_page_config(
    page_title="Technical Indicators",
)

df = pd.read_csv('dataset-auto-collect.csv')

df['change'] = df['close'].diff()
df['gain'] = df.change.mask(df.change < 0, 0.0)
df['loss'] = -df.change.mask(df.change > 0, -0.0)

#@numba.jit
def rma(x, n):
    """Running moving average"""
    a = np.full_like(x, np.nan)
    a[n] = x[1:n+1].mean()
    for i in range(n+1, len(x)):
        a[i] = (a[i-1] * (n - 1) + x[i]) / n
    return a

df['avg_gain'] = rma(df.gain.to_numpy(), 14)
df['avg_loss'] = rma(df.loss.to_numpy(), 14)

df['rs'] = df.avg_gain / df.avg_loss
df['rsi'] = 100 - (100 / (1 + df.rs))

st.subheader("Technical Indicators")






import plotly.graph_objs as go


fig = go.Figure()
#fig.add_trace(go.Scatter(x=df['Date'], y=df['close'], mode='lines', name='Time series data'))

# Split the data into training and testing sets

option = st.selectbox(
    'Choose time period',
    ('Past 3 years','Last year','Last 2 months', 'Last 1 month', 'Last 10 Days'))


if option == 'Last 2 months':
    train_data = df[-60:]
elif option == 'Past 3 years':
    train_data = df[-1068:]
elif option == 'Last 10 Days':
    train_data = df[-10:]
elif option == 'Last 1 month':
    train_data = df[-30:]
elif option == 'Last year':
    train_data = df[-365:]



from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=1,row_heights=[0.7,0.4])
# Add the training and testing data to the scatter plot
#'''fig.add_trace(go.Candlestick(x=train_data['Date'],
#                open=train_data['Open'],
#                high=train_data['High'],
#                low=train_data['Low'],
#                close=train_data['close'],  name='Price'),row=1, col=1)'''
fig.add_trace(go.Scatter(x=train_data['Date'],y=train_data['close'],name='Price'),row=1, col=1)
fig.add_trace(go.Scatter(x=train_data['Date'], y=train_data['BBU_20_2.0'], mode='lines', name='BBDands Upper'),row=1, col=1)
fig.add_trace(go.Scatter(x=train_data['Date'], y=train_data['BBL_20_2.0'], mode='lines', name='BBDands Lower'),row=1, col=1)
fig.add_trace(go.Scatter(x=train_data['Date'], y=train_data['SMA_20'], mode='lines', name='SMA20'),row=1, col=1)

#   fig.add_trace(go.Scatter(x=test_data['Date'], y=test_data['predicted'], mode='lines', name='Predicted'),row=1, col=1)


# Set the layout and show the plot
fig.update_layout( xaxis_title='Date', yaxis_title='Price',height=600,xaxis_rangeslider_visible=False)

fig.add_trace(go.Scatter(x=train_data['Date'], y=train_data['rsi'], mode='lines',line_color='white', name='RSI'),row=2, col=1)
fig.add_hline(y=30, row=2, col=1,line_color='green',line_dash="dash")
fig.add_hline(y=70, row=2, col=1, line_color='red',line_dash="dash")

st.plotly_chart(fig, use_container_width=True)

