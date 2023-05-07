import pytest
from bee_a_pizza.generators.order_generation import *


def test_generate_n_slices_per_customer():
    n_slices_per_customer = generate_n_slices_per_customer(
        min_slices=2, max_slices=5, n_customers=7
    )
    assert np.all((n_slices_per_customer >= 2) & (n_slices_per_customer <= 5))


def test_generate_preferences():
    with pytest.raises(ValueError):
        generate_preferences(
            n_customers=5, n_ingredients=0, avg_likes=0, avg_dislikes=0
        )

    with pytest.raises(ValueError):
        generate_preferences(
            n_customers=5, n_ingredients=5, avg_likes=3, avg_dislikes=3
        )

    preferences = generate_preferences(
        n_customers=5, n_ingredients=15, avg_likes=3, avg_dislikes=3
    )

    assert np.all((preferences >= -1) & (preferences <= 1))


def test_assign_customers_to_slices():
    n_slices_per_customer = np.array([2, 3, 1])
    slice_assignment = assign_customers_to_slices(
        n_slices_per_customer=n_slices_per_customer
    )

    assert np.all(slice_assignment == [0, 0, 1, 1, 1, 2])


def test_get_preferences_by_slice():
    preferences = np.array([[1, 1, -1], [0, 0, 1], [-1, 0, -1]])
    n_slices_per_customer = np.array([2, 3, 1])
    expected_preferences_by_slice = np.array(
        [[1, 1, -1], [1, 1, -1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [-1, 0, -1]]
    )
    preferences_by_slice = get_preferences_by_slice(
        preferences=preferences, n_slices_per_customer=n_slices_per_customer
    )

    assert np.all(preferences_by_slice == expected_preferences_by_slice)
