import pytest
from bee_a_pizza.solution_evaluation import *


def test_get_slices_pizzas_likes_hates():
    pizzas_ingredients = np.array(
        [
            [1, 0, 0, 1],
            [1, 1, 0, 0],
            [0, 1, 1, 1],
            [1, 1, 1, 0],
            [0, 1, 1, 0],
            [1, 0, 1, 1],
        ],
        dtype=np.int8,
    )

    slices_ingredients_preference = np.array(
        [
            [-1, 1, 0, 1],
            [1, -1, -1, -1],
            [1, 1, -1, -1],
            [-1, -1, -1, 1],
            [-1, 1, 1, -1],
        ],
        dtype=np.int8,
    )

    correct_likes = np.array(
        [
            [1, 1, 2, 1, 1, 1],
            [1, 1, 0, 1, 0, 1],
            [1, 2, 1, 2, 1, 1],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 2, 2, 2, 1],
        ]
    )

    correct_hates = np.array(
        [
            [1, 1, 0, 1, 0, 1],
            [1, 1, 3, 2, 2, 2],
            [1, 0, 2, 1, 1, 2],
            [1, 2, 2, 3, 2, 2],
            [2, 1, 1, 1, 0, 2],
        ]
    )

    likes, hates = get_slices_pizzas_likes_hates(
        pizzas_ingredients, slices_ingredients_preference
    )

    assert np.all(likes == correct_likes)
    assert np.all(hates == correct_hates)


def test_get_number_of_pizza_types():
    slices_pizzas = np.array(
        [
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
        ],
        dtype=np.int8,
    )
    assert np.all(
        get_number_of_pizza_types(slices_pizzas, 1) == np.array([4, 1, 0, 3, 0])
    )
    assert np.all(
        get_number_of_pizza_types(slices_pizzas, 2) == np.array([2, 1, 0, 2, 0])
    )
    assert np.all(
        get_number_of_pizza_types(slices_pizzas, 3) == np.array([2, 1, 0, 1, 0])
    )
    assert np.all(
        get_number_of_pizza_types(slices_pizzas, 4) == np.array([1, 1, 0, 1, 0])
    )


def test_get_cost_of_pizzas():
    slices_pizzas = np.array(
        [
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
        ],
        dtype=np.int8,
    )
    prices = np.array([35, 40, 10, 60, 28])
    assert get_cost_of_pizzas(slices_pizzas, 1, prices) == 360
    assert get_cost_of_pizzas(slices_pizzas, 2, prices) == 230
    assert get_cost_of_pizzas(slices_pizzas, 3, prices) == 170
    assert get_cost_of_pizzas(slices_pizzas, 4, prices) == 135


def test_get_number_of_positive_negative_matchings():
    likes = np.array(
        [
            [1, 1, 2, 1, 1, 1],
            [1, 1, 0, 1, 0, 1],
            [1, 2, 1, 2, 1, 1],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 2, 2, 2, 1],
        ]
    )
    hates = np.array(
        [
            [1, 1, 0, 1, 0, 1],
            [1, 1, 3, 2, 2, 2],
            [1, 0, 2, 1, 1, 2],
            [1, 2, 2, 3, 2, 2],
            [2, 1, 1, 1, 0, 2],
        ]
    )
    slices_pizzas = np.array(
        [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
        ]
    )
    assert get_number_of_positive_negative_matchings(likes, hates, slices_pizzas) == (
        3,
        9,
    )


def test_get_slices_pizzas_from_indices():
    assert np.all(
        get_slices_pizzas_from_indices(np.array([0, 0, 0, 0, 0], np.int8), 4)
        == np.array(
            [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]
        )
    )
    assert np.all(
        get_slices_pizzas_from_indices(np.array([1, 0, 2, 0, 3], np.int8), 4)
        == np.array(
            [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]]
        )
    )


def test_get_number_of_slices_non_forming_whole_pizza():
    slices_pizzas = np.array(
        [
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
        ],
        dtype=np.int8,
    )
    assert get_number_of_slices_non_forming_whole_pizza(slices_pizzas, 1) == 0
    assert get_number_of_slices_non_forming_whole_pizza(slices_pizzas, 2) == 2
    assert get_number_of_slices_non_forming_whole_pizza(slices_pizzas, 3) == 2
    assert get_number_of_slices_non_forming_whole_pizza(slices_pizzas, 4) == 4


def test_get_number_of_wasted_slices():
    slices_pizzas = np.array(
        [
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
        ],
        dtype=np.int8,
    )
    slices_pizzas2 = np.array(
        [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
        ]
    )
    assert get_number_of_wasted_slices(slices_pizzas, 1) == 0
    assert get_number_of_wasted_slices(slices_pizzas, 2) == 2
    assert get_number_of_wasted_slices(slices_pizzas, 3) == 4
    assert get_number_of_wasted_slices(slices_pizzas, 4) == 4

    assert get_number_of_wasted_slices(slices_pizzas2, 8) == 27


def test_get_fitness():
    results = np.array(
        [
            [1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1],
        ]
    )
    coefs = np.array([1, 1, 1])
    pizzas_ingredients = np.array(
        [
            [1, 0, 0, 1],
            [1, 1, 0, 0],
            [0, 1, 1, 1],
            [1, 1, 1, 0],
            [0, 1, 1, 0],
            [1, 0, 1, 1],
        ],
        dtype=np.int8,
    )

    preferences = np.array(
        [
            [-1, 1, 0, 1],
            [1, -1, -1, -1],
            [1, 1, -1, -1],
            [-1, -1, -1, 1],
            [-1, 1, 1, -1],
        ],
        dtype=np.int8,
    )

    n_likes = 3
    n_hates = 9
    n_wasted_slices = 27
    result = get_fitness(results, coefs, pizzas_ingredients, preferences)

    assert result == -3 + 9 + 27
