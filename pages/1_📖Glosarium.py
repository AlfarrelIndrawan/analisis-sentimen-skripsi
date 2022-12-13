import streamlit as st  
import pandas as pd

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.header("Penjelasan Pengkategorian Aspek dan Sentimen")

st.subheader("Dasar Pengkategorian Aspek")
url = 'https://raw.githubusercontent.com/AlfarrelIndrawan/data-ulasan/main/panduan-aspek.csv'
df_aspek = pd.read_csv(url, delimiter = ";", encoding='cp1252')
st.table(df_aspek)

st.subheader("Dasar Pengkategorian Sentimen")
url = 'https://raw.githubusercontent.com/AlfarrelIndrawan/data-ulasan/main/panduan-sentimen.csv'
df_sentimen = pd.read_csv(url, delimiter = ";", encoding='cp1252')
st.table(df_sentimen)