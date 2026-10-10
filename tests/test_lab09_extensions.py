import pandas as pd

from inf8239_u03.metrics import catalog_coverage, hit_rate_at_k
from inf8239_u03.recommenders import MatrixFactorization


def test_empty_ranking_returns_zero():
    assert hit_rate_at_k({}, pd.DataFrame({"userId": [1], "movieId": [2]})) == 0
    assert catalog_coverage({}, 10) == 0


def test_cold_user_has_no_collaborative_scores(sample_ratings):
    model = MatrixFactorization(factors=2, seed=42).fit(sample_ratings, epochs=1)
    assert model.top_n(999999, set(), k=10).empty
