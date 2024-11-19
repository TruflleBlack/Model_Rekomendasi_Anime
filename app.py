import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your prepared dataframe (anime_new)
anime_new = pd.read_csv('anime_new.csv')  # Assuming you saved it as a CSV

# Function to get recommendations
def anime_recommendations(nama_anime, similarity_data, items, k=5):
    index = similarity_data.loc[:, nama_anime].to_numpy().argpartition(range(-1, -k, -1))
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    closest = closest.drop(nama_anime, errors='ignore')
    return pd.DataFrame(closest).merge(items).head(k)

# Streamlit app
st.set_page_config(page_title="Anime Recommendation System", page_icon=":movie_camera:", layout="wide")
st.title("Anime Recommendation System")
st.write("Discover your next anime adventure!")

# Tambahkan gaya CSS yang lebih menarik
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://img3.wallspic.com/crops/6/9/0/4/7/174096/174096-shonen_manga-anime-weekly_shnen_jump-naruto_uzumaki-sleeve-1366x768.jpg');
        background-size: cover;  
        background-blend-mode: multiply;  
        color: #ffffff;  
        font-family: 'Arial', sans-serif;  
    }

    .header {
        text-align: center;
        margin-bottom: 20px;
        font-size: 2.5em;  
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);  
    }
    </style>
    <div class="overlay"></div>
    """,
    unsafe_allow_html=True
)

# Gambar cover dengan efek border
st.markdown('<div class="cover"><img src="https://storage.googleapis.com/kaggle-datasets-images/465305/874035/b7b33566d0733e759d469ff0f0cfa8b8/dataset-cover.jpg?t=2020-01-05-01-03-57" alt="Cover Image" style="width:100%; border-radius: 15px; border: 5px solid #ffcc00;"></div>', unsafe_allow_html=True)

# Tambahkan header yang lebih menarik
st.markdown('<h1 class="header">Sistem Rekomendasi Anime</h1>', unsafe_allow_html=True)

# Input untuk nama anime
anime_name = st.text_input("Masukkan Nama Anime:", "", placeholder="Contoh: Attack on Titan", key="search")

# Preprocess data dan buat matriks kesamaan (hanya sekali)
if 'similarity_matrix' not in st.session_state:
    tf = TfidfVectorizer()
    tfidf_matrix = tf.fit_transform(anime_new['genre'])
    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_df = pd.DataFrame(cosine_sim, index=anime_new['anime_title'], columns=anime_new['anime_title'])
    st.session_state['similarity_matrix'] = cosine_sim_df

# Tampilkan rekomendasi
if anime_name:
    formatted_anime_name = anime_name.title()
    filtered_anime = anime_new[anime_new['anime_title'].str.contains(formatted_anime_name, case=False)]

    if not filtered_anime.empty:
        st.markdown('<div class="anime-results">', unsafe_allow_html=True)
        for index, row in filtered_anime.iterrows():
            st.markdown(f""" 
            <div class="anime-card-container" style="display: flex; justify-content: space-between;">
                <div class="anime-card" style="margin: 10px; padding: 15px; border: 2px solid #ffcc00; border-radius: 10px; background-color: rgba(255, 204, 0, 0.1); width: 100%; display: flex; flex-direction: column; justify-content: space-between; height: 250px; display: inline-flex; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);" >
                    <div class="anime-card-content">
                        <h3 style="color: #ffcc00; font-size: 1.5em; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);">{row['anime_title']}</h3>
                        <p><strong>Genre:</strong> {row['genre']}</p>
                        <p><strong>Type:</strong> {row['type']}</p>
                        <p><strong>Episode:</strong> {row['episode']}</p>
                        <p><strong>Ratings:</strong> {row['ratings']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("Tidak ada anime yang ditemukan sesuai dengan kriteria pencarian.")
        st.write("Tidak ada anime yang ditemukan sesuai dengan kriteria pencarian.")

# Tambahkan footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.write("**Dibuat oleh: Rizqulloh Rifqi Edwanto**")
