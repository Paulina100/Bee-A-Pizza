from solution_generation import *


def find_neighbour(solution: np.ndarray, pizzas: np.ndarray, search_cycle_proportion: float) -> np.ndarray:
    pass


def local_search(pizzas: np.ndarray, slices: np.ndarray, max_cost: float, pizza_prices: np.ndarray,
                 starting_solution: np.array, foragers_n: int, search_cycle_proportion: float):

    best_solution = starting_solution
    best_fitness = calculate_fitness(solution=starting_solution, pizzas=pizzas, slices=slices,
                                     max_cost=max_cost, pizza_prices=pizza_prices)
    for forager in range(foragers_n):
        neighbour = find_neighbour(solution=starting_solution, pizzas=pizzas,
                                   search_cycle_proportion=search_cycle_proportion)
        neighbour_fitness = calculate_fitness(solution=neighbour, pizzas=pizzas,
                                              slices=slices, max_cost=max_cost, pizza_prices=pizza_prices)
        if neighbour_fitness > best_fitness:
            best_solution = neighbour
            best_fitness = neighbour_fitness
    return best_solution, best_fitness


def calculate_fitness(solution: np.ndarray, pizzas: np.ndarray, slices: np.ndarray,
                      max_cost: float, pizza_prices: np.ndarray) -> int:
    pass


# pizzas - array [n,m] n - 0/1 tam gdzie są składniki, m - liczba pizz w menu
# slices - array [n,m] n - -1/0/1 tam gdzie są składniki, m - liczba sliców, które chcemy otrzymać
def bees_algorithm(pizzas: np.ndarray, slices: np.ndarray, max_cost: float, pizza_prices: np.ndarray,
                   scouts_n: int, best_solutions_n: int, elite_solutions_n: int, best_foragers_n: int,
                   elite_foragers_n: int,
                   local_search_cycles: int, generations: int):

    # initializing possible solutions
    possible_solutions = [generate_random_solution(n_slices=len(slices), n_pizzas=len(pizzas),
                                                   n_slices_in_pizza=8, max_cost=max_cost, pizza_prices=pizza_prices)]
    # lists of: [solution, fitness, search_cycle_n]
    possible_solutions = [[solution, calculate_fitness(solution=solution, pizzas=pizzas, slices=slices,
                                                       max_cost=max_cost, pizza_prices=pizza_prices), 0]
                          for solution in possible_solutions]

    best_solution_over_time = [0 for _ in range(generations)]
    best_fitness = -1

    for gen in range(generations):
        # Recruitment
        possible_solutions.sort(key=lambda x: x[1], reverse=True)
        # Finding new best solution
        if possible_solutions[0][1] > best_fitness:
            best_solution_over_time[gen] = possible_solutions[0][0]
            best_fitness = possible_solutions[0][1]
        else:
            best_solution_over_time[gen] = best_solution_over_time[gen - 1]

        # local search
        for i in range(0, elite_solutions_n):
            new_solution = local_search(pizzas, slices, max_cost, pizza_prices, possible_solutions[i][0],
                                        elite_foragers_n, possible_solutions[i][2] / local_search_cycles)
            if new_solution[1] > possible_solutions[i][1]:
                possible_solutions[i] = [new_solution[0], new_solution[1], 0]
            else:
                # neighbourhood shrinking
                possible_solutions[i][2] += 1
                if possible_solutions[i][2] == local_search_cycles:
                    # site abandonment
                    possible_solutions[i][1] = 0
        for i in range(elite_solutions_n, best_solutions_n):
            new_solution = local_search(pizzas, slices, max_cost, pizza_prices, possible_solutions[i][0],
                                        best_foragers_n, possible_solutions[i][2] / local_search_cycles)
            if new_solution[1] > possible_solutions[i][1]:
                possible_solutions[i] = [new_solution[0], new_solution[1], 0]
            else:
                # neighbourhood shrinking
                possible_solutions[i][2] += 1
                if possible_solutions[i][2] == local_search_cycles:
                    # site abandonment
                    possible_solutions[i][1] = 0
        # global search
        for i in range(best_solutions_n, scouts_n):
            possible_solutions[i][0] = generate_random_solution(n_slices=len(slices), n_pizzas=len(pizzas),
                                                                n_slices_in_pizza=8, max_cost=max_cost,
                                                                pizza_prices=pizza_prices)
            possible_solutions[i][1] = calculate_fitness(solution=possible_solutions[i][0], pizzas=pizzas,
                                                         slices=slices, max_cost=max_cost, pizza_prices=pizza_prices)
            possible_solutions[i][2] = 0

    # Finding new best solution
    possible_solutions.sort(key=lambda x: x[1], reverse=True)
    if possible_solutions[0][1] > best_fitness:
        best_solution_over_time[generations - 1] = possible_solutions[0][0]

    return best_solution_over_time[generations - 1], best_solution_over_time
