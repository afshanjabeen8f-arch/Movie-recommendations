import streamlit as st

from recommender import (
    load_recommender,
    get_movie_titles,
    recommend_movies,
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Movie Recommendation Engine",
    page_icon="🎬",
    layout="wide",
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 0;
        }

        .subtitle {
            font-size: 18px;
            color: #666;
            margin-top: 5px;
            margin-bottom: 30px;
        }

        .movie-card {
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #ddd;
            margin-bottom: 12px;
            background-color: #fafafa;
        }

        .movie-title {
            font-size: 20px;
            font-weight: 600;
        }

        .movie-info {
            color: #555;
            margin-top: 5px;
        }

        .similarity {
            font-size: 14px;
            color: #777;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🎬 Movie Recommendation Engine</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Find movies similar to your favorite movie using TF-IDF and cosine similarity."
    "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Load recommender
# ---------------------------------------------------------

try:
    movies, tfidf_matrix, cosine_similarity_matrix = load_recommender()

except FileNotFoundError as error:
    st.error(str(error))

    st.info(
        "Please download the MovieLens ml-latest-small dataset and place it "
        "inside the data/ml-latest-small/ folder."
    )

    st.stop()

except Exception as error:
    st.error(f"Something went wrong while loading the dataset: {error}")
    st.stop()


movie_titles = get_movie_titles(movies)


# ---------------------------------------------------------
# Movie selection
# ---------------------------------------------------------

st.subheader("Choose a movie")

selected_movie = st.selectbox(
    "Search for a movie",
    movie_titles,
    index=None,
    placeholder="Start typing a movie title...",
)

recommend_button = st.button(
    "🍿 Get Recommendations",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# Recommendation results
# ---------------------------------------------------------

if recommend_button:

    if selected_movie is None:
        st.warning("Please select a movie first.")
        st.stop()

    recommendations = recommend_movies(
        selected_movie=selected_movie,
        movies=movies,
        tfidf_matrix=tfidf_matrix,
        cosine_similarity_matrix=cosine_similarity_matrix,
        number_of_recommendations=10,
    )

    st.markdown("---")

    st.subheader(f"Movies similar to **{selected_movie}**")

    if recommendations.empty:
        st.warning("No recommendations were found.")
        st.stop()

    # Display recommendations in two columns
    columns = st.columns(2)

    for index, (_, movie) in enumerate(recommendations.iterrows()):

        with columns[index % 2]:

            title = movie["title"]
            genres = movie["genres"]
            rating = movie["rating"]
            rating_count = movie["rating_count"]
            similarity = movie["similarity"]

            if rating_count > 0:
                rating_text = (
                    f"⭐ {rating:.2f}/5 "
                    f"({rating_count} ratings)"
                )
            else:
                rating_text = "⭐ No rating available"

            st.markdown(
                f"""
                <div class="movie-card">
                    <div class="movie-title">
                        {index + 1}. {title}
                    </div>

                    <div class="movie-info">
                        🎭 {genres}
                    </div>

                    <div class="movie-info">
                        {rating_text}
                    </div>

                    <div class="similarity">
                        Content similarity: {similarity:.1%}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------
# About section
# ---------------------------------------------------------

with st.expander("ℹ️ How does this recommendation system work?"):

    st.write(
        """
        This application uses a content-based recommendation approach.

        Each movie is represented using its title and genres. These text
        features are converted into numerical vectors using TF-IDF
        (Term Frequency-Inverse Document Frequency).

        Cosine similarity is then used to measure how similar two movies
        are in the resulting vector space.

        The application returns the 10 movies with the highest similarity
        score to the selected movie.

        Movie ratings shown in the results come from the MovieLens ratings.csv
        file and are displayed as additional information. They are not used
        to calculate the content similarity.
        """
    )

    st.caption(
        f"Dataset contains {len(movies):,} movies."
    )

st.markdown("---")

st.caption(
    "Built with Python • Pandas • Scikit-learn • Streamlit • MovieLens"
)