import sys

try:
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ModuleNotFoundError as e:
    print(f"Missing dependency: {e.name}")
    print("Install required packages with:")
    print("    pip install pandas scikit-learn")
    sys.exit(1)

# ----------------------
# SAMPLE DATA
# ----------------------
movies = pd.DataFrame({
    'movie_id': [1, 2, 3, 4, 5],
    'title': [
        'The Matrix',
        'The Lord of the Rings',
        'The Avengers',
        'Inception',
        'Interstellar'
    ],
    'genres': [
        'Action Sci-Fi',
        'Adventure Fantasy',
        'Action Superhero',
        'Sci-Fi Thriller',
        'Sci-Fi Drama'
    ]
})

# ----------------------
# CONTENT-BASED FILTERING
# ----------------------
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(movies['genres'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_movies_content(movie_title, num_recommendations=3):
    """Return a list of recommended movies (title + genres) similar to movie_title.

    This function is case-insensitive and raises a clear error if the title is missing.
    """
    matches = movies[movies['title'].str.lower() == movie_title.lower()]
    if matches.empty:
        raise ValueError(f"Movie '{movie_title}' not found in the dataset.")

    idx = matches.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] != idx][:num_recommendations]
    return movies.iloc[[s[0] for s in sim_scores]][['title', 'genres']].to_dict('records')

# ----------------------
# COLLABORATIVE FILTERING (USER-ITEM MATRIX)
# ----------------------
ratings = pd.DataFrame({
    'user_id': [1, 1, 1, 2, 2, 3, 3, 4],
    'movie_id': [1, 2, 3, 2, 4, 1, 5, 3],
    'rating':  [5, 4, 4, 5, 3, 4, 5, 4]
})

user_item_matrix = ratings.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)
user_similarity = cosine_similarity(user_item_matrix)

def recommend_movies_collaborative(user_id, num_recommendations=3):
    """Recommend movies for a user based on the most similar other user.

    Uses the user-item rating matrix. The function handles non-contiguous user IDs by
    mapping user_id to the pivot table index with get_loc().
    """
    if user_id not in user_item_matrix.index:
        raise ValueError(f"User id {user_id} not found in ratings data.")

    user_idx = user_item_matrix.index.get_loc(user_id)
    sim_scores = list(enumerate(user_similarity[user_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # find nearest neighbor (skip self)
    neighbors = [i for i, s in sim_scores if i != user_idx]
    if not neighbors:
        return []

    top_neighbor_idx = neighbors[0]
    neighbor_user_id = user_item_matrix.index[top_neighbor_idx]

    user_movies = set(ratings[ratings['user_id'] == user_id]['movie_id'])
    neighbor_ratings = ratings[ratings['user_id'] == neighbor_user_id]

    candidates = neighbor_ratings[~neighbor_ratings['movie_id'].isin(user_movies)]
    if candidates.empty:
        return []

    candidates = candidates.sort_values(by='rating', ascending=False).head(num_recommendations)
    return movies[movies['movie_id'].isin(candidates['movie_id'])][['title', 'genres']].to_dict('records')

# ----------------------
# Example usage
# ----------------------
if __name__ == "__main__":
    print("Content-based recommendations for 'Inception':")
    try:
        recs = recommend_movies_content('Inception', num_recommendations=2)
        for r in recs:
            print(f"- {r['title']} ({r['genres']})")
    except ValueError as e:
        print(e)

    print ("Collaborative recommendations for user 1:")
    try:
        recs = recommend_movies_collaborative(1, num_recommendations=2)
        for r in recs:
            print(f"- {r['title']} ({r['genres']})")
    except ValueError as e:
        print(e)
