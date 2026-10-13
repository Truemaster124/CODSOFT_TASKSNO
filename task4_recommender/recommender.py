# Task 4 - Simple movie recommendation system
# Two approaches are implemented:
#   1. content based  - recommend movies with similar genres to one you liked
#   2. collaborative  - recommend movies liked by users who rate like you
# The data is a small hand-made dataset so the script runs without downloads.

import math

# movie -> list of genres
MOVIES = {
    "Inception":            ["sci-fi", "thriller", "action"],
    "Interstellar":         ["sci-fi", "drama", "adventure"],
    "The Matrix":           ["sci-fi", "action"],
    "The Dark Knight":      ["action", "crime", "thriller"],
    "Avengers: Endgame":    ["action", "adventure", "sci-fi"],
    "3 Idiots":             ["comedy", "drama"],
    "Dangal":               ["drama", "sports", "biography"],
    "Zindagi Na Milegi Dobara": ["comedy", "drama", "adventure"],
    "Andhadhun":            ["thriller", "comedy", "crime"],
    "Drishyam":             ["thriller", "crime", "drama"],
    "Lagaan":               ["drama", "sports", "musical"],
    "PK":                   ["comedy", "sci-fi", "drama"],
    "Titanic":              ["romance", "drama"],
    "The Notebook":         ["romance", "drama"],
    "Jab We Met":           ["romance", "comedy"],
    "Shutter Island":       ["thriller", "mystery"],
    "Gone Girl":            ["thriller", "mystery", "crime"],
    "Toy Story":            ["animation", "comedy", "adventure"],
    "Coco":                 ["animation", "musical", "adventure"],
    "Chhichhore":           ["comedy", "drama"],
}

# Fictional example users -> {movie: rating out of 5}
RATINGS = {
    "Aman":   {"Inception": 5, "Interstellar": 5, "The Matrix": 4, "The Dark Knight": 5, "3 Idiots": 3},
    "Riya":   {"3 Idiots": 5, "Dangal": 4, "Zindagi Na Milegi Dobara": 5, "Chhichhore": 5, "Jab We Met": 4},
    "Karan":  {"Andhadhun": 5, "Drishyam": 5, "Shutter Island": 4, "Gone Girl": 5, "The Dark Knight": 4},
    "Sneha":  {"Titanic": 5, "The Notebook": 5, "Jab We Met": 5, "3 Idiots": 4, "Coco": 3},
    "Vikram": {"Inception": 4, "Avengers: Endgame": 5, "The Matrix": 5, "Interstellar": 4, "PK": 3},
    "Pooja":  {"Toy Story": 5, "Coco": 5, "Chhichhore": 4, "PK": 4, "Zindagi Na Milegi Dobara": 4},
    "Rahul":  {"Lagaan": 5, "Dangal": 5, "3 Idiots": 5, "PK": 5, "Drishyam": 3},
    "Meera":  {"Gone Girl": 4, "Shutter Island": 5, "Drishyam": 4, "Andhadhun": 4, "Inception": 3},
}


def cosine(a, b):
    """cosine similarity between two dicts (sparse vectors)"""
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[k] * b[k] for k in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ---------- content based ----------

def genre_vector(movie):
    return {g: 1 for g in MOVIES[movie]}


def similar_movies(title, n=5):
    if title not in MOVIES:
        return None
    target = genre_vector(title)
    scored = []
    for other in MOVIES:
        if other == title:
            continue
        scored.append((cosine(target, genre_vector(other)), other))
    scored.sort(reverse=True)
    return scored[:n]


# ---------- collaborative filtering ----------

def recommend_for_user(user, n=5, k=3):
    """User based CF: find the k most similar users, then predict ratings
    for movies the target user hasn't rated using a weighted average."""
    if user not in RATINGS:
        return None

    my_ratings = RATINGS[user]

    neighbours = []
    for other, their_ratings in RATINGS.items():
        if other == user:
            continue
        sim = cosine(my_ratings, their_ratings)
        if sim > 0:
            neighbours.append((sim, other))
    neighbours.sort(reverse=True)
    neighbours = neighbours[:k]

    weighted_sum = {}
    sim_sum = {}
    for sim, other in neighbours:
        for movie, rating in RATINGS[other].items():
            if movie in my_ratings:
                continue
            weighted_sum[movie] = weighted_sum.get(movie, 0) + sim * rating
            sim_sum[movie] = sim_sum.get(movie, 0) + sim

    predictions = [(weighted_sum[m] / sim_sum[m], m) for m in weighted_sum]
    predictions.sort(reverse=True)
    return predictions[:n], neighbours


# ---------- small command line menu ----------

def menu():
    print("=== Movie Recommender ===")
    while True:
        print("\n1. Movies similar to one I liked (content based)")
        print("2. Recommendations for a user (collaborative)")
        print("3. List movies")
        print("4. List users")
        print("5. Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Movie title: ").strip()
            # let the user type in any case
            lookup = {m.lower(): m for m in MOVIES}
            title = lookup.get(title.lower(), title)
            result = similar_movies(title)
            if result is None:
                print("I don't have that movie. Pick one from option 3.")
            else:
                print(f"\nBecause you liked {title}:")
                for score, m in result:
                    print(f"  {m}  (similarity {score:.2f})")

        elif choice == "2":
            name = input("User name: ").strip().capitalize()
            result = recommend_for_user(name)
            if result is None:
                print("Unknown user. Pick one from option 4.")
            else:
                preds, neighbours = result
                print(f"\nUsers with similar taste to {name}: " +
                      ", ".join(f"{u} ({s:.2f})" for s, u in neighbours))
                if not preds:
                    print("Nothing new to recommend.")
                for score, m in preds:
                    print(f"  {m}  (predicted rating {score:.1f}/5)")

        elif choice == "3":
            for m, g in MOVIES.items():
                print(f"  {m} - {', '.join(g)}")

        elif choice == "4":
            print("  " + ", ".join(RATINGS))

        elif choice == "5":
            break
        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    try:
        menu()
    except (EOFError, KeyboardInterrupt):
        print("\nRecommender closed.")
