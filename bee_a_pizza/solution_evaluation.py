"""Solution evaluation module."""

import numpy as np
from typing import Tuple


def get_slices_pizzas_likes_hates(
    pizzas_ingredients: np.ndarray, slices_ingredients_preference: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns a pair of matrices with pizza to slice fit values.

    Parameters
    ----------
    `pizzas_ingredients` : (n_pizzas, n_ingredients)
    `slices_ingredients_preference` : (n_slices, n_ingredients)

    Returns
    -------
    `slices_pizzas_likes` : (n_slices, n_pizzas)
    `slices_pizzas_hates` : (n_slices, n_pizzas)
    """
    slices_ingredients_likes = (slices_ingredients_preference > 0).astype(np.int8)
    slices_ingredients_hates = (slices_ingredients_preference < 0).astype(np.int8)

    slices_pizzas_likes = slices_ingredients_likes @ pizzas_ingredients.T
    slices_pizzas_hates = slices_ingredients_hates @ pizzas_ingredients.T

    return slices_pizzas_likes, slices_pizzas_hates


def get_number_of_positive_negative_matchings(
    slices_pizzas_likes: np.ndarray,
    slices_pizzas_hates: np.ndarray,
    slices_pizzas: np.ndarray,
) -> Tuple[int, int]:
    """
    Returns a number of positive and negative matchings of pizza to slices.

    Parameters
    ----------
    `slices_pizzas_likes` : (n_slices, n_pizzas)
    `slices_pizzas_hates` : (n_slices, n_pizzas)
    `slices_pizzas` : (n_slices, n_pizzas)

    Returns
    -------
    `n_positive_matchings` : int
    `n_negative_matchings` : int
    """
    n_positive_matchings = np.sum(slices_pizzas_likes * slices_pizzas)
    n_negative_matchings = np.sum(slices_pizzas_hates * slices_pizzas)
    return n_positive_matchings, n_negative_matchings


def get_number_of_pizza_types(
    slices_pizzas: np.ndarray, n_slices_in_pizza: int
) -> np.ndarray:
    """
    Returns a vector with number of whole pizzas.

    Parameters
    ----------
    `slices_pizzas` : (n_slices, n_pizzas)
    `n_slices_in_pizza` : int

    Returns
    -------
    `number_of_pizza_types` : (n_pizzas,)
    """
    return (np.sum(slices_pizzas, axis=0) + n_slices_in_pizza - 1) // n_slices_in_pizza


def get_cost_of_pizzas(
    slices_pizzas: np.ndarray, n_slices_in_pizza: int, pizza_prices: np.ndarray
) -> float:
    """
    Returns a sum of whole pizzas costs.

    Parameters
    ----------
    `slices_pizzas` : (n_slices, n_pizzas)
    `n_slices_in_pizza` : int
    `pizza_prices` : (n_pizzas,)

    Returns
    -------
    `cost_of_pizzas` : float
    """
    number_of_pizza_types = get_number_of_pizza_types(slices_pizzas, n_slices_in_pizza)
    return np.dot(number_of_pizza_types, pizza_prices)


def get_number_of_slices_non_forming_whole_pizza(
    slices_pizzas: np.ndarray, n_slices_in_pizza: int
) -> int:
    """
    Returns a number of slices that don't form a whole pizza.

    Parameters
    ----------
    `slices_pizzas` : (n_slices, n_pizzas)
    `n_slices_in_pizza` : int

    Returns
    -------
    `n_slices_not_in_pizza` : int
    """
    return np.sum(np.mod(np.sum(slices_pizzas, axis=0), n_slices_in_pizza))


def get_number_of_wasted_slices(
    slices_pizzas: np.ndarray, n_slices_in_pizza: int
) -> int:
    """
    Returns a number of unnecessarily wasted slices.

    Parameters
    ----------
    `slices_pizzas` : (n_slices, n_pizzas)
    `n_slices_in_pizza` : int

    Returns
    -------
    `n_wasted_slices` : int
    """

    n_slices_non_forming_whole_pizza_by_type = np.mod(
        np.sum(slices_pizzas, axis=0), n_slices_in_pizza
    )
    n_wasted_slices_by_type = np.where(
        n_slices_non_forming_whole_pizza_by_type > 0,
        n_slices_in_pizza - n_slices_non_forming_whole_pizza_by_type,
        0,
    )
    return np.sum(n_wasted_slices_by_type)


def get_slices_pizzas_from_indices(
    slices_pizzas_indices: np.ndarray, n_pizzas: int
) -> np.ndarray:
    """
    Returns a slices pizzas matrix from a vector of indices of pizzas.

    Parameters
    ----------
    `slices_pizzas_indices` : (n_slices,)
    `n_pizzas` : int

    Returns
    -------
    `slices_pizzas` : (n_slices, n_pizzas)
    """
    n_slices = slices_pizzas_indices.shape[0]
    slices_pizzas = np.zeros((n_slices, n_pizzas), dtype=np.int8)
    for i, j in enumerate(slices_pizzas_indices):
        slices_pizzas[i, j] = 1
    return slices_pizzas


def is_pizzas_cost_leq_than_max_cost(
    slices_pizzas: np.ndarray,
    n_slices_in_pizza: int,
    max_cost: float,
    pizza_prices: np.ndarray,
) -> bool:
    """
    Returns true if cost of pizzas is less than or equal the max_cost.

    Parameters
    ----------
    `slices_pizzas` : (n_slices, n_pizzas)
    `n_slices_in_pizza` : int
    `max_cost` : float
    `pizza_prices` : (n_pizzas,)
    """
    cost = get_cost_of_pizzas(slices_pizzas, n_slices_in_pizza, pizza_prices)
    return cost <= max_cost


def get_fitness(
    results: np.ndarray,
    coefs: np.ndarray,
    pizzas_ingredients: np.ndarray,
    preferences: np.ndarray,
    n_slices_in_pizza: int = 8,
) -> float:
    """
    Calculates fitness of the given solution, based on preferences and pizzas' ingredients.

    Parameters
    ----------
    `results` : (n_slices, n_pizzas) - solution of which fitness needs to be calculated
    `coefs` : (3) - array in form of [alpha, beta, gamma], where the values represent coefficients
        corresponding to the importance of: maximizing liked ingredients, minimizing disliked
        ingredients and minimizing food waste. Signs of coefs don't matter.
    `pizzas_ingredients` : (n_pizzas, n_ingredients)
    `preferences` : (n_slices, n_ingredients)
    `n_slices_in_pizza` : number of slices pizzas have
    """
    coefs = np.abs(coefs)
    coefs[0] *= -1

    slices_pizzas_likes, slices_pizzas_hates = get_slices_pizzas_likes_hates(
        pizzas_ingredients, preferences
    )
    (
        n_positive_matchings,
        n_negative_matchings,
    ) = get_number_of_positive_negative_matchings(
        slices_pizzas_likes, slices_pizzas_hates, results
    )
    n_wasted_slices = get_number_of_wasted_slices(results, n_slices_in_pizza)
    func_vals = np.array(
        [
            [n_positive_matchings],
            [n_negative_matchings],
            [n_wasted_slices],
        ]
    )

    return coefs @ func_vals
