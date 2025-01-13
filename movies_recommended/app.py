import streamlit as st
import pickle
import pandas as pd
import requests
import time

# Set the title of the page
st.title("Welcome to My Portfolio")

# Function to fetch movie posters from TMDb API with retry logic
def fetch_poster(movie_id):
    try:
        api_key = "8265bd1679663a7ea12ac168da84d2e8"  # TMDb API Key
        retries = 3  # Number of retries for the API request
        for _ in range(retries):
            try:
                # Send GET request with a 10-second timeout
                response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US", timeout=10)
                response.raise_for_status()  # Raise an exception for HTTP errors
                data = response.json()
                # Return poster URL if available, else return a placeholder
                if "poster_path" in data and data["poster_path"]:
                    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
                else:
                    return "https://via.placeholder.com/500x750?text=No+Image+Available"
            except requests.exceptions.RequestException as e:
                if _ < retries - 1:
                    time.sleep(2)  # Wait for 2 seconds before retrying
                else:
                    st.error(f"Error fetching poster: {e}")
                    return "https://via.placeholder.com/500x750?text=Error"
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


# Function to recommend movies based on similarity
def recommend(movie):
    try:
        # Find the index of the selected movie
        movie_index = movies[movies["title"] == movie].index[0]
        distances = similarity[movie_index]
        # Get the top 10 similar movies
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

        recommended_movies = []
        recommended_movies_posters = []
        for movie_tuple in movies_list:
            # Fetch movie title and poster
            movie_id = movies.iloc[movie_tuple[0]].movie_id
            recommended_movies.append(movies.iloc[movie_tuple[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("Movie not found in the dataset. Please select another movie.")
        return [], []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return [], []


# Load preprocessed data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit App
st.title("Movie Recommender System")

# Dropdown to select a movie
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies["title"].values
)







# Recommend button functionality
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    if names and posters:
        # Display movies in rows of 5
        for row_index in range(0, len(names), 5):
            cols = st.columns(5)
            for col_index, col in enumerate(cols):
                if row_index + col_index < len(names):
                    with col:
                        st.image(posters[row_index + col_index], use_container_width=True)
                        st.caption(names[row_index + col_index])


# Display a name
st.header("Krishnanmohan Kumar")

# Add an image
st.image("logo.jpg", caption="Krishanmohan Kumar")

# Add additional information
st.write("Hey Gyes ,"
         "My name is Krishanmohan Kumar and i am pursuing my bachelor's degree in Data Science  at Sri Balaji university pune .Now I`m working on movies "
         "Recommendation System "
         "Its a normal web page but i am try to improve it  .")
