import streamlit as st
import pickle
import pandas as pd
import requests
import gzip
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the data from CSV and add movie_id
movies_df = pd.read_csv('Movies_IMDB.csv')
movies_df['movie_id'] = range(len(movies_df))
movies = pd.DataFrame(movies_df)

# Load the precomputed similarity matrix
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4b535bb4ed32ad84c6832cfc9f1a6a8a&append_to_response=videos,images'
    data = requests.get(url).json()
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/original/" + data['poster_path']
    else:
        return "https://via.placeholder.com/150"  # Placeholder image if poster not available

def release(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4b535bb4ed32ad84c6832cfc9f1a6a8a'
    data = requests.get(url).json()
    return data.get('release_date', 'N/A')

def recommend(movie):
    movie_index = movies[movies['movie_name'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_movies_name = []
    recommend_movies_poster = []
    recommend_movies_release = []
    recommend_movies_rating = []
    recommend_movies_Genre = []
    recommend_movies_Director = []
    recommend_movies_Stars = []
    
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies_poster.append(fetch_poster(movie_id))
        recommend_movies_name.append(movies.iloc[i[0]].movie_name)
        recommend_movies_release.append(release(movie_id))
        recommend_movies_rating.append(movies.iloc[i[0]].rating)
        recommend_movies_Genre.append(movies.iloc[i[0]].genre)
        recommend_movies_Director.append(movies.iloc[i[0]].directors)
        recommend_movies_Stars.append(movies.iloc[i[0]].stars)
    
    return recommend_movies_poster, recommend_movies_name, recommend_movies_Genre, recommend_movies_rating, recommend_movies_release, recommend_movies_Director, recommend_movies_Stars

# Streamlit app
st.title('Movie Recommender System')
option = st.selectbox('Select your Movie:', movies['movie_name'].values)
if st.button('Recommend'):
    rec_poster, rec_name, rec_genre, rec_rating, rec_release, rec_director, rec_stars = recommend(option)
    cols = st.columns(5)
    tabs = st.tabs(['Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie5'])
    for i, col in enumerate(cols):
        with col:
            st.image(rec_poster[i])
            st.write(f'<b style="color:yellow">{rec_name[i]}</b>', unsafe_allow_html=True)
    for i, tab in enumerate(tabs):
        with tab:
            st.write(f'<b style="color:red">Rating:</b> <b style="color:yellow">{rec_rating[i]}</b>', unsafe_allow_html=True)
            st.write(f'<b style="color:red">Genre:</b> <b style="color:yellow">{rec_genre[i]}</b>', unsafe_allow_html=True)
            st.write(f'<b style="color:red">Release:</b> <b style="color:yellow">{rec_release[i]}</b>', unsafe_allow_html=True)
            st.write(f'<b style="color:red">Director:</b> <b style="color:yellow">{rec_director[i]}</b>', unsafe_allow_html=True)
            st.write(f'<b style="color:red">Stars:</b> <b style="color:yellow">{rec_stars[i]}</b>', unsafe_allow_html=True)
