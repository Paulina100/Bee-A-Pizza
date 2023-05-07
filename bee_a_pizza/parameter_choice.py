import numpy as np
from statistics import median_high
from bees import bees_algorithm
from solution_evaluation import get_fitness
from bee_a_pizza.bees import *
from bee_a_pizza.pizza_calculator import *
from bee_a_pizza.order_generation import *
from bee_a_pizza.solution_evaluation import *
from math import inf

from time import time


def find_best_params_for_bees(pizzas: np.ndarray,
    slices: np.ndarray,
    max_cost: float,
    pizza_prices: np.ndarray,
    coefs: np.ndarray,
                     scouts_n: list, best_solutions_n: list, elite_solutions_n: list, best_foragers_n: list,
                     elite_foragers_n: list,
                     local_search_cycles: list, generations: list, best_params=None, best_fitness=inf):

    params_to_optimize = [scouts_n, best_solutions_n, elite_solutions_n, best_foragers_n, elite_foragers_n,
                          local_search_cycles, generations]
    if best_params is None:
        best_params = [median_high(param) for param in params_to_optimize]
    for i in range(len(params_to_optimize)):
        best_fitness = inf
        print('Param ', i)
        param = params_to_optimize[i]
        for value in param:
            print('value ', value)
            old_value = best_params[i]
            if old_value == value:
                continue
            best_params[i] = value
            if best_params[0] <= best_params[1] or best_params[1] <= best_params[2] or best_params[3] >= best_params[4]:
                best_params[i] = old_value
                continue
            solution, l_sol = bees_algorithm(pizzas=pizzas,
    slices=slices,
    max_cost=max_cost,
    pizza_prices=pizza_prices,
    coefs=coefs,
                                             scouts_n=best_params[0], best_solutions_n=best_params[1],
                                             elite_solutions_n=best_params[2],
                                             best_foragers_n=best_params[3], elite_foragers_n=best_params[4],
                                             local_search_cycles=best_params[5], generations=best_params[6])
            fitness = get_fitness(results=solution, coefs=coefs,
                                  pizzas_ingredients=pizzas,
                                  preferences=slices,)
            if fitness < best_fitness:
                best_fitness = fitness
            else:
                best_params[i] = old_value
        print('params: ', best_params)
        print('fitness: ', best_fitness)
    return best_params, best_fitness


def find_best_coefs(pizzas: np.ndarray,
    slices: np.ndarray,
    max_cost: float,
    pizza_prices: np.ndarray,
    coefs: np.ndarray,
                     scouts_n: int, best_solutions_n: int, elite_solutions_n: int, best_foragers_n: int,
                     elite_foragers_n: int,
                     local_search_cycles: int, generations: int, best_coefs=None, best_fitness=inf):
    if best_coefs is None:
        best_coefs = np.array([median_high(coef) for coef in coefs])

    for i in range(len(coefs)):
        best_fitness = inf
        coef = coefs[i]
        print("Coef: ", i)
        print("Best coefs:", best_coefs)
        for value in coef:
            print("Value: ", value)
            old_value = best_coefs[i]
            if old_value == value:
                continue
            best_coefs[i] = value
            solution, l_sol = bees_algorithm(pizzas=pizzas,
                                             slices=slices,
                                             max_cost=max_cost,
                                             pizza_prices=pizza_prices,
                                             coefs=best_coefs,
                                             scouts_n=scouts_n, best_solutions_n=best_solutions_n,
                                             elite_solutions_n=elite_solutions_n,
                                             best_foragers_n=best_foragers_n, elite_foragers_n=elite_foragers_n,
                                             local_search_cycles=local_search_cycles, generations=generations)
            fitness = get_fitness(results=solution, coefs=best_coefs,
                                  pizzas_ingredients=pizzas,
                                  preferences=slices, )
            if fitness < best_fitness:
                best_fitness = fitness
            else:
                best_coefs[i] = old_value
            print('coefs: ', best_coefs)
            print('fitness: ', best_fitness)
    return best_coefs, best_fitness


# Tests
pizzas, pizza_names, ingredient_names, pizza_prices = read_pizza_file(
    "../data/Pizzas.csv"
)
print("Pizzas:", pizzas.shape)

n_slices = generate_n_slices_per_customer(min_slices=2, max_slices=5, n_customers=7)
preferences = generate_preferences(
    n_customers=7, n_ingredients=pizzas.shape[1], avg_likes=5, avg_dislikes=5
)
slices = get_preferences_by_slice(preferences, n_slices)
print("Slices:", slices.shape)
max_cost = 1000

coefs = np.arange(1, 4)

start = time()
params = find_best_params_for_bees(pizzas=pizzas,  slices=slices,
    max_cost=max_cost,
    pizza_prices=np.array(pizza_prices),
    coefs=coefs,
                          scouts_n=list(range(70, 120, 10)), best_solutions_n=list(range(60, 90, 10)), elite_solutions_n=list(range(10, 80, 10)),
                          best_foragers_n=list(range(5, 20, 5)), elite_foragers_n=list(range(10, 50, 10)), local_search_cycles=list(range(2, 10, 2)),
                          generations=list((20, 120, 10)))
end = time()
print("\nTime: ", end - start)
print("Best params:")
print(params)

# start = time()
# coefs = find_best_coefs(pizzas=pizzas,  slices=slices,
#     max_cost=max_cost,
#     pizza_prices=np.array(pizza_prices),
#     coefs=np.array([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]),
#                           scouts_n=90, best_solutions_n=60, elite_solutions_n=40,
#                           best_foragers_n=10, elite_foragers_n=40, local_search_cycles=8,
#                           generations=120)
# end = time()
# print("\nTime: ", end - start)
# print("Best coefs:")
# print(coefs)
