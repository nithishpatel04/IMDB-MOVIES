#!/usr/bin/env python
# coding: utf-8

# In[1]:



import streamlit as st
import pickle
import pandas as pd
import requests
import base64



textColor="red"


# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://watchmingle.com/static/images/movies.jpeg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
  
    background-repeat: no-repeat;
    background-color: rgba(0,0,1,0,);
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)




def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=c4b3e35657228509f910bfe621114879&append_to_response=videos,images'.format(movie_id)
    data =requests.get(url)
    data1= data.json()
    poster_path = data1['poster_path']
    full_path = "https://image.tmdb.org/t/p/original/" + data1['poster_path']

    return full_path
def release(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=c4b3e35657228509f910bfe621114879'.format(movie_id)
    data = requests.get(url)
    data1 = data.json()
    release = data1['release_date']
    return release


def recommend(movie):
    movie_index = movies[movies['movie_name'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse =True,key=lambda x:x[1])[1:6]
    
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
        recommend_movies_rating.append(movies.iloc[i[0]].rating)
        recommend_movies_release.append(release(movie_id))
        recommend_movies_Genre.append(movies.iloc[i[0]].genre)

        recommend_movies_Director.append(movies.iloc[i[0]].directors)
        recommend_movies_Stars.append(movies.iloc[i[0]].stars)


    return recommend_movies_poster,recommend_movies_name, recommend_movies_Genre,recommend_movies_rating,recommend_movies_release, recommend_movies_Director,recommend_movies_Stars


movies_df = pickle.load(open('movies_df.pkl','rb'))
movies = pd.DataFrame(movies_df)

similarity = pickle.load(open('similarity.pkl','rb'))


st.title(':red[Movie Recommender System]')

option = st.selectbox('Select your Movie:', movies['movie_name'].values)

if st.button('Recommend'):
    recommend_movies_poster,recommend_movies_name,recommend_movies_Genre,recommend_movies_rating,recommend_movies_release, recommend_movies_Director,recommend_movies_Stars= recommend(option)
    
    col1,col2,col3,col4,col5= st.columns(5)
    col = [col1,col2,col3,col4,col5]


    for i in range(0, 5):

        with col[i]:


            st.write(f' <b style="color:yellow">{recommend_movies_name[i]} </b>',unsafe_allow_html=True)
            st.image(recommend_movies_poster[i])
             #st.write(f'<b style="color:red">Rating:</b> <b style="color:yellow">{recommend_movies_rating[i]}</b>', unsafe_allow_html=True)
             #st.write(f'<b style="color:red">Genre:</b> <b style="color:yellow">{recommend_movies_Genre[i]} <b> ', unsafe_allow_html=True)


    tab1,tab2,tab3,tab4,tab5= st.tabs(['Movie1','Movie2','Movie3','Movie4','Movie5'])
    tab = [tab1,tab2,tab3,tab4,tab5]

    for t in range(0,5):

        with tab[t]:


            st.write(f'<b style="color:red">Rating:</b> <b style="color:yellow">{recommend_movies_rating[t]}</b>', unsafe_allow_html=True)
            st.write(f'<b style="color:red">Genre:</b> <b style="color:yellow">{recommend_movies_Genre[t]} <b> ',unsafe_allow_html=True)
            st.write(f'<b style="color:red">Release:</b> <b style="color:yellow">{recommend_movies_release[t]}</b>',
                      unsafe_allow_html=True)
            st.write(f'<b style="color:red">Director:</b> <b style="color:yellow">{recommend_movies_Director[t]} <b> ',
                      unsafe_allow_html=True)
            st.write(f'<b style="color:red">Stars:</b> <b style="color:yellow">{recommend_movies_Stars[t]}</b>',
                      unsafe_allow_html=True)





        # with col[t]:
         #    st.write(f'<b style="color:red">Rating:</b> <b style="color:yellow">{recommend_movies_rating[t]}</b>', unsafe_allow_html=True)
          #   st.write(f'<b style="color:red">Genre:</b> <b style="color:yellow">{recommend_movies_Genre[t]} <b> ',
           #       unsafe_allow_html=True)


        # with col2:

         #    st.write(f' <b style="color:#E50914">{recommend_movies_name[1]} </b>', unsafe_allow_html=True)
          #   st.image(recommend_movies_poster[1])
           #  st.write(f'<b style="color:">Rating:</b> <b style="color:yellow">{recommend_movies_rating[1]}</b>',
            #      unsafe_allow_html=True)
             #st.write(f'<b style="color:#DB4437">Genre:</b> <b style="color:yellow">{recommend_movies_Genre[1]} <b> ',
              #   unsafe_allow_html=True)


# In[ ]:




