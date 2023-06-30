import requests
import pandas as pd

from datetime import date

today = date.today()

def convert_date(df):
  df.rename({"timestamp" : "Date"}, axis=1, inplace=True)
  df['Date'] = pd.to_datetime(df['Date']).dt.date
  df['Date'] = pd.to_datetime(df['Date'])
  df = df[(df['Date'] <= str(today))]
  return df

df = pd.read_excel('https://www.eia.gov/dnav/pet/xls/PET_PRI_SPT_S1_D.xls',sheet_name='Data 1', skiprows=2)
df.drop(['Europe Brent Spot Price FOB (Dollars per Barrel)'],axis=1,inplace=True)
df.rename({'Cushing, OK WTI Spot Price FOB (Dollars per Barrel)':'WTI_Oil_Price'},axis=1,inplace=True)
df.fillna(method='ffill',inplace=True)
df.fillna(method='bfill',inplace=True)
df = convert_date(df)
df = df[(df.Date > '2013-03-28')]
df.to_csv('oil.csv' , index=False)

prices = requests.get('https://markets.tradingeconomics.com/chart?s=xauusd:cur&span=1y&securify=new&url=/commodity/gold&AUTH=rwRgUnjCSNY6Y5/fuwi/5HbQHZd7SJh0cu3IBNUGQJvXY5MYhHwYZPhpv/dnqq/U&ohlc=1').json()
prices = list([prices['series'][0]['data'][i]['date'] , prices['series'][0]['data'][0]['close']] for i in range(len(prices['series'][0]['data'])))
gold = pd.DataFrame(prices , columns=['Date','gold_price'])
gold = convert_date('Date')
gold.to_csv('gold.csv' , index=False)
