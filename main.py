"""Main file to run the bees algorithm on the pizza problem."""

from time import time
import numpy as np
import matplotlib.pyplot as plt

from bee_a_pizza.bees_algorithm.bees import bees_algorithm
from bee_a_pizza.import_export.import_pizzas import read_pizza_file
from bee_a_pizza.import_export.import_preferences import read_preferences_file
from bee_a_pizza.generators.order_generation import (
    generate_n_slices_per_customer,
    generate_preferences,
    get_preferences_by_slice,
)
from bee_a_pizza.bees_algorithm.solution_evaluation import get_cost
from bee_a_pizza.import_export.export import export_generated_customers

# load pizzas
pizzas, pizza_names, ingredient_names, pizza_prices = read_pizza_file("data/pizzas.csv")
print(pizzas.shape)

# generate slices
# n_slices = generate_n_slices_per_customer(min_slices=2, max_slices=5, n_customers=15)
# preferences = generate_preferences(
#     n_customers=15, n_ingredients=pizzas.shape[1], avg_likes=7, avg_dislikes=7
# )

n_slices, preferences = read_preferences_file("data/preferences.csv", ingredient_names)

slices = get_preferences_by_slice(preferences, n_slices)
print(slices.shape)

coefs = np.array([1, 2])

# solve
start = time()
result, solutions_list = bees_algorithm(
    pizzas=pizzas, slices=slices,
)
end = time()
# print(result)

export_generated_customers(
    pizzas=pizzas,
    n_slices_per_customers=n_slices,
    preferences=preferences,
    solution=result,
    pizza_names=pizza_names,
    ingredient_names=ingredient_names,
    customer_slices_filename="data/customers.csv",
    pizza_order_filename="data/order.csv",
)

print(pizza_names)
sum_result = np.sum(result, axis=0)
print(sum_result)

cost = get_cost(
    results=result,
    coefs=coefs,
    pizzas_ingredients=pizzas,
    preferences=slices,
)

all_margharitas = np.zeros(result.shape, dtype=int)
all_margharitas[:, 0] = 1
cost_all_margharitas = get_cost(
    results=all_margharitas,
    coefs=coefs,
    pizzas_ingredients=pizzas,
    preferences=slices,
)

print(f"cost = {cost}")
print(f"cost all margharitas = {cost_all_margharitas}")
print(f"Time = {end - start}")

cost_over_time = [
    get_cost(
        results=sol,
        coefs=coefs,
        pizzas_ingredients=pizzas,
        preferences=slices,
    )
    for sol in solutions_list
]

plt.plot(cost_over_time)
plt.show()
