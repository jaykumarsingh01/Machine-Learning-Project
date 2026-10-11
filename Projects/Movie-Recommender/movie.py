import pickle
import streamlit as st
import requests
import pandas as pd


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0b0f19, #111827);
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        margin-top: 20px;
        margin-bottom: 5px;
        color: white;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #a7b0c0;
        font-size: 18px;
        margin-bottom: 35px;
    }

    /* Section heading */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: white;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Movie title */
    .movie-title {
        text-align: center;
        color: white;
        font-size: 16px;
        font-weight: 600;
        min-height: 48px;
        padding-top: 10px;
        line-height: 1.4;
    }

    /* Recommendation button */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 48px;
        font-size: 17px;
        font-weight: 700;
        border: none;
    }

    /* Select box */
    div[data-baseweb="select"] {
        border-radius: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 14px;
        margin-top: 60px;
        padding-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------- FUNCTIONS ----------------

def fetch_poster(movie_id):

    url = (
        "https://api.themoviedb.org/3/movie/{}"
        "?api_key=8265bd1679663a7ea12ac168da84d2e8"
        "&language=en-US"
    ).format(movie_id)

    response = requests.get(url)

    data = response.json()

    if 'poster_path' not in data or data['poster_path'] is None:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    poster_path = data['poster_path']

    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path


def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:

        # Actual TMDB movie ID
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_movie_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_movie_posters


# ---------------- LOAD DATA ----------------

movies_dict = pickle.load(
    open('movie_dict.pkl', 'rb')
)

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(
    open('similarity.pkl', 'rb')
)


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">🎬 Movie Recommender System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover movies similar to your favorites'
    '</div>',
    unsafe_allow_html=True
)


# ---------------- MOVIE SELECTION ----------------

st.markdown(
    '<div class="section-title">🎥 Choose a movie</div>',
    unsafe_allow_html=True
)

selected_movie_name = st.selectbox(
    "Select a movie you like",
    movies['title'].values
)


# ---------------- RECOMMEND BUTTON ----------------

recommend_button = st.button(
    "✨ Recommend Movies"
)


# ---------------- RECOMMENDATIONS ----------------

if recommend_button:

    names, posters = recommend(selected_movie_name)

    st.markdown(
        '<div class="section-title">🍿 Recommended For You</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(
        5,
        gap="medium"
    )

    columns = [col1, col2, col3, col4, col5]

    for col, name, poster in zip(
        columns,
        names,
        posters
    ):

        with col:

            st.image(
                poster,
                width="stretch"
            )

            st.markdown(
                f'<div class="movie-title">{name}</div>',
                unsafe_allow_html=True
            )


# ---------------- FOOTER ----------------

st.markdown(
    '<div class="footer">'
    '🎬 Movie Recommender System • Powered by Machine Learning & TMDB'
    '</div>',
    unsafe_allow_html=True
)