import time
import streamlit as st  
import pickle
import pandas as pd
import re
import emoji
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary

def preprocessing(message):
	message = message.lower()
	message = re.sub('[0-9]+', '', message)
	clean_spcl = re.compile('[/(){}\[\]\|@,;]')
	clean_symbol = re.compile('[^0-9a-z]')
	message = clean_spcl.sub('', message)
	message = clean_symbol.sub(' ', message)
	message = str(message)
	message = re.sub(r"//t",r"\t", message)
	message = re.sub(r"( )\1+",r"\1", message)
	message = re.sub(r"(\n)\1+",r"\1", message)
	message = re.sub(r"(\r)\1+",r"\1", message)
	message = re.sub(r"(\t)\1+",r"\1", message)
	message = message.strip(" ")
	message = formalize_translate(message)
	message = stopword_removal(message)
	message = emoji.replace_emoji(message, '')
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()
	message = stemmer.stem(message)
	return message

def formalize_translate(message):
	url = 'https://raw.githubusercontent.com/AlfarrelIndrawan/data-ulasan/main/fomalisasi-translasi.csv'
	df_formalize = pd.read_csv(url, delimiter = ";", encoding='cp1252')
	kata_salah = list(df_formalize['kata_salah'])
	kata_benar = list(df_formalize['kata_benar'])
	splitted_text = message.split()
	for i, kata in enumerate(kata_salah):
		for j, split_word in enumerate(splitted_text):
			if kata == split_word:
				splitted_text[j] = kata_benar[i]
	return ' '.join(splitted_text)

def stopword_removal(message):
	url = 'https://raw.githubusercontent.com/AlfarrelIndrawan/data-ulasan/main/tambahan-stopword.csv'
	df_stopword = pd.read_csv(url, delimiter = ";", encoding='cp1252')
	custom_stopword = list(df_stopword['stopword'])
	factory = StopWordRemoverFactory()
	stopwords = factory.get_stop_words() + custom_stopword
	dictionary = ArrayDictionary(stopwords)
	stopword = StopWordRemover(dictionary)
	message = stopword.remove(message)
	return message

def vectorize_message(vectorizer, message):
	arr = [message]
	temp_df = pd.DataFrame(arr)
	train_vectors = vectorizer.transform(temp_df[0])
	feature_names = vectorizer.get_feature_names_out()
	dense = train_vectors.todense()
	denselist=dense.tolist()
	dftfidf=pd.DataFrame(denselist, columns=feature_names)
	return dftfidf

st.title("Review Classification")
st.markdown("Input customer's review to get classification result")
form = st.form("classification-form")
message = form.text_area("Review")
submit = form.form_submit_button('Submit')

aspek_model = pickle.load(open('aspek_classifier.sav', 'rb'))
sentimen_model = pickle.load(open('sentimen_classifier.sav', 'rb'))
vectorizer = pickle.load(open('vectorizer.sav', 'rb'))

if submit:
	st.subheader("Classification Result")
	message = preprocessing(message)
	dftidf = vectorize_message(vectorizer, message)
	with st.spinner('Please Wait...'):
		time.sleep(3)
	result_aspek = aspek_model.predict(dftidf)[0]
	st.write("Aspect: ", result_aspek)
	result_sentimen = sentimen_model.predict(dftidf)[0]
	st.write("Sentiment: ", result_sentimen)