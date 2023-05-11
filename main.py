from bee_a_pizza.bees_algorithm.bees import *
from bee_a_pizza.import_export.import_pizzas import *
from bee_a_pizza.generators.order_generation import *
from bee_a_pizza.bees_algorithm.solution_evaluation import *
import matplotlib.pyplot as plt
from time import time

# load pizzas
pizzas, pizza_names, ingredient_names, pizza_prices = read_pizza_file("data/Pizzas.csv")
print(pizzas.shape)

# generate slices
n_slices = generate_n_slices_per_customer(min_slices=2, max_slices=5, n_customers=15)
preferences = generate_preferences(
    n_customers=15, n_ingredients=pizzas.shape[1], avg_likes=7, avg_dislikes=7
)
slices = get_preferences_by_slice(preferences, n_slices)
print(slices.shape)
max_cost = 1000

coefs = np.array([1, 2])

# solve
start = time()
result, solutions_list = bees_algorithm(
    pizzas=pizzas,
    slices=slices,
    max_cost=max_cost,
    pizza_prices=np.array(pizza_prices),
)
end = time()
# print(result)

print(pizza_names)
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
