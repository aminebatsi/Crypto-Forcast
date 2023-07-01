import streamlit as st
import base64
import datasetCollection

datasetCollection.collect_data()

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

def render_svg(svg_file):

    with open(svg_file, "r") as f:
        lines = f.readlines()
        svg = "".join(lines)
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s" width="420" height="230"/>' % b64
        return html



st.title('Crypto Forecast Hub')
co1,co2= st.columns(2)
co1.markdown("""Welcome to our website for Bitcoin price prediction! We specialize in providing 
accurate and insightful forecasts for the price movements of Bitcoin, 
the worlds leading cryptocurrency.
Our team of experts and data analysts are constantly monitoring market trends,
 historical data, and other relevant factors to offer you the most informed predictions. 
 Whether you are an investor, trader, or simply interested in the cryptocurrency market, 
 our website is the go-to resource for reliable Bitcoin price 
 predictions.""")
co2.markdown(
    render_svg('1.svg'),
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
   st.subheader("Technical Analysis")
   st.markdown("""Explore the world of technical analysis as we analyze Bitcoin's price charts, patterns, 
   and indicators. Our technical analysis section provides you with insights into support and resistance levels, 
   trend lines, moving averages, 
   and other technical tools that can assist you in predicting future price movements.""")

with col2:
   st.subheader("Bitcoin Price Predictions")
   st.markdown("""Our team utilizes a combination of technical analysis, 
   fundamental analysis, and market sentiment to make informed predictions about Bitcoin's price. We provide short-term,
    medium-term, and long-term forecasts, giving you a comprehensive view of potential price movements.""")

with col3:
   st.subheader("Fundamental Analysis")
   st.markdown("""Understand the fundamental factors that can influence Bitcoin's price. We delve into key events, regulatory developments, industry news,
    and macroeconomic factors that may impact the value of Bitcoin, 
    helping you make more informed investment decisions.""")

st.sidebar.info('Select a page above', icon="ℹ️")
