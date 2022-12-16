import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

st.header("Performa Model")
st.markdown("Performa model dari model Support Vector Machine yang digunakan")

st.subheader("Penjelasan Performa Model")
st.markdown("Hasil evaluasi skor dari model yang dibuat mempunyai hasil yang bagus dikarenakan memiliki nilai accuracy dan F1-Score yang tinggi. Nilai accuracy dan F1-Score yang tinggi berarti model dapat memprediksi ulasan dengan akurat dan memiliki tingkat kesalahan yang rendah. Pada aspek harga, kenyamanan, pelayanan, dan rasa memiliki nilai accuracy dan F1-Score di atas 90% sedangkan aspek umum memiliki nilai sekitar 82%. Accuracy dan F1-Score yang rendah pada aspek umum bisa terjadi dikarenakan ulasan dengan aspek umum memiliki variatif teks yang tinggi dan ulasan pada aspek umum memiliki kata-kata yang mirip dengan ulasan pada aspek lain.")

st.subheader("Evaluasi Akurasi dan F1-Score")
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

url = 'https://raw.githubusercontent.com/AlfarrelIndrawan/data-ulasan/main/hasil-klasifikasi.csv'
df = pd.read_csv(url, delimiter = ";", encoding='cp1252')
df['Accuracy'] = df['Accuracy'].map("{:,.2f}".format) 
df['Precision'] = df['Precision'].map("{:,.2f}".format) 
df['Recall'] = df['Recall'].map("{:,.2f}".format) 
df['F1-Score'] = df['F1-Score'].map("{:,.2f}".format) 
st.table(df)

# Score Image
st.subheader("Bar Chart Hasil Evaluasi Skor")
image = Image.open("bar-chart-hasil-skor.png")
st.image(image)

# Heatmap
st.subheader("Confusion Matrix Heatmap")

# Defining index for the dataframe
idx = ['harga', 'kenyamanan', 'pelayanan', 'rasa', 'umum']
  
# Defining columns for the dataframe
cols = ['harga', 'kenyamanan', 'pelayanan', 'rasa', 'umum']
  
# Entering values in the index and columns  
# and converting them into a panda dataframe
df = pd.DataFrame([[70, 0, 0, 0, 0], [0, 62, 0, 0, 6],
                   [0, 0, 73, 0, 2], [0, 0, 0, 65, 6], [1, 4, 1, 5, 57]],
                   columns = cols, index = idx)

fig, ax = plt.subplots(figsize=(10,7))
sns.heatmap(df, linewidths = 0.30, annot = True, cmap="viridis")
plt.xticks(rotation=0)
plt.yticks(rotation=0)
st.write(fig)