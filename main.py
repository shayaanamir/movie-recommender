import pickle
import requests
import streamlit as st

data = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
api_key = st.secrets["api_key"]


def fetchPoster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}?api_key={api_key}&language=en-US"
    movie_data = requests.get(url)
    movie_data = movie_data.json()
    print(movie_data)
    poster_path = movie_data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + str(poster_path)

    return full_path


def recommendMovies(movie):
    movie = movie.lower()
    recommendedMovies = []
    recommendedMoviePosters = []
    if movie not in data['movie_title'].unique():
        print("Movie not found!")
    else:
        index = data[data['movie_title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
        for i in distances[1:11]:
            movie_id= data.iloc[i[0]]['movie_id']
            recommendedMovies.append(data.iloc[i[0]]['movie_title'].upper())
            recommendedMoviePosters.append(fetchPoster(movie_id))
    return recommendedMovies, recommendedMoviePosters


def main():
    st.title("Hello")

    selected_movie = st.selectbox('Search movies...', data["movie_title"].values, )
    if st.button('Recommend'):
        movieNames, moviePosters = recommendMovies(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5,gap='medium', vertical_alignment='bottom')
        with col1:
            st.text(movieNames[0])
            st.image(moviePosters[0])
        with col2:
            st.text(movieNames[1])
            st.image(moviePosters[1])

        with col3:
            st.text(movieNames[2])
            st.image(moviePosters[2])
        with col4:
            st.text(movieNames[3])
            st.image(moviePosters[3])
        with col5:
            st.text(movieNames[4])
            st.image(moviePosters[4])

main()