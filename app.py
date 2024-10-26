import streamlit as st
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Remove background image setting

API_KEY = 'd4a267e87212b1218509323158cfe737'  # Your TMDB API key

@st.cache_data
def get_movie_poster(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                return poster_url
    return "https://via.placeholder.com/150"  # Default placeholder if not found

@st.cache_data
def load_data():
    return pickle.load(open('movie_data.pkl', 'rb'))

@st.cache_data
def load_tfidf():
    return pickle.load(open('tfidf_matrix.pkl', 'rb'))

@st.cache_data
def load_vectorizer():
    return pickle.load(open('tfidf_vectorizer.pkl', 'rb'))

df = load_data()
tfidf_matrix = load_tfidf()
tf = load_vectorizer()

cosine_similar = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_movie_name_from_index(index):
    return df[df.index == index]["movie_name"].values[0]

def get_index_from_movie_name(movie_name):
    return df[df.movie_name == movie_name]["index"].values[0]

st.title(":red[Movie Recommendation System]")
st.write("Select a movie to find similar movies:")

# Use a selectbox for the movie selection
movie_user_likes = st.selectbox("Movie Name", df['movie_name'].values)

if st.button("Find Similar Movies"):
    if movie_user_likes:
        poster_url = get_movie_poster(movie_user_likes)
        if poster_url:
            st.image(poster_url, width=200)
        else:
            st.write("Poster not found.")

        try:
            movie_index = get_index_from_movie_name(movie_user_likes)
            similar_movies = list(enumerate(cosine_similar[movie_index]))
            sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

            st.write(f"Top 10 similar movies to **{movie_user_likes}** are:")
            cols = st.columns(5)  # Create five columns for layout
            for i, element in enumerate(sorted_similar_movies):
                if i >= 10:
                    break
                with cols[i % 5]:  # Cycle through the columns
                    movie_name = get_movie_name_from_index(element[0])
                    st.write(f"<b style='color: yellow'>{movie_name}</b>", unsafe_allow_html=True)
                    st.image(get_movie_poster(movie_name), width=100)  # Fetch and show poster for each movie
        except IndexError:
            st.write("Movie not found in the database. Please check the name.")
    else:
        st.write("Please select a movie.")
