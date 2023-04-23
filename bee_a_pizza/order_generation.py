'''Generates random orders for the pizza shop.'''

import numpy as np


def generate_n_slices_per_customer(
    min_slices: int, max_slices: int, n_customers: int
) -> np.ndarray:
    """
    Randomly generates number of pizza slices desired by every customer.

    Parameters
    ----------
    `min_slices` : int
    `max_slices` : int
    `n_customers` : int

    Returns
    -------
    `n_slices_per_customer` : (n_customers)
    """
    return np.random.randint(
        low=min_slices, high=max_slices, size=n_customers, dtype="int8"
    )


def generate_preferences(
    n_customers: int, n_ingredients, avg_likes: int, avg_dislikes: int
) -> np.ndarray:
    """
    Randomly generates the ingredient preferences of customers.
    1 for liked ingredients
    0 for neutral ingredients
    -1 for disliked ingredients

    Parameters
    ----------
    `n_customers` : int
    `n_ingredients` : int
    `avg_likes` : int
    `avg_dislikes` : int

    Returns
    -------
    `preferences` : (n_customers, n_ingredients)
    """
    if (
        n_ingredients <= 0
        or avg_likes < 0
        or avg_dislikes < 0
        or n_ingredients < avg_likes + avg_dislikes
    ):
        raise ValueError

    distribution = np.random.randint(
        low=0, high=n_ingredients, size=(n_customers, n_ingredients), dtype="int32"
    )
    preferences = np.where(distribution < avg_dislikes, -1, 0)
    preferences = np.where(distribution >= n_ingredients - avg_likes, 1, preferences)

    return preferences


def assign_customers_to_slices(n_slices_per_customer: np.ndarray) -> np.ndarray:
    """
    Creates a vector of customer to slice assignment

    Parameters
    ----------
    `n_slices_per_customer` : (n_customers)

    Returns
    -------
    `slice_assignment` : (n_slices_total)
    """
    n_slices_total = np.sum(n_slices_per_customer)
    slice_assignment = np.zeros(n_slices_total, dtype="uint8")
    first_slice = 0
    last_slice = 0
    for customer, n_slices in enumerate(n_slices_per_customer):
        last_slice += n_slices
        slice_assignment[first_slice:last_slice] = customer
        first_slice = last_slice

    return slice_assignment


def get_preferences_by_slice(
    preferences: np.ndarray, n_slices_per_customer: np.ndarray
) -> np.ndarray:
    """
    Assigns customers' ingredient preferences to their assigned slices

    Parameters
    ----------
    `preferences` : (n_customers, n_ingredients)
    `n_slices_per_customer` : (n_customers)

    Returns
    -------
    `preferences_by_slice` : (n_slices_total, n_ingredients)
    """
    slice_assignment = assign_customers_to_slices(
        n_slices_per_customer=n_slices_per_customer
    )
    return preferences[slice_assignment]
