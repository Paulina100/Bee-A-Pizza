from math import inf

from bee_a_pizza.bees_algorithm.neighbors import get_neighbor
from bee_a_pizza.bees_algorithm.solution_generation import *


def local_search(
    pizzas: np.ndarray,
    slices: np.ndarray,
    coefs: np.ndarray,
    starting_solution: np.ndarray,
    foragers_n: int,
    search_cycle_proportion: float,
    pizza_swap_proba: float = 0.5,
):
    best_solution = starting_solution
    best_cost = get_cost(
        results=starting_solution,
        coefs=coefs,
        pizzas_ingredients=pizzas,
        preferences=slices,
    )
    for forager in range(foragers_n):
        neighbour = get_neighbor(
            results=starting_solution,
            search_cycle_proportion=search_cycle_proportion,
            pizza_swap_proba=pizza_swap_proba,
        )
        neighbour_cost = get_cost(
            results=neighbour,
            coefs=coefs,
            pizzas_ingredients=pizzas,
            preferences=slices,
        )
        if neighbour_cost < best_cost:
            best_solution = neighbour
            best_cost = neighbour_cost
    return best_solution, best_cost


def bees_algorithm(
    pizzas: np.ndarray,
    slices: np.ndarray,
    coefs: np.ndarray = np.array([1, 2]),
    scouts_n: int = 80,
    best_solutions_n: int = 50,
    elite_solutions_n: int = 10,
    best_foragers_n: int = 10,
    elite_foragers_n: int = 40,
    local_search_cycles: int = 8,
    generations: int = 125,
    pizza_swap_proba: float = 0.3,
):
    # initializing possible solutions
    possible_solutions = [
        generate_random_solution(
            n_slices=len(slices),
            n_pizzas=len(pizzas),
            n_slices_in_pizza=8,
        )
        for _ in range(scouts_n)
    ]

    # lists of: [solution, cost, search_cycle_n]
    possible_solutions = [
        [
            solution,
            get_cost(
                results=solution,
                coefs=coefs,
                pizzas_ingredients=pizzas,
                preferences=slices,
            ),
            0,
        ]
        for solution in possible_solutions
    ]
    best_solution_over_time = [0 for _ in range(generations)]
    best_cost = inf

    for gen in range(generations):
        # Recruitment
        possible_solutions.sort(key=lambda x: x[1], reverse=False)
        # Finding new best solution
        if possible_solutions[0][1] < best_cost:
            best_solution_over_time[gen] = possible_solutions[0][0]
            best_cost = possible_solutions[0][1]
        else:
            best_solution_over_time[gen] = best_solution_over_time[gen - 1]

        # local search
        for i in range(0, elite_solutions_n):
            new_solution = local_search(
                pizzas,
                slices,
                coefs,
                possible_solutions[i][0],
                elite_foragers_n,
                possible_solutions[i][2] / local_search_cycles,
                pizza_swap_proba,
            )
            if new_solution[1] < possible_solutions[i][1]:
                possible_solutions[i] = [new_solution[0], new_solution[1], 0]
            else:
                # neighbourhood shrinking
                possible_solutions[i][2] += 1
                if possible_solutions[i][2] == local_search_cycles:
                    # site abandonment
                    possible_solutions[i][1] = inf
        for i in range(elite_solutions_n, best_solutions_n):
            new_solution = local_search(
                pizzas,
                slices,
                coefs,
                possible_solutions[i][0],
                best_foragers_n,
                possible_solutions[i][2] / local_search_cycles,
                pizza_swap_proba,
            )
            if new_solution[1] < possible_solutions[i][1]:
                possible_solutions[i] = [new_solution[0], new_solution[1], 0]
            else:
                # neighbourhood shrinking
                possible_solutions[i][2] += 1
                if possible_solutions[i][2] == local_search_cycles:
                    # site abandonment
                    possible_solutions[i][1] = inf
        # global search
        for i in range(best_solutions_n, scouts_n):
            possible_solutions[i][0] = generate_random_solution(
                n_slices=len(slices),
                n_pizzas=len(pizzas),
                n_slices_in_pizza=8,
            )
            possible_solutions[i][1] = get_cost(
                results=possible_solutions[i][0],
                coefs=coefs,
                pizzas_ingredients=pizzas,
                preferences=slices,
            )
            possible_solutions[i][2] = 0

    # Finding new best solution
    possible_solutions.sort(key=lambda x: x[1], reverse=True)
    if possible_solutions[0][1] < best_cost:
        best_solution_over_time[generations - 1] = possible_solutions[0][0]

    return best_solution_over_time[generations - 1], best_solution_over_time
