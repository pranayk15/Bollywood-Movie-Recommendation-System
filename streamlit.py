import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# =============================
# CONFIG
# =============================
OMDB_API_KEY = "80c068a7"   # your OMDb key
MODEL_PATH = "movie_similarity.pkl"

# Google Drive file ID
DRIVE_URL = "https://drive.google.com/uc?id=1Cdkl3c6BxbuAoZWjm9AFddW6jPMtoadS"

st.set_page_config(
    page_title="Bollywood Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# =============================
# DARK THEME CSS
# =============================
st.markdown(
    """
    <style>
    body {
        background-color: #141414;
        color: white;
    }

    h1.netflix-title {
        color: #ffffff !important;
        font-weight: 700;
        margin-bottom: 0.2em;
    }

    .block-container {
        padding-top: 1rem;
    }

    .movie-card {
        background-color: #1f1f1f;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        transition: transform 0.3s ease;
        height:350px;
        width:175px;
    }

    .movie-card:hover {
        transform: scale(1.05);
    }

    .poster-container img {
        width: 550px;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.6);
    }

    .movie-title {
        font-weight: 600;
        margin-top: 10px;
        font-size: 16px;
        color: #ffffff;
    }

    .movie-meta {
        font-size: 14px;
        color: #b3b3b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# SIDEBAR — MODEL EXPLANATION
# =============================
st.sidebar.title("🧠 How this Recommender Works")

st.sidebar.markdown(
    """
    ### 1️⃣ Poster Availability
    Movie Posters are fetched from IMDB using the OMDB API
    
    Some **less popular or older bollywood movies** may not have posters available in the IMDB database.
    In such cases, a placeholder image is displayed.
    
    ---
    
    ### 🎯 Problem Statement
    Recommend **relevant Bollywood movies** based on a selected movie while avoiding outdated or irrelevant recommendations.

    ---
    ### 🧩 Model Type
    **Hybrid Content-Based Recommendation System**

    ---
    ### 🔍 Features Used
    - Overview
    - Genre
    - Director
    - Cast
    - Release year

    ---
    ### 🧠 Text Representation
    TF-IDF + Transformer embeddings

    Hybrid Similarity:
    0.6 × TF-IDF  
    0.4 × Embedding

    ---
    ### ⭐ Final Ranking
    Final Score =
    0.7 × Content Similarity  
    0.3 × Popularity Score
    """
)

# =============================
# DOWNLOAD MODEL IF NOT PRESENT
# =============================
if not os.path.exists(MODEL_PATH):
    st.info("Downloading similarity model...")
    gdown.download(DRIVE_URL, MODEL_PATH, quiet=False)

# =============================
# LOAD DATA
# =============================
df = pickle.load(open("movies_metadata.pkl", "rb"))
similarity = pickle.load(open(MODEL_PATH, "rb"))

# =============================
# OMDb FETCH (POSTER + RATING)
# =============================
@st.cache_data
def get_movie_details(imdb_id):

    fallback_poster = "https://via.placeholder.com/300x450?text=No+Poster"
    fallback_rating = "N/A"

    if pd.isna(imdb_id) or imdb_id == "":
        return fallback_poster, fallback_rating

    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
        data = requests.get(url, timeout=5).json()

        poster = data.get("Poster", "N/A")
        rating = data.get("imdbRating", "N/A")

        if poster == "N/A":
            poster = fallback_poster

        return poster, rating
    except:
        return fallback_poster, fallback_rating

# =============================
# RECOMMENDATION LOGIC
# =============================
def recommend(movie):

    idx = df[df['movie_name'] == movie].index[0]
    sim_scores = list(enumerate(similarity[idx]))

    final_scores = []

    for i, sim in sim_scores:
        score = (
            0.7 * sim +
            0.3 * df.iloc[i].popularity_score
        )
        final_scores.append((i, score))

    final_scores = sorted(final_scores, key=lambda x: x[1], reverse=True)[1:6]

    return df.iloc[[i[0] for i in final_scores]]

# =============================
# MAIN UI
# =============================
st.markdown(
    "<h1 class='netflix-title'>🎬 Bollywood Movie Recommender</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:#b3b3b3;'> • Popularity-aware • IMDb ratings</p>",
    unsafe_allow_html=True
)

movie_list = sorted(df['movie_name'].unique())
selected_movie = st.selectbox("🔍 Search a movie", movie_list)

if st.button("▶ Recommend"):

    with st.spinner("Finding movies you’ll love..."):
        results = recommend(selected_movie)

    cols = st.columns(5)

    for col, (_, row) in zip(cols, results.iterrows()):

        with col:

            poster, rating = get_movie_details(row.movie_id)

            st.markdown(
                f"""
                <div class="movie-card">
                    <div class="poster-container">
                        <img src="{poster}" />
                    </div>
                    <div class="movie-title">{row.movie_name}</div>
                    <div class="movie-meta">⭐ IMDb: {rating}</div>
                    <div class="movie-meta">📅 {row.year}</div>
                    <div class="movie-meta">🎭 {row.genre}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
