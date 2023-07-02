import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import date
from yahoofinancials import YahooFinancials

st.set_page_config(
    page_title="Macroeconomic",
)

today = date.today()

def convert_date(df):
  df.rename({"timestamp" : "Date"}, axis=1, inplace=True)
  df['Date'] = pd.to_datetime(df['Date']).dt.date
  df['Date'] = pd.to_datetime(df['Date'])
  df = df[(df['Date'] <= str(today))]
  return df

Infla = pd.read_excel('https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=719&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPIAUCSL&scale=left&cosd=1947-01-01&coed=2023-05-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date='+str(today)+'&revision_date='+str(today)+'&nd=1947-01-01',skiprows=10)

Infla.rename({'observation_date' : 'Date', 'CPIAUCSL':'Infla'}, inplace=True, axis=1)
Infla = convert_date(Infla)
Infla = Infla[(Infla.Date > '2013-03-28')]

yahoo_financials = YahooFinancials('GC=F', concurrent=True, max_workers=8, country="US")
gold = pd.DataFrame(yahoo_financials.get_historical_price_data('2013-04-15', str(today), 'daily')['GC=F']['prices']).rename({'formatted_date':'Date','close':'gold_price'},axis=1)[['Date','gold_price']]
gold['Date'] = pd.to_datetime(gold['Date'])
gold.fillna('ffill',inplace=True,axis=1)
gold.fillna('bfill',inplace=True,axis=1)
yahoo_financials = YahooFinancials('CL=F', concurrent=True, max_workers=8, country="US")
oil = pd.DataFrame(yahoo_financials.get_historical_price_data('2013-04-15', str(today), 'daily')['CL=F']['prices']).rename({'formatted_date':'Date','close':'WTI_Oil_Price'},axis=1)[['Date','WTI_Oil_Price']]
oil["Date"] = pd.to_datetime(oil['Date'])
oil.reset_index(drop=True,inplace=True)
oil.fillna('ffill',inplace=True,axis=1)
oil.fillna('bfill',inplace=True,axis=1)

gold_list = pd.to_numeric(gold['gold_price']).tolist()
oil_list = pd.to_numeric(oil['WTI_Oil_Price']).tolist()


st.subheader('Macroeconomic')

gold_change = (gold.loc[:,gold.columns == 'gold_price'].tail(1).values[0][0]- gold.loc[:,gold.columns == 'gold_price'].tail(2).values[0][0])/ gold.loc[:,gold.columns == 'gold_price'].tail(2).values[0][0]
oil_change = (oil.loc[:,oil.columns == 'WTI_Oil_Price'].tail(1).values[0][0]- oil.loc[:,oil.columns == 'WTI_Oil_Price'].tail(2).values[0][0])/oil.loc[:,oil.columns == 'WTI_Oil_Price'].tail(2).values[0][0]


pos_check = Infla.loc[:,Infla.columns == 'Infla'].tail(1).values[0][0] - Infla.loc[:,Infla.columns == 'Infla'].tail(2).values[0][0]
if pos_check > 0:
    inf = Infla.loc[:,Infla.columns == 'Infla'].tail(1).values[0][0]
elif pos_check <0:
    inf = - Infla.loc[:,Infla.columns == 'Infla'].tail(1).values[0][0]

col1, col2, col3 = st.columns(3)
col1.metric("Change", "Gold", str(round(gold_change , 4)) + "%")
col2.metric("Change", "Oil", str(round(oil_change , 4)) + "%")
col3.metric("Monthly", "Inflation", str(round(inf, 4)))

option_tab3 = st.selectbox(
    'Choose Feature',
    ('Gold','Oil','Inflation'))
if option_tab3 == 'Gold':
    train_data =  gold_list
    temp = gold.Date
elif option_tab3 == 'Oil':
    train_data = oil_list
    temp = oil.Date
elif option_tab3 == 'Inflation':
    train_data = Infla['Infla'].tolist()
    temp = Infla['Date'].tolist()


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=temp, y=train_data, line_color='red' , mode='lines'))
st.plotly_chart(fig1, use_container_width=True)