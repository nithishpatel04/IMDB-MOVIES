import streamlit as st
import pickle
import pandas as pd
import requests
import gzip

def load_compressed_pickle(filepath):
    with gzip.open(filepath, 'rb') as f:
        return pickle.load(f)

# Load the data
movies_df = pickle.load(open('new_movies_df.pkl', 'rb'))
movies = pd.DataFrame(movies_df)
similarity = load_compressed_pickle('similarity.pkl.gz')

def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=c4b3e35657228509f910bfe621114879&append_to_response=videos,images'.format(movie_id)
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']

def release(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=c4b3e35657228509f910bfe621114879'.format(movie_id)
    return requests.get(url).json()['release_date']

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
