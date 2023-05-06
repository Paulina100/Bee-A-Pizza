from bee_a_pizza.bees import *
from bee_a_pizza.pizza_calculator import *
from bee_a_pizza.order_generation import *
from bee_a_pizza.solution_evaluation import *
import matplotlib.pyplot as plt
from time import time

pizzas, pizza_names, ingredient_names, pizza_prices = read_pizza_file(
    "../data/Pizzas.csv"
)
print(pizzas.shape)

n_slices = generate_n_slices_per_customer(min_slices=2, max_slices=5, n_customers=7)
preferences = generate_preferences(
    n_customers=7, n_ingredients=pizzas.shape[1], avg_likes=5, avg_dislikes=5
)
slices = get_preferences_by_slice(preferences, n_slices)
print(slices.shape)
max_cost = 1000

coefs = np.arange(1, 3)

start = time()
result, solutions_list = bees_algorithm(
    pizzas=pizzas,
    slices=slices,
    max_cost=max_cost,
    pizza_prices=np.array(pizza_prices),
    coefs=coefs,
    scouts_n=100,
    best_solutions_n=80,
    elite_solutions_n=30,
    best_foragers_n=5,
    elite_foragers_n=10,
    local_search_cycles=5,
    generations=100,
)
end = time()
print(result)

sum_result = np.sum(result, axis=0)
print(sum_result)

fitness = get_fitness(
    results=result,
    coefs=coefs,
    pizzas_ingredients=pizzas,
    preferences=slices,
)[0]

all_margharitas = np.zeros(result.shape, dtype=int)
all_margharitas[:, 0] = 1
fitness_all_margharitas = get_fitness(
    results=all_margharitas,
    coefs=coefs,
    pizzas_ingredients=pizzas,
    preferences=slices,
)[0]

print(f"Fitness = {fitness}")
print(f"Fitness all margharitas = {fitness_all_margharitas}")
print(f"Time = {end - start}")

fitness_over_time = [
    get_fitness(
        results=sol,
        coefs=coefs,
        pizzas_ingredients=pizzas,
        preferences=slices,
    )
    for sol in solutions_list
]

plt.plot(fitness_over_time)
plt.show()
