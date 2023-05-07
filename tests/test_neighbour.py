import numpy as np
from bee_a_pizza.bees_algorithm.neighbors import swap_pizzas, swap_slices, get_neighbor


def test_swap_pizzas():
    size = 5
    results = np.eye(size, size)
    n_pizzas_to_change = 2
    n_slices_in_pizza = 2
    new_results = swap_pizzas(results, n_pizzas_to_change, n_slices_in_pizza)

    assert np.sum(new_results) == size
    assert np.sum(new_results, axis=1).max() == 1
    assert np.sum(new_results, axis=1).min() == 1


def test_swap_slices():
    size = 5
    results = np.eye(size, size)
    n_slices_to_swap = 2
    new_results = swap_slices(results, n_slices_to_swap)

    assert np.sum(new_results) == size
    assert np.sum(new_results, axis=1).max() == 1
    assert np.sum(new_results, axis=1).min() == 1


def test_get_neighbor():
    size = 5
    results = np.eye(size, size)
    search_cycle_proportion = 0.5
    new_results = get_neighbor(results, search_cycle_proportion)

    assert np.sum(new_results) == size
    assert np.sum(new_results, axis=1).max() == 1
    assert np.sum(new_results, axis=1).min() == 1
