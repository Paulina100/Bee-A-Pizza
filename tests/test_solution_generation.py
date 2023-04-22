import pytest
from bee_a_pizza.solution_generation import *


def test_generate_greedy_solution():
    prices = 20 * np.random.random(50) + 10

    with pytest.raises(ValueError):
        generate_random_solution(
            n_slices=100,
            n_pizzas=50,
            n_slices_in_pizza=3,
            max_cost=20,
            pizza_prices=prices,
            random_state=0,
        )

    try:
        generate_random_solution(
            n_slices=100,
            n_pizzas=50,
            n_slices_in_pizza=3,
            max_cost=1200,
            pizza_prices=prices,
            random_state=0,
        )
        assert True
    except:
        assert False
