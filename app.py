import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
matrix = pickle.load(open("matrix.pkl", 'rb'))
movies_list = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2d7a21abc11c217b1ae86dfcbba131ef&language=en-US'.format(movie_id))
    d = response.json()
    return "http://image.tmdb.org/t/p/w500/"+d['poster_path']


def recommend(movie):
    movie_idx = movies_list[movies_list['title'] == movie].index[0]
    dist = matrix[movie_idx]
    movies = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters=[]
    for i in movies:
        movie_id = movies_list.iloc[i[0]].id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


st.header("Movie Recommender System")
st.text('by Harsh Prajapati')
selected_movie_name = st.selectbox(
    'type your favourite movie',
    movies_list['title'].values)
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5  =st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col1:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])