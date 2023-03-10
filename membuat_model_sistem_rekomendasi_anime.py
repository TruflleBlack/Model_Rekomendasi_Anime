# -*- coding: utf-8 -*-
"""Membuat_Model_Sistem_Rekomendasi_Anime

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vbewHvWFmdj6utUcD2RBjKjgEkBxO3HS

# 1. Download dataset

## 1.1. Mengupload kagle ke google colab
"""

from google.colab import files

files.upload()
! mkdir ~/.kaggle
! cp kaggle.json ~/.kaggle/
! chmod 600 ~/.kaggle/kaggle.json
! kaggle datasets list

"""## 1.2. Download dataset"""

! kaggle datasets download -d hernan4444/animeplanet-recommendation-database-2020

"""## 1.3. Unzip dataset"""

! unzip animeplanet-recommendation-database-2020.zip -d .

"""# 2. Mengimport Modul Python

mengimport data numpy dan pandas, data untuk visualisasi, dan data untuk pembuatan model
"""

import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt
import missingno as msno
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, plot, iplot
from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""# 3. Data Understanding

## 3.1. Memuat dan membaca data pada sebuah dataframe menggunakan pandas
"""

anime = pd.read_csv('/content/anime.csv')
anime_list = pd.read_csv('/content/animelist.csv')
anime_recomen = pd.read_csv('/content/anime_recommendations.csv')
rating = pd.read_csv('/content/rating_complete.csv')
watch = pd.read_csv('/content/watching_status.csv')

"""## 3.2. Ukuran dari dataset Movie"""

anime.shape

"""## 3.3. Ukuran dari dataset Anime list"""

anime_list.shape

"""## 3.4. Ukuran dari dataset Anime Recomen"""

anime_recomen.shape

"""## 3.5. Ukuran dari dataset Rating"""

rating.shape

"""## 3.6. Ukuran dari dataset Watch"""

watch.shape

"""# 4. Univariate Exploratory Data Analysis

## 4.1. Anime dataset

Menampilkan fitur sampel pada dataset Movie
"""

anime.sample(10)

anime = anime.rename(columns={'Anime-PlanetID': 'anime_id'})

anime.head()

"""Memuat kumpulan informasi dataset movie"""

anime.info()

"""Overview dataframe dataset movie"""

anime.describe().T.style.bar(
    subset=['mean'],
    color='#606ff2').background_gradient(
    subset=['std'], cmap='PuBu').background_gradient(subset=['50%'], 
                                                     cmap='PuBu')

"""Memeriksa baris yang *missing values*

## 4.2. Anime List dataset

Menampilkan fitur sampel pada dataset Rating
"""

anime_list.sample(10)

"""Memuat kumpulan informasi dataset ratings"""

anime_list.info()

"""Overview dataframe dataset ratings"""

anime_list.describe().T.style.bar(
    subset=['mean'],
    color='#606ff2').background_gradient(
    subset=['std'], cmap='PuBu').background_gradient(subset=['50%'], 
                                                     cmap='PuBu')

"""Memeriksa baris yang missing values

## 4.3. Anime Recomendasi dataset
"""

anime_recomen.sample(10)

anime_recomen.info()

anime_recomen.describe().T.style.bar(
    subset=['mean'],
    color='#606ff2').background_gradient(
    subset=['std'], cmap='PuBu').background_gradient(subset=['50%'], 
                                                     cmap='PuBu')

"""## 4.4. Rating Dataset"""

rating.sample(10)

rating.info()

rating.describe().T.style.bar(
    subset=['mean'],
    color='#606ff2').background_gradient(
    subset=['std'], cmap='PuBu').background_gradient(subset=['50%'], 
                                                     cmap='PuBu')

"""## 4.5. Visualisasi Dataset"""

data = rating['rating'].value_counts()

trace = go.Bar(x = data.index,y = data.values,text = ['{:.1f} %'.format(val) for val in (data.values / rating.shape[0] * 100)],textposition = 'auto')

layout = dict(title = 'Distribution of {} Anime-ratings'.format(rating.shape[0]), xaxis = dict(title = 'rating'), yaxis = dict(title = 'Anime'))

fig = go.Figure(data=[trace], layout=layout)

iplot(fig)

data = anime['StartYear'].value_counts()

trace = go.Bar(x = data.index,y = data.values,text = ['{:.1f} %'.format(val) for val in (data.values / anime.shape[0] * 100)],textposition = 'auto')

layout = dict(title = 'Distribution of {} Anime - Year-wise'.format(rating.shape[0]), xaxis = dict(title = 'StartYear'), yaxis = dict(title = 'Animes'))

fig = go.Figure(data=[trace], layout=layout)

iplot(fig)

"""# 5. Data Preprocessing

## 5.1. Menggabungkan Anime Id
"""

anime_all = np.concatenate((
    anime.anime_id.unique(),
    anime_list.anime_id.unique(),
    anime_recomen.Anime.unique(),
    rating.anime_id.unique()
))
anime_all= np.sort(np.unique(anime_all))
 
print('Jumlah seluruh data Anime berdasarkan anime ID: ', len(anime_all))

"""## 5.2. Menggabungkan seluruh user id"""

# Menggabungkan seluruh userID
user_all = np.concatenate((
    anime_list.user_id.unique(),
    rating.user_id.unique()
))
 
# Menghapus data yang sama kemudian mengurutkannya
user_all = np.sort(np.unique(user_all)) 
 
print('Jumlah seluruh user: ', len(user_all))

"""## 5.3. Mengetahui Jumlah Rating"""

animes = pd.merge(rating, anime , on='anime_id', how='left')
animes

animes.info()

animes.isnull().sum()

"""## 5.4. Menggabungkan Data dengan Fitur Nama Anime"""

animes.groupby('anime_id').sum()

all_anime_rate = rating
all_anime_rate

"""## 5.5. Menggabungkan Data dengan dataframe anime"""

all_anime_name = pd.merge(all_anime_rate, anime[['anime_id','Name','Tags','Type','Episodes','Rating Score','Synopsis']], on='anime_id', how='left')
all_anime_name

"""# 6. Data Preparation

## 6.1. Mengecek missing value
"""

all_anime_name.isnull().sum()

all_anime_clean = all_anime_name.dropna()
all_anime_clean

all_anime_clean.isnull().sum()

"""## 6.2. Menyamakan Jenis Anime"""

fix_anime = all_anime_clean.sort_values('anime_id', ascending=True)
fix_anime

len(fix_anime.anime_id.unique())

"""## 6.3. Membuat variabel preparation"""

preparation = fix_anime
preparation.sort_values('anime_id')

"""## 6.4. Membuang data duplikat pada variabel preparation"""

preparation = preparation.drop_duplicates('anime_id')
preparation

"""## 6.5. Melakukan konversi data series menjadi list"""

# Mengonversi data series ???movieId??? menjadi dalam bentuk list
anime_id = preparation['anime_id'].tolist()
 
# Mengonversi data series 'Name' menjadi dalam bentuk list
anime_name = preparation['Name'].tolist()
 
# Mengonversi data series 'Tags' menjadi dalam bentuk list
genre = preparation['Tags'].tolist()

# Mengonversi data series 'Type' menjadi dalam bentuk list
type = preparation['Type'].tolist()

# Mengonversi data series 'Episodes' menjadi dalam bentuk list
episodes = preparation['Episodes'].tolist()

# Mengonversi data series 'Rating' menjadi dalam bentuk list
ratings = preparation['rating'].tolist()
 
print(len(anime_id))
print(len(anime_name))
print(len(genre))
print(len(type))
print(len(episodes))
print(len(ratings))

# Membuat dictionary untuk data ???movie_id???, ???movie_name???, dan ???movie_genre???
anime_new = pd.DataFrame({
    'id': anime_id,
    'anime_title': anime_name,
    'genre': genre,
    'type':type,
    'episode':episodes,
    'ratings':ratings
})
anime_new

"""# 7. Model Development dengan Content Based Filtering

## 7.1. Model TF-IDF Vectorizer
"""

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()
 
# Melakukan perhitungan idf pada data cuisine
tf.fit(anime_new['genre']) 
 
# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names()

# Melakukan fit lalu ditransformasikan ke bentuk matrix
tfidf_matrix = tf.fit_transform(anime_new['genre']) 
 
# Melihat ukuran matrix tfidf
tfidf_matrix.shape

# Mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()
tfidf_matrix.todense()

# Membuat dataframe untuk melihat tf-idf matrix
 
pd.DataFrame(
    tfidf_matrix.todense(), 
    columns=tf.get_feature_names(),
    index=anime_new.anime_title
).sample(22, axis=1).sample(10, axis=0)

"""## 7.2. Cosine Similarity"""

# Menghitung cosine similarity pada matrix tf-idf
cosine_sim = cosine_similarity(tfidf_matrix) 
cosine_sim

cosine_sim_df = pd.DataFrame(cosine_sim, index=anime_new['anime_title'], columns=anime_new['anime_title'])
print('Shape:', cosine_sim_df.shape)
 
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""## 7.3. Mendapatkan Rekomendasi"""

def anime_recommendations(nama_anime, similarity_data=cosine_sim_df, items=anime_new[['anime_title', 'genre', 'type', 'episode','ratings']], k=5):
   
 
    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan    
    # Dataframe diubah menjadi numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,nama_anime].to_numpy().argpartition(
        range(-1, -k, -1))
    
    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    
    # Drop nama_movie agar nama movie yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(nama_anime, errors='ignore')
 
    return pd.DataFrame(closest).merge(items).head(k)

anime_new[anime_new.anime_title.eq('Naruto')]

recommended = anime_recommendations('Naruto')
recommended.sort_values(['ratings'], ascending=False)

"""# 8. Evaluation"""

k = 5.0
threshold = 2.5
anime_ratings = recommended['ratings'].values
ratings_relevances = anime_ratings > threshold
precision = len(anime_ratings[ratings_relevances]) / k
print(f'The precision of the recommendation system is {precision:.1%}')