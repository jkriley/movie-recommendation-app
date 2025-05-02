import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv('movies.csv')

# Rename column for consistency if needed (or just reference 'genres' directly)
# movies.rename(columns={'genres': 'genre'}, inplace=True)

# Combine genres with title for modeling
movies['combined_features'] = movies['title'] + ' ' + movies['genres'].str.replace('|', ' ', regex=False)

# Create TF-IDF matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

# Compute similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create title-to-index mapping
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

movies.to_csv('movies.csv', index=False)


