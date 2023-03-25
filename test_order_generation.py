import pytest
from order_generation import *


def test_generate_n_slices_per_customer():
    n_slices_per_customer = generate_n_slices_per_customer(
        min_slices=2,
        max_slices=5,
        n_customers=7
    )
    assert np.all((n_slices_per_customer >= 2) & (n_slices_per_customer <= 5))


def test_generate_preferences():
    with pytest.raises(ValueError):
        generate_preferences(
            n_customers=5,
            n_ingredients=0,
            avg_likes=0,
            avg_dislikes=0
        )

    with pytest.raises(ValueError):
        generate_preferences(
            n_customers=5,
            n_ingredients=5,
            avg_likes=3,
            avg_dislikes=3
        )

    preferences = generate_preferences(
        n_customers=5,
        n_ingredients=15,
        avg_likes=3,
        avg_dislikes=3
    )

    assert np.all((preferences >= -1) & (preferences <= 1))


