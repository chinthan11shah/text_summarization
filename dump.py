import pandas as pd
from sqlalchemy import create_engine
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
cnx = create_engine('sqlite:///Newspaper.db').connect()
telegraph = pd.read_sql_table('Telegraph',cnx)
ht = pd.read_sql_table('Hindustan_Times',cnx)
ie = pd.read_sql_table('Indian_Express',cnx)
fpj = pd.read_sql_table('FPJ',cnx)
frames = [telegraph,ht,ie,fpj]
df = pd.concat(frames)

df['keywords'] = ''
r = Rake()
for index, row in df.iterrows():
    r.extract_keywords_from_text(row['Article'])
    key_words_dict_scores = r.get_word_degrees()
    row['keywords'] = list(key_words_dict_scores.keys())

df['Tag'] = df['Tag'].map(lambda x: x.split('-'))
for index, row in df.iterrows():
    row['Tag'] = [x.lower().replace('-','') for x in row['Tag']]

df['BOW'] = ''
columns = ['Tag','keywords']
for index, row in df.iterrows():
    words = ''
    for col in columns:
        words += ''.join(row[col])+" "
    row['BOW'] = words

df = df[['Headline','BOW']]

count = CountVectorizer()
count_matrix = count.fit_transform(df['BOW'])
cosine_sim = cosine_similarity(count_matrix,count_matrix)
indices = pd.Series(df['Headline'])
title = 'Sensex, Nifty capture new heights on positive global cues'
idx = indices[indices == title]
print(cosine_sim)