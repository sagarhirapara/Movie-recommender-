import streamlit as st
import pickle
import pandas as pd
import requests


def get_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=efba9760083631cd07be4e76f45f42a2&language=en-US".format(movie_id))
    data = dict(response.json())
    return "https://www.themoviedb.org/t/p/w600_and_h900_bestv2" + data['poster_path']


movies = pd.DataFrame(pickle.load(open("movies_list.pkl", "rb")))
similarity = pickle.load(open("simlarity.pkl", 'rb'))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[movie_index]))
    dist = sorted(distances, key=lambda x: x[1], reverse=True)
    final_name = []
    # for fetching poster
    recommend_movies_poster = []
    for i in range(1, 6):
        recommend_movies_poster.append(get_poster(
            int(movies['movie_id'].iloc[int(dist[i][0])])))
        final_name.append(movies['title'].iloc[int(dist[i][0])])
    return final_name, recommend_movies_poster


movies_list = movies['title'].values

st.title("movies recommended system")
movie_name = st.selectbox('Select your movies', movies_list)

if st.button('Recommend'):
    final_name, posters = recommend(movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(final_name[0])
        st.image(posters[0])

    with col2:
        st.text(final_name[1])
        st.image(posters[1])

    with col3:
        st.text(final_name[2])
        st.image(posters[2])

    with col4:
        st.text(final_name[3])
        st.image(posters[3])
    with col5:
        st.text(final_name[4])
        st.image(posters[4])
