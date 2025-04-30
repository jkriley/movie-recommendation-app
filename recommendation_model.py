import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
movies = pd.read_csv('real_movies.csv')

# Clean up movie titles
movies['title'] = movies['title'].str.strip()

# Fill missing description column if needed
if 'description' not in movies.columns:
    movies['description'] = 'Description not available'
movies['description'] = movies['description'].fillna('Description not available')

# If 'genre' column doesn't exist, create it
if 'genre' not in movies.columns:
    movies['genre'] = 'unknown'
else:
    movies['genre'] = movies['genre'].fillna('unknown').str.lower().str.strip()

# Extract year from title and convert to integer
movies['year'] = movies['title'].apply(lambda x: re.search(r'\((\d{4})\)', x))
movies['year'] = movies['year'].apply(lambda x: int(x.group(1)) if x else None)
movies['year'] = movies['year'].fillna(0).astype(int)

# Create a clean 'decade' column
movies['decade'] = movies['year'].apply(lambda x: f"{(x // 10) * 10}s" if x > 0 else 'unknown')
movies['decade'] = movies['decade'].str.lower()

# Create combined features column
movies['combined_features'] = movies['genre'] + " " + movies['description']

# Create the TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

# Calculate the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create a reverse mapping of movie titles to index
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

def get_recommendations(selected_genre, selected_decade):
    selected_genre = selected_genre.lower()
    selected_decade = selected_decade.lower()

    print("\n--- RECOMMENDATION REQUEST ---")
    print("Filtering for genre:", selected_genre)
    print("Filtering for decade:", selected_decade)

    # Filter by genre + decade first
    filtered_movies = movies[
        (movies['genre'] == selected_genre) &
        (movies['decade'] == selected_decade)
    ]
    print("Strict match count:", len(filtered_movies))

    # If no strict match, fallback to genre only
    if filtered_movies.empty:
        filtered_movies = movies[movies['genre'] == selected_genre]
        print("Fallback to genre-only match count:", len(filtered_movies))

    if filtered_movies.empty:
        print("Final result: no matches found.")
        return ["No matching movies found for that genre."]

    # Pick the first movie in filtered list as the reference
    ref_idx = filtered_movies.index[0]
    filtered_indices = filtered_movies.index.tolist()

    # Compare reference movie only to other filtered candidates
    sim_scores = [(i, cosine_sim[ref_idx][i]) for i in filtered_indices if i != ref_idx]
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sim_scores[:5]]
    print("Returning recommendations for:", movies.loc[ref_idx, 'title'])

    return movies['title'].iloc[top_indices].tolist()

# Optional debug/test output
if __name__ == "__main__":
    print("\n✅ Genre frequencies:")
    print(movies['genre'].value_counts())

    print("\n✅ Decade frequencies:")
    print(movies['decade'].value_counts())

    print("\n🎬 Sample recommendation:")
    print(get_recommendations('drama', '1990s'))
