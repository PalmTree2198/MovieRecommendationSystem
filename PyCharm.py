import streamlit as st
import pickle
import pandas as pd  # Import pandas for DataFrame
import requests

def fetch_poster(movie_id):
    api_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=de807812701c180170ecde28387bd450&append_to_response=videos"
    response = requests.get(api_url)
    data = response.json()

    return "https://image.tmdb.org/t/p/w500" + data['poster_path']  # Complete poster path

def recommend(movie):
    # Convert movies_list to a DataFrame
    movies_df = pd.read_pickle('movie_list.pkl')

    # Find the index of the selected movie
    index = movies_df[movies_df['title'] == movie].index[0]

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    # Create a list of recommended movies
    recommended_movies = []

    # Create list of poster paths
    recommended_movies_posters = []
    for i in distances[1:6]:
        movie_id = movies_df.iloc[i[0]].movie_id

        # Finding the name of the movies and adding them to the empty list
        recommended_movies.append(movies_df.iloc[i[0]].title)

        # Fetch poster from API, calling the function to get the poster of the movie
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data and similarity scores
movies_df = pd.read_pickle('movie_list.pkl')
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Title of the website
st.markdown("<h1 style='color: lightblue; font-size: 36px; font-weight: bold; font-family: Arial, sans-serif;'>Movie Recommendation System</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='color: grey; font-family: Arial, sans-serif; font-size: 20px;'>Select a movie type:</h2>", unsafe_allow_html=True)
option = st.selectbox(
    label=" ",
    options=movies_df['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(option)

    # Displaying the name of the movie along with its poster
    # Create a loop to generate the columns
    num_columns = 5  # Number of columns
    col_width = st.columns(num_columns)

    for i in range(num_columns):
        with col_width[i]:
            # Name
            st.markdown(f"<h2 style='color: lightgreen; font-family: Arial, sans-serif;font-size: 20px; '>{names[i]}</h2>", unsafe_allow_html=True)

            # Poster
            st.image(posters[i])
