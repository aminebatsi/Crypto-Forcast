import streamlit as st
import deploy
import pandas as pd

st.set_page_config(
    page_title="data prediction",
)

df = pd.read_csv('dataset-auto-collect.csv')
df_pred = deploy.hello()
st.subheader("Prediction of next 15 Days")


df_pred['change'] = df_pred["predicted"].pct_change() 
df_pred['change'] = df_pred['change'] * 100
df_pred.fillna((df_pred.predicted.head(1).values[0] - df.close.tail(1).values[0]) / df.close.tail(1).values[0], inplace=True) 


col1, col2, col3 ,col4, col5,= st.columns(5)
col1.metric("", "Day 1", str(round(df_pred.iloc[0,2], 2)) + "%")
col2.metric("", "Day 2", str(round(df_pred.iloc[1,2], 2)) + "%")
col3.metric("", "Day 3", str(round(df_pred.iloc[2,2], 2)) + "%")
col4.metric("", "Day 4", str(round(df_pred.iloc[3,2], 2)) + "%")
col5.metric("", "Day 5", str(round(df_pred.iloc[4,2], 2)) + "%")

col6, col7 , col8, col9, col10  = st.columns(5)
col6.metric("", "Day 6", str(round(df_pred.iloc[5,2], 2)) + "%")
col7.metric("", "Day 7", str(round(df_pred.iloc[6,2], 2)) + "%")
col8.metric("", "Day 8", str(round(df_pred.iloc[7,2], 2)) + "%")
col9.metric("", "Day 9", str(round(df_pred.iloc[8,2], 2)) + "%")
col10.metric("", "Day 10", str(round(df_pred.iloc[9,2], 2)) + "%")

col11, col12, col13 ,col14, col15,= st.columns(5)
col11.metric("", "Day 11", str(round(df_pred.iloc[10,2], 2)) + "%")
col12.metric("", "Day 12", str(round(df_pred.iloc[11,2], 2)) + "%")
col13.metric("", "Day 13", str(round(df_pred.iloc[12,2], 2)) + "%")
col14.metric("", "Day 14", str(round(df_pred.iloc[13,2], 2)) + "%")
col15.metric("", "Day 15", str(round(df_pred.iloc[14,2], 2)) + "%")


st.dataframe(df_pred.loc[:, df_pred.columns != 'actual'].set_index('Date').transpose())

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 