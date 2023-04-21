import numpy as np


def swap_pizzas(results: np.ndarray, n_pizzas_to_change: int) -> np.ndarray:
    return results


def swap_slices(results: np.ndarray, n_slices_to_swap: int) -> np.ndarray:
    return results


def get_neighbor(results: np.ndarray, search_cycle_proportion: float, pizza_swap_proba: float = 0.5) -> np.ndarray:

    if np.random.rand(1) < pizza_swap_proba:
        n_pizzas_to_change = results.shape[0] * search_cycle_proportion // 1
        return swap_pizzas(results, n_pizzas_to_change)
    else:
        n_slices_to_swap = results.shape[0] * search_cycle_proportion // 1
        return swap_slices(results, n_slices_to_swap)
