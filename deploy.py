# -*- coding: utf-8 -*-
"""Deploy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dKiPH1o-TQWmVONqmdOK5rl0wbUA8per
"""

import pandas as pd
import pickle



def hello():
       df = pd.read_csv('dataset-auto-collect.csv')
       df['1Day_N'] = df['close'].shift(-1)
       df['2Day_N'] = df['close'].shift(-2)
       df['3Day_N'] = df['close'].shift(-3)
       df['4Day_N'] = df['close'].shift(-4)
       df['5Day_N'] = df['close'].shift(-5)
       df['6Day_N'] = df['close'].shift(-6)
       df['7Day_N'] = df['close'].shift(-7)
       df['8Day_N'] = df['close'].shift(-8)
       df['9Day_N'] = df['close'].shift(-9)
       df['10Day_N'] = df['close'].shift(-10)
       df['11Day_N'] = df['close'].shift(-11)
       df['12Day_N'] = df['close'].shift(-12)
       df['13Day_N'] = df['close'].shift(-13)
       df['14Day_N'] = df['close'].shift(-14)
       df['15Day_N'] = df['close'].shift(-15)

       from sklearn.preprocessing import MinMaxScaler
       scaler=MinMaxScaler(feature_range=(0,1))

       size = int(df.shape[0] * 0.85)


       df.columns

       X = df[['close', 'Open', 'High', 'Low', 'BtcDominance', 'TotalMarketCap',
              'TMC_Without_Btc', 'Infla', 'GPRC_USA', 'avg_mining_difficulty',
              'avg_hashrate', 'avg_transac_fee', 'avg_transac_value',
              'miners_revenue', 'nb_btc_in_circulation', 'SMA_20', 'BBL_20_2.0',
              'BBM_20_2.0', 'BBU_20_2.0', 'Bitcoin_MarCap']]
       Y = df[['1Day_N', '2Day_N',
              '3Day_N', '4Day_N', '5Day_N', '6Day_N', '7Day_N', '8Day_N', '9Day_N',
              '10Day_N', '11Day_N', '12Day_N', '13Day_N', '14Day_N', '15Day_N']]

       x_train = X.loc[:size]
       y_train = Y.loc[:size]
       x_test = X.loc[size:]
       y_test = Y.loc[size:]

       x_train = scaler.fit_transform(x_train)
       x_test = scaler.fit_transform(x_test)
       y_train = scaler.fit_transform(y_train)
       y_test = scaler.fit_transform(y_test)

       x_test.shape , x_train.shape , y_test.shape , y_train.shape


       with open('model_15D.pkl', 'rb') as file:  
              multioutputregressor = pickle.load(file)

       pred = multioutputregressor.predict(x_test)

       print(scaler.inverse_transform(pred)[-1])
       df_temp= None
       df_temp = pd.DataFrame()
       df_temp['Date'] = pd.date_range(df.Date.tail(1).values[0], periods=16, freq='D')[1:]
       df_temp['predicted'] = scaler.inverse_transform(pred)[-1]
       return df_temp
