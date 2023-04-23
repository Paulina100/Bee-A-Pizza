import numpy as np


def swap_pizzas(results: np.ndarray, n_pizzas_to_change: int) -> np.ndarray:
    return results


def swap_slices(results: np.ndarray, n_slices_to_swap: int) -> np.ndarray:
    return results


def get_neighbor(
    results: np.ndarray, search_cycle_proportion: float, pizza_swap_proba: float = 0.5
) -> np.ndarray:
    """
    Returns a neighbor of the given solution generated either by swap_pizzas() or swap_slices(), chosen randomly

    Parameters
    ----------
    `results` : (n_slices, n_pizzas)
    `search_cycle_proportion` : float (0 - 1) - decides how distant the neighbor is, relative to the current solution
        (i.e. 1 means all slices/pizzas need to be swapped, 0.5 means only 50% of them needs to be swapped)
    `pizza_swap_proba` : probability of choosing swap_pizzas() over swap_slices()
    """
    if np.random.rand(1) < pizza_swap_proba:
        n_pizzas_to_change = int(results.shape[0] * search_cycle_proportion)
        return swap_pizzas(results, n_pizzas_to_change)
    else:
        n_slices_to_swap = int(results.shape[0] * search_cycle_proportion)
        return swap_slices(results, n_slices_to_swap)
