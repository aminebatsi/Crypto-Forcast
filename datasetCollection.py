import pandas as pd
import warnings
import requests
from simplified_scrapy import SimplifiedDoc, req
from cryptocmd import CmcScraper


warnings.filterwarnings('ignore')


def check_continous_date(final_df):
    # Create a time series with missing dates
    expected_index = pd.date_range(start=final_df.Date.min(), end=final_df.Date.max(), freq='D')
    # Calculate the difference between expected and actual date ranges
    missing_dates = set(expected_index) - set(final_df.Date)
    if len(missing_dates)==0:
        print('There is no missing date')
    else:
        print(missing_dates)

def convert_date(df):
  df.rename({"timestamp" : "Date"}, axis=1, inplace=True)
  df['Date'] = pd.to_datetime(df['Date']).dt.date
  df['Date'] = pd.to_datetime(df['Date'])
  df = df[(df['Date'] <= str(today))]
  return df

def delete_added_col(final_df):
    final_df.drop({'key_2' , 'Date_x'},axis=1,inplace=True)
    final_df.rename({'Date_y':'Date'},inplace=True,axis=1)

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

from datetime import date
import datetime
import time
today = date.today()
unix_today = int(time.mktime(today.timetuple()))

from cryptocmd import CmcScraper
def collect_data():
    # initialise scraper without time interval for max historical data
    scraper = CmcScraper("BTC")
    # Pandas dataFrame for the same data
    final_df = scraper.get_dataframe()

    final_df

    final_df.drop('Volume',axis=1,inplace=True)

    tech1 = requests.get('https://api.coinmarketcap.com/data-api/v3/global-metrics/quotes/historical?format=chart&interval=2d&timeEnd='+str(unix_today)+'&timeStart=2013-04-29').json()
    tech1_list = list([i["timestamp"],i['btcDominance'],i['quote'][0]['totalMarketCap'],i['quote'][0][ "altcoinMarketCap"]] for i in tech1['data']['quotes'])
    colNames = ['Date' , 'BtcDominance', 'TotalMarketCap' , 'TMC_Without_Btc']
    df = pd.DataFrame(data=tech1_list, columns=colNames)
    df = convert_date(df)

    df

    #final_df = merge_df(final_df[1:],df)
    final_df = merge_df(final_df[:],df)

    df

    final_df

    final_df.fillna(method='ffill',inplace=True)
    final_df.fillna(method='bfill',inplace=True)

    final_df

    final_df.rename({'Market Cap':'Bitcoin_MarCap'},axis=1,inplace=True)

    final_df

    """# ***Mining Difficulty***"""

    data = get_data_bitchartinfo('https://bitinfocharts.com/comparison/bitcoin-difficulty.html')
    df = pd.DataFrame(data,columns=['Date','avg_mining_difficulty'])
    df = convert_date(df)
    final_df = merge_df(final_df,df)
    final_df.dropna(axis=0,inplace=True)

    """# ***Hashrate***"""

    data = get_data_bitchartinfo('https://bitinfocharts.com/comparison/bitcoin-hashrate.html')
    df = pd.DataFrame(data,columns=['Date','avg_hashrate'])
    df = convert_date(df)
    final_df = merge_df(final_df,df)
    final_df.dropna(axis=0,inplace=True)

    """# **Transaction Fee**"""

    data = get_data_bitchartinfo('https://bitinfocharts.com/comparison/bitcoin-transactionfees.html')
    df = pd.DataFrame(data,columns=['Date','avg_transac_fee'])
    df = convert_date(df)
    final_df = merge_df(final_df,df)
    final_df.dropna(axis=0,inplace=True)

    """# ***Transaction Value***"""

    data = get_data_bitchartinfo('https://bitinfocharts.com/comparison/transactionvalue-btc.html')
    df = pd.DataFrame(data,columns=['Date','avg_transac_value'])
    df = convert_date(df)
    final_df = merge_df(final_df,df)
    final_df.dropna(axis=0,inplace=True)


    """# **GPR**"""

    GPR = pd.read_excel('https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls')

    GPR = GPR[['month' , 'GPRC_USA']]
    GPR.rename({'month' : 'Date'}, inplace=True, axis=1)

    GPR = convert_date(GPR)

    GPR = GPR[(GPR.Date > '2013-03-28	')]

    GPR

    GPR.GPRC_USA.tail(1)

    final_df = pd.merge(
        final_df,
        GPR,
        left_on=[final_df["Date"].dt.year, final_df["Date"].dt.month],
        right_on=[GPR["Date"].dt.year, GPR["Date"].dt.month],
        how="outer",
    ).drop(["key_0", "key_1"], axis=1)
    final_df.drop({'Date_y'} , inplace=True , axis=1)
    final_df.rename({'Date_x' : 'Date'}, inplace=True , axis=1)
    final_df.fillna(GPR.GPRC_USA.tail(1).values[0],inplace=True)

    """# **Inflation**"""

    df = pd.read_excel('https://fred.stlouisfed.org/graph/fredgraph.xls?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=719&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CPIAUCSL&scale=left&cosd=1947-01-01&coed=2023-05-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date='+str(today)+'&revision_date='+str(today)+'&nd=1947-01-01',skiprows=10)

    df.rename({'observation_date' : 'Date', 'CPIAUCSL':'Infla'}, inplace=True, axis=1)
    df = convert_date(df)
    df = df[(df.Date > '2013-03-28')]

    df

    final_df = pd.merge(
        final_df,
        df,
        left_on=[final_df["Date"].dt.year, final_df["Date"].dt.month],
        right_on=[df["Date"].dt.year, df["Date"].dt.month],
        how="outer",
    ).drop(["key_0", "key_1"], axis=1)
    final_df.drop({'Date_y'} , inplace=True , axis=1)
    final_df.rename({'Date_x' : 'Date'}, inplace=True , axis=1)
    final_df.fillna(df.Infla.tail(1).values[0],inplace=True)

    final_df

    final_df.sort_values(by='Date', inplace = True)

    """# ***Miners revenue***"""

    data = requests.get('https://data.nasdaq.com/api/v3/datasets/7692472/data')
    data = data.json()
    df = pd.DataFrame(data['dataset_data']['data'],columns=['Date','miners_revenue'])
    df = convert_date(df)
    final_df = merge_df(final_df,df)
    final_df.dropna(axis=0,inplace=True)

    final_df

    """# ***Bitcoin in Circulation***"""

    data = requests.get('https://data.nasdaq.com/api/v3/datasets/7692453/data')
    data = data.json()
    df = pd.DataFrame(data['dataset_data']['data'],columns=['Date','nb_btc_in_circulation'])
    df = convert_date(df)
    final_df = merge_df(final_df,df)
    final_df.dropna(axis=0,inplace=True)

    window = 20  # Number of periods for the moving average and standard deviation
    final_df['SMA_20'] = final_df['Close'].rolling(window).mean()  # Moving average
    final_df['STD'] = final_df['Close'].rolling(window).std() 
    final_df['BBL_20_2.0'] = final_df['SMA_20'] + (2 * final_df['STD'])  # Upper Bollinger Band
    final_df['BBM_20_2.0'] = final_df['SMA_20']  # Midlle 
    final_df['BBU_20_2.0'] = final_df['SMA_20'] - (2 * final_df['STD'])  # Lower Bollinger Band

    print(final_df)

    final_df.drop({'STD'}, inplace=True, axis=1)

    final_df.dropna(inplace=True)

    final_df.rename({'Close' : 'close'},axis=1,inplace=True)

    final_df.to_csv('dataset-auto-collect.csv',index=False)


collect_data()