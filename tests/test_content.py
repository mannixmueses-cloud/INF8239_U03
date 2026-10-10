from inf8239_u03.recommenders import ContentRecommender, weighted_popularity


def test_content_excludes_query_and_returns_unique_items(sample_movies):
    result = ContentRecommender().fit(sample_movies).recommend("Alpha", 3)
    assert "Alpha" not in set(result["title"])
    assert result["movieId"].is_unique


def test_unknown_title_falls_back_to_popularity(sample_ratings, sample_movies):
    popular = weighted_popularity(sample_ratings, sample_movies, quantile=0.0)
    model = ContentRecommender().fit(sample_movies)
    result = model.recommend_or_popular("Pelicula Inventada (2030)", popular, 3)
    assert result["source"].eq("popularidad").all()
    assert result["movieId"].tolist() == popular.index[:3].tolist()
    assert model.recommend_or_popular("Alpha", popular, 3)["source"].eq("contenido").all()


def test_popularity_contains_weighted_score(sample_ratings, sample_movies):
    result = weighted_popularity(sample_ratings, sample_movies, quantile=0.0)
    assert "weighted_score" in result.columns
