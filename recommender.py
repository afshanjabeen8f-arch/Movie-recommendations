from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data" / "ml-latest-small"

MOVIES_FILE = DATA_DIR / "movies.csv"
RATINGS_FILE = DATA_DIR / "ratings.csv"


# ---------------------------------------------------------
# Load and prepare data
# ---------------------------------------------------------

def load_data():
    """
    Load MovieLens movies and ratings data.

    Returns
    -------
    movies : pandas.DataFrame
        Movie information including title, genres, and ratings.
    """

    if not MOVIES_FILE.exists():
        raise FileNotFoundError(
            f"Could not find movies.csv at:\n{MOVIES_FILE}\n\n"
            "Please download the MovieLens ml-latest-small dataset "
            "and place it inside data/ml-latest-small/."
        )

    if not RATINGS_FILE.exists():
        raise FileNotFoundError(
            f"Could not find ratings.csv at:\n{RATINGS_FILE}\n\n"
            "Please download the MovieLens ml-latest-small dataset "
            "and place it inside data/ml-latest-small/."
        )

    movies = pd.read_csv(MOVIES_FILE)
    ratings = pd.read_csv(RATINGS_FILE)

    # -----------------------------------------------------
    # Calculate average movie ratings
    # -----------------------------------------------------

    rating_summary = (
        ratings.groupby("movieId")["rating"]
        .agg(["mean", "count"])
        .reset_index()
    )

    rating_summary.rename(
        columns={
            "mean": "rating",
            "count": "rating_count",
        },
        inplace=True,
    )

    # -----------------------------------------------------
    # Merge ratings with movie information
    # -----------------------------------------------------

    movies = movies.merge(
        rating_summary,
        on="movieId",
        how="left",
    )

    # Some movies may not have a rating.
    movies["rating"] = movies["rating"].fillna(0)
    movies["rating_count"] = movies["rating_count"].fillna(0)

    # -----------------------------------------------------
    # Clean text fields
    # -----------------------------------------------------

    movies["title"] = movies["title"].fillna("")
    movies["genres"] = movies["genres"].fillna("")

    # Convert pipe-separated genres to normal text.
    movies["genres_text"] = movies["genres"].str.replace(
        "|",
        " ",
        regex=False,
    )

    # -----------------------------------------------------
    # Create content field
    # -----------------------------------------------------

    # The title is repeated so it has slightly more influence
    # than an individual genre token.
    movies["content"] = (
        movies["title"] + " "
        + movies["title"] + " "
        + movies["genres_text"]
    )

    return movies


# ---------------------------------------------------------
# Build TF-IDF model
# ---------------------------------------------------------

def build_tfidf_model(movies):
    """
    Convert movie titles and genres into TF-IDF vectors.

    Returns
    -------
    tfidf_matrix : sparse matrix
        TF-IDF representation of every movie.
    vectorizer : TfidfVectorizer
        The fitted TF-IDF vectorizer.
    """

    vectorizer = TfidfVectorizer(
        stop_words="english",
        lowercase=True,
        ngram_range=(1, 2),
    )

    tfidf_matrix = vectorizer.fit_transform(
        movies["content"]
    )

    return tfidf_matrix, vectorizer


# ---------------------------------------------------------
# Build cosine similarity matrix
# ---------------------------------------------------------

def build_similarity_matrix(tfidf_matrix):
    """
    Calculate cosine similarity between all movies.
    """

    return cosine_similarity(tfidf_matrix)


# ---------------------------------------------------------
# Load complete recommender
# ---------------------------------------------------------

def create_recommender():
    """
    Load data and build the complete recommendation model.
    """

    movies = load_data()

    tfidf_matrix, _ = build_tfidf_model(movies)

    cosine_similarity_matrix = build_similarity_matrix(
        tfidf_matrix
    )

    return (
        movies,
        tfidf_matrix,
        cosine_similarity_matrix,
    )


# ---------------------------------------------------------
# Get cached recommender
# ---------------------------------------------------------

def load_recommender():
    """
    Streamlit-friendly cached loader.

    The model is built once and reused between Streamlit
    interactions.
    """

    import streamlit as st

    @st.cache_resource
    def _load():
        return create_recommender()

    return _load()


# ---------------------------------------------------------
# Get movie titles
# ---------------------------------------------------------

def get_movie_titles(movies):
    """
    Return movie titles sorted alphabetically.
    """

    return movies["title"].sort_values().tolist()


# ---------------------------------------------------------
# Find selected movie
# ---------------------------------------------------------

def find_movie_index(selected_movie, movies):
    """
    Find the DataFrame index corresponding to a movie title.

    Returns
    -------
    int
        Index of the selected movie.
    """

    matches = movies.index[
        movies["title"] == selected_movie
    ].tolist()

    if not matches:
        raise ValueError(
            f"Movie '{selected_movie}' was not found."
        )

    return matches[0]


# ---------------------------------------------------------
# Generate recommendations
# ---------------------------------------------------------

def recommend_movies(
    selected_movie,
    movies,
    tfidf_matrix,
    cosine_similarity_matrix,
    number_of_recommendations=10,
):
    """
    Return movies most similar to the selected movie.

    Parameters
    ----------
    selected_movie : str
        Movie title selected by the user.

    movies : pandas.DataFrame
        MovieLens movie data.

    tfidf_matrix :
        TF-IDF representation of movies.

    cosine_similarity_matrix :
        Pairwise cosine similarity matrix.

    number_of_recommendations : int
        Number of movies to return.

    Returns
    -------
    pandas.DataFrame
        Recommended movies with similarity and rating information.
    """

    selected_index = find_movie_index(
        selected_movie,
        movies,
    )

    # Get similarity scores for the selected movie.
    similarity_scores = list(
        enumerate(
            cosine_similarity_matrix[selected_index]
        )
    )

    # Sort from highest similarity to lowest.
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True,
    )

    recommendations = []

    for movie_index, similarity_score in similarity_scores:

        # Skip the selected movie itself.
        if movie_index == selected_index:
            continue

        recommendations.append(
            {
                "movie_index": movie_index,
                "similarity": float(similarity_score),
            }
        )

        if len(recommendations) >= number_of_recommendations:
            break

    # -----------------------------------------------------
    # Convert recommendation indexes to movie rows
    # -----------------------------------------------------

    recommendation_indexes = [
        item["movie_index"]
        for item in recommendations
    ]

    result = movies.loc[
        recommendation_indexes,
        [
            "movieId",
            "title",
            "genres",
            "rating",
            "rating_count",
        ],
    ].copy()

    similarity_by_index = {
        item["movie_index"]: item["similarity"]
        for item in recommendations
    }

    result["similarity"] = [
        similarity_by_index[index]
        for index in result.index
    ]

    # Make sure results appear in similarity order.
    result = result.sort_values(
        "similarity",
        ascending=False,
    )

    return result.reset_index(drop=True)