from bee_a_pizza.bees_algorithm.solution_generation import *


def test_generate_random_solution():
    result = generate_random_solution(
        n_slices=100,
        n_pizzas=50,
        n_slices_in_pizza=3,
        random_state=0,
    )
    assert np.all(np.sum(result, axis=1) == np.ones(100))
    assert np.sum(np.sum(result, axis=0) > 0) <= np.ceil(100 / 3)
