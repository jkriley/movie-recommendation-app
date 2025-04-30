import pandas as pd
import random

# Load MovieLens data
df = pd.read_csv("ml-latest-small/movies.csv")

# Extract first genre
df['genre'] = df['genres'].apply(lambda x: x.split('|')[0] if isinstance(x, str) else 'Unknown')

# Generate random ratings between 3.0 and 5.0
df['avg_rating'] = [round(random.uniform(3.0, 5.0), 1) for _ in range(len(df))]

# Reorder and trim columns
df_final = df[['movieId', 'title', 'genre', 'avg_rating']]

# Export to new CSV
df_final.to_csv("real_movies.csv", index=False)

print("✅ real_movies.csv created with real titles and genres + fake ratings.")
