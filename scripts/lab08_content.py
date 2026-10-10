import sys

from inf8239_u03.config import MOVIELENS_DIR, ROOT
from inf8239_u03.data import load_movielens
from inf8239_u03.recommenders import ContentRecommender, weighted_popularity

DEFAULT_TITLES = [
    "Toy Story (1995)",
    "Shawshank Redemption, The (1994)",
    "Matrix, The (1999)",
]

ratings, movies = load_movielens(MOVIELENS_DIR)
reports = ROOT / "reports"
reports.mkdir(exist_ok=True)

popular = weighted_popularity(ratings, movies).head(10)
popular[["title", "count", "mean", "weighted_score"]].to_csv(reports / "popular_top10.csv")
print("Popularidad:\n", popular[["title", "count", "mean", "weighted_score"]])

titles = sys.argv[1:] or DEFAULT_TITLES
model = ContentRecommender().fit(movies)

for i, title in enumerate(titles, start=1):
    recommendations = model.recommend_or_popular(title, popular, 10)
    recommendations.to_csv(reports / f"content_recommendations_{i}.csv", index=False)
    if recommendations["source"].eq("popularidad").all():
        print(f"\nTítulo no encontrado: {title}. Respaldo con el Top-10 de popularidad:\n", recommendations)
    else:
        print(f"\nSimilares a {title}:\n", recommendations)