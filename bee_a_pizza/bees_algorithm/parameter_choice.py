from statistics import median_high
from bee_a_pizza.bees_algorithm.bees import *
from bee_a_pizza.import_export.import_pizzas import *
from bee_a_pizza.generators.order_generation import *
from bee_a_pizza.bees_algorithm.solution_evaluation import *
from math import inf

from time import time


def find_best_params_for_bees(
    pizzas: np.ndarray,
    slices: np.ndarray,
    coefs: np.ndarray,
    scouts_n: list,
    best_solutions_n: list,
    elite_solutions_n: list,
    best_foragers_n: list,
    elite_foragers_n: list,
    local_search_cycles: list,
    generations: list,
    pizza_swap_proba: list,
    best_params=None,
    best_cost=inf,
):
    params_to_optimize = [
        scouts_n,
        best_solutions_n,
        elite_solutions_n,
        best_foragers_n,
        elite_foragers_n,
        local_search_cycles,
        generations,
        pizza_swap_proba,
    ]
    if best_params is None:
        best_params = [median_high(param) for param in params_to_optimize]
    for i in range(len(params_to_optimize)):
        best_cost = inf
        print("Param ", i)
        param = params_to_optimize[i]
        for value in param:
            print("value ", value)
            old_value = best_params[i]
            if old_value == value:
                continue
            best_params[i] = value
            if (
                best_params[0] <= best_params[1]
                or best_params[1] <= best_params[2]
                or best_params[3] >= best_params[4]
            ):
                best_params[i] = old_value
                continue
            solution, l_sol = bees_algorithm(
                pizzas=pizzas,
                slices=slices,
                coefs=coefs,
                scouts_n=best_params[0],
                best_solutions_n=best_params[1],
                elite_solutions_n=best_params[2],
                best_foragers_n=best_params[3],
                elite_foragers_n=best_params[4],
                local_search_cycles=best_params[5],
                generations=best_params[6],
                pizza_swap_proba=best_params[7],
            )
            cost = get_cost(
                results=solution,
                coefs=coefs,
                pizzas_ingredients=pizzas,
                preferences=slices,
            )
            if cost < best_cost:
                best_cost = cost
            else:
                best_params[i] = old_value
        print("params: ", best_params)
        print("cost: ", best_cost)
    return best_params, best_cost


def find_best_coefs(
    pizzas: np.ndarray,
    slices: np.ndarray,
    coefs: np.ndarray,
    scouts_n: int,
    best_solutions_n: int,
    elite_solutions_n: int,
    best_foragers_n: int,
    elite_foragers_n: int,
    local_search_cycles: int,
    generations: int,
    pizza_swap_proba_n: float,
    best_coefs=None,
    best_cost=inf,
):
    if best_coefs is None:
        best_coefs = np.array([median_high(coef) for coef in coefs])

    for i in range(len(coefs)):
        best_cost = inf
        coef = coefs[i]
        print("Coef: ", i)
        print("Best coefs:", best_coefs)
        for value in coef:
            print("Value: ", value)
            old_value = best_coefs[i]
            if old_value == value:
                continue
            best_coefs[i] = value
            solution, l_sol = bees_algorithm(
                pizzas=pizzas,
                slices=slices,
                coefs=best_coefs,
                scouts_n=scouts_n,
                best_solutions_n=best_solutions_n,
                elite_solutions_n=elite_solutions_n,
                best_foragers_n=best_foragers_n,
                elite_foragers_n=elite_foragers_n,
                pizza_swap_proba=pizza_swap_proba_n,
                local_search_cycles=local_search_cycles,
                generations=generations,
            )
            cost = get_cost(
                results=solution,
                coefs=best_coefs,
                pizzas_ingredients=pizzas,
                preferences=slices,
            )
            if cost < best_cost:
                best_cost = cost
            else:
                best_coefs[i] = old_value
            print("coefs: ", best_coefs)
            print("cost: ", best_cost)
    return best_coefs, best_cost


# Tests
pizzas, pizza_names, ingredient_names, pizza_prices = read_pizza_file(
    "../../data/pizzas.csv"
)
print("Pizzas:", pizzas.shape)

n_slices = generate_n_slices_per_customer(min_slices=2, max_slices=5, n_customers=20)
preferences = generate_preferences(
    n_customers=20, n_ingredients=pizzas.shape[1], avg_likes=7, avg_dislikes=7
)
slices = get_preferences_by_slice(preferences, n_slices)
print("Slices:", slices.shape)

coefs = np.arange(1, 3)

start = time()
params = find_best_params_for_bees(
    pizzas=pizzas,
    slices=slices,
    coefs=coefs,
    scouts_n=list(range(40, 100, 10)),
    best_solutions_n=list(range(30, 70, 10)),
    elite_solutions_n=list(range(10, 60, 10)),
    best_foragers_n=list(range(5, 20, 5)),
    elite_foragers_n=list(range(10, 50, 10)),
    local_search_cycles=list(range(2, 10, 2)),
    generations=list((180, 200, 10)),
    pizza_swap_proba=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
    best_params=[80, 50, 20, 10, 30, 6, 180, 0.3],
)
end = time()
print("\nTime: ", end - start)
print("Best params:")
print(params)
# [70, 50, 20, 10, 30, 6, 180, 0.3]
# [60, 30, 10, 10, 30, 8, 200, 0.2]
# [90, 50, 10, 5, 40, 8, 200, 0.3]
# BEST PARAMETERS:
# [80, 50, 10, 10, 40, 8, 200, 0.3]
# coefs = np.array([1, 2])

# start = time()
# coefs = find_best_coefs(pizzas=pizzas,  slices=slices,
#     coefs=np.array([[1, 2, 3, 4], [1, 2, 3, 4]]),
#                           scouts_n=90, best_solutions_n=60, elite_solutions_n=40,
#                           best_foragers_n=10, elite_foragers_n=40, local_search_cycles=8,
#                           generations=120)
# end = time()
# print("\nTime: ", end - start)
# print("Best coefs:")
# print(coefs)
