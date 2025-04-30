import pandas as pd
import random

# Load your real dataset
movies = pd.read_csv('real_movies.csv')

# Define a set of demo genres
sample_genres = ['action', 'drama', 'comedy', 'horror', 'sci-fi']

# Replace or create the 'genre' column with random choices
movies['genre'] = [random.choice(sample_genres) for _ in range(len(movies))]

# Save it as a new file (or overwrite, if you're brave)
movies.to_csv('real_movies.csv', index=False)

print("✅ Random genres added to dataset.")
