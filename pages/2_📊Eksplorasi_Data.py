import streamlit as st
import pandas as pd

st.header("Sumber Data")

url = 'https://raw.githubusercontent.com/AlfarrelIndrawan/data-ulasan/main/sumber-data.csv'
df = pd.read_csv(url, delimiter = ";", encoding='cp1252')
df = df.drop(df.columns[[6, 7, 8, 9, 10, 11]],axis = 1)
df['jumlah_ulasan'] = df['jumlah_ulasan'].map("{:,.0f}".format) 
st.dataframe(df)