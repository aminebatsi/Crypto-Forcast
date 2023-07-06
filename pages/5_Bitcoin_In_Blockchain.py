import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import date
from simplified_scrapy import SimplifiedDoc, req

st.set_page_config(
    page_title="Bitcoin In Blockchain",
)

today = date.today()

st.subheader('Bitcoin In Blockchain')
final_df = pd.read_csv('dataset-auto-collect.csv')

def get_data_bitchartinfo(url):
  html = req.get(url)

  doc = SimplifiedDoc(html)
  js = doc.getElementByText('new Dygraph', tag='script').html
  js = js[js.find('document.getElementById("container"),') +
          len('document.getElementById("container"),'):]
  js = js[:js.find(', {labels:')] # Get data part
  js = js.replace('[new Date("', '').replace('")', '')[1:-2]
  data = [kv.split(',') for kv in js.split('],')]
  return data

def merge_df(merged_df1,df):
      merged_df1 = pd.merge(
      merged_df1,
      df,
      left_on=[merged_df1["Date"].dt.year, merged_df1["Date"].dt.month , merged_df1["Date"].dt.day],
      right_on=[df["Date"].dt.year, df["Date"].dt.month , df["Date"].dt.day],
      how="outer",
      ).drop(["key_0", "key_1"], axis=1)
      merged_df1.drop({'key_2','Date_y'} , inplace=True , axis=1)
      merged_df1.rename({'Date_x' : 'Date'}, inplace=True , axis=1)
      return merged_df1

def convert_date(df):
  df.rename({"timestamp" : "Date"}, axis=1, inplace=True)
  df['Date'] = pd.to_datetime(df['Date']).dt.date
  df['Date'] = pd.to_datetime(df['Date'])
  df = df[(df['Date'] <= str(today))]
  return df

final_= convert_date(final_df)

data = get_data_bitchartinfo('https://bitinfocharts.com/comparison/bitcoin-transactions.html')
df = pd.DataFrame(data,columns=['Date','number_transac_blockchain'])
df = convert_date(df)
final_df = merge_df(final_df,df)
final_df.dropna(axis=0,inplace=True)

data = get_data_bitchartinfo('https://bitinfocharts.com/comparison/sentinusd-btc.html')
df = pd.DataFrame(data,columns=['Date','sent_coins_usd'])
df = convert_date(df)
final_df = merge_df(final_df,df)
final_df.dropna(axis=0,inplace=True)


option_tab3 = st.selectbox(
    'Choose Feature',
    ('Number Of Transaction In Blockchain','Nb of Bitcoin In Circulation', 'Sent Coins In USD', 'Miners Revenue'))

if option_tab3 == 'Number Of Transaction In Blockchain':
    train_data = 'number_transac_blockchain'
elif option_tab3 == 'Nb of Bitcoin In Circulation':
    train_data = 'nb_btc_in_circulation'
elif option_tab3 == 'Sent Coins In USD':
    train_data = 'sent_coins_usd'
elif option_tab3 == 'Miners Revenue':
    train_data = 'miners_revenue'


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=final_df['Date'], y=final_df[train_data], mode='lines'))
st.plotly_chart(fig1, use_container_width=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 