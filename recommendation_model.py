import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Global placeholders
movies = None
tfidf_matrix = None
cosine_sim = None

def load_data():
    global movies, tfidf_matrix, cosine_sim

    print("🔁 Loading dataset and building similarity model...")

    # Load the dataset
    movies = pd.read_csv('movies_with_features.csv')
    movies['title'] = movies['title'].str.strip()

    # Clean genres
    movies['genres'] = movies['genres'].fillna('unknown').str.lower().str.strip()

    # Extract year from title
    movies['year'] = movies['title'].apply(lambda x: re.search(r'\((\d{4})\)', x))
    movies['year'] = movies['year'].apply(lambda x: int(x.group(1)) if x else None)
    movies['year'] = movies['year'].fillna(0).astype(int)

    # Create decade column
    movies['decade'] = movies['year'].apply(lambda x: f"{(x // 10) * 10}s" if x > 0 else 'unknown')
    movies['decade'] = movies['decade'].str.lower()

    # Combine title and genres for TF-IDF
    movies['combined_features'] = movies['title'] + " " + movies['genres'].str.replace('|', ' ', regex=False)

    # TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(movies['combined_features'])

    # Cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    print("✅ Model loaded.")

def get_recommendations(selected_genre, selected_decade):
    global movies, tfidf_matrix, cosine_sim

    if movies is None or tfidf_matrix is None or cosine_sim is None:
        load_data()

    selected_genre = selected_genre.lower()
    selected_decade = selected_decade.lower()

    print("\n--- RECOMMENDATION REQUEST ---")
    print("Filtering for genre:", selected_genre)
    print("Filtering for decade:", selected_decade)

    # Filter movies by genre substring and decade
    filtered_movies = movies[
        (movies['genres'].str.contains(selected_genre, case=False)) &
        (movies['decade'] == selected_decade)
    ]
    print("Strict match count:", len(filtered_movies))

    # Fallback if no matches
    if filtered_movies.empty:
        filtered_movies = movies[movies['genres'].str.contains(selected_genre, case=False)]
        print("Fallback to genre-only match count:", len(filtered_movies))

    if filtered_movies.empty:
        print("Final result: no matches found.")
        return ["No matching movies found for that genre."]

    ref_idx = filtered_movies.index[0]
    filtered_indices = filtered_movies.index.tolist()

    sim_scores = [(i, cosine_sim[ref_idx][i]) for i in filtered_indices if i != ref_idx]
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sim_scores[:5]]
    print("Returning recommendations for:", movies.loc[ref_idx, 'title'])

    return movies['title'].iloc[top_indices].tolist()

# Optional test
if __name__ == "__main__":
    print("🧪 Running test:")
    recs = get_recommendations('drama', '1990s')
    print("🎬 Sample recommendations:", recs)
