import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
movies = pd.read_csv('beefed_up_movies_dataset_clean.csv')

# Fill any missing description fields with empty strings
movies['description'] = movies['description'].fillna('')

# Combine genre and description into a single feature
movies['combined_features'] = movies['genre'] + " " + movies['description']

# Create the TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

# Calculate the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create a reverse mapping of movie titles to index
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

def get_recommendations(selected_genre, selected_decade):
    # Try strict filter first (genre + decade)
    filtered_movies = movies[
        (movies['genre'].str.lower() == selected_genre.lower()) &
        (movies['decade'].str.lower() == selected_decade.lower())
    ]

    # If no strict matches, fallback to only genre
    if filtered_movies.empty:
        filtered_movies = movies[
            movies['genre'].str.lower() == selected_genre.lower()
        ]

    if filtered_movies.empty:
        return ["No matching movies found for that genre."]

    # Pick the first matching movie as a reference
    idx = filtered_movies.index[0]

    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get top 5 similar movies (excluding the reference movie itself)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]

    return movies['title'].iloc[movie_indices].tolist()
  # Get top 5 similar movies (excluding the reference movie

