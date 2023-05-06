from typing import Optional
import numpy as np
from bee_a_pizza.solution_evaluation import *


def generate_random_solution(
    n_slices: int,
    n_pizzas: int,
    n_slices_in_pizza: int,
    random_state: Optional[int] = None,
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

    n_types_to_choose = np.ceil(n_slices / n_slices_in_pizza).astype(int)

    slices_pizzas = np.zeros((n_slices, n_pizzas))

    chosen_types = np.random.randint(0, n_pizzas, n_types_to_choose)
    chosen_types = np.array(
        [[chosen_types[i]] * n_slices_in_pizza for i in range(n_types_to_choose)]
    )
    chosen_types = chosen_types.reshape(n_types_to_choose * n_slices_in_pizza)
    chosen_types = chosen_types[:n_slices]
    np.random.shuffle(chosen_types)

    slices_pizzas[np.arange(n_slices), chosen_types] = 1

    return slices_pizzas
