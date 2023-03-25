import numpy as np


def generate_n_slices_per_customer(min_slices: int, max_slices: int, n_customers: int) -> np.ndarray:
    return np.random.randint(low=min_slices, high=max_slices, size=n_customers, dtype='int8')


def generate_preferences(n_customers: int, n_ingredients, avg_likes: int, avg_dislikes: int) -> np.ndarray:
    if n_ingredients <= 0 or avg_likes < 0 or avg_dislikes < 0 or n_ingredients < avg_likes + avg_dislikes:
        raise ValueError

    distribution = np.random.randint(low=0, high=n_ingredients, size=(n_customers, n_ingredients), dtype='int32')
    result = np.where(distribution < avg_dislikes, -1, 0)
    result = np.where(distribution >= n_ingredients - avg_likes, 1, result)

    return result