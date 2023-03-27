from typing import Optional
import numpy as np
from bee_a_pizza.solution_evaluation import *


def generate_random_solution(
    n_slices: int,
    n_pizzas: int,
    n_slices_in_pizza: int,
    max_cost: float,
    pizza_prices: np.ndarray,
    random_state: Optional[int] = None
) -> np.ndarray:
    """
    Returns a random solution in form of a 0-1 matrix.

    Parameters
    ----------
    `n_slices` : int
    `n_pizzas` : int
    `n_slices_in_pizza` : int
    `max_cost` : float
    `pizza_prices` : (n_pizzas,)
    `random_state` : Optional[int]

    Returns
    -------
    `slices_pizzas` : (n_slices, n_pizzas)
    """
    np.random.seed(random_state)

    slices_pizzas = np.zeros((n_slices, n_pizzas))

    for _ in range(2 * n_slices * n_pizzas):
        indices = np.random.randint(np.zeros(n_slices), (n_pizzas-1)*np.ones(n_slices))
        slices_pizzas = get_slices_pizzas_from_indices(indices, n_pizzas)
        if is_pizzas_cost_leq_than_max_cost(
            slices_pizzas, n_slices_in_pizza, max_cost, pizza_prices
        ):
            break

    else:
        raise ValueError("Random solution not found - max_cost is too low")

    return slices_pizzas
