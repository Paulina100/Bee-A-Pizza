"""Exports results to csv as a sheet with pizza assigned to customers and
a sheet with pizza order list"""

from collections import Counter
import csv
import numpy as np


def export_generated_customers(
    pizzas: np.ndarray,
    n_slices_per_customers: np.ndarray,
    preferences: np.ndarray,
    solution: np.ndarray,
    pizza_names: list[str],
    ingredient_names: list[str],
    customer_slices_filename: str,
    pizza_order_filename: str,
):
    n_pizzas, n_ingredients = pizzas.shape
    n_customers = len(n_slices_per_customers)
    n_slices = sum(n_slices_per_customers)

    slices_customer = [0] * n_slices
    i = 0
    for customer, n_slices_per_customer in enumerate(n_slices_per_customers):
        for _ in range(n_slices_per_customer):
            slices_customer[i] = customer
            i += 1

    slices_pizza = [0] * n_slices
    for slice, pizza in np.argwhere(solution != 0):
        slices_pizza[slice] = pizza

    customers_pizzas = [Counter[int]() for _ in range(n_customers)]
    for customer, pizza in zip(slices_customer, slices_pizza):
        customers_pizzas[customer][pizza] += 1

    pizzas_with_count = sum(customers_pizzas, Counter[int]())
    pizza_names_with_count = list(
        map(
            lambda pizza__count: (pizza_names[pizza__count[0]], pizza__count[1]),
            pizzas_with_count.items(),
        )
    )

    customers_likes = [list[int]() for _ in range(n_customers)]
    for customer, ingredient_liked in np.argwhere(preferences > 0):
        customers_likes[customer].append(ingredient_liked)

    customers_hates = [list[int]() for _ in range(n_customers)]
    for customer, ingredient_hated in np.argwhere(preferences < 0):
        customers_hates[customer].append(ingredient_hated)

    pizzas_ingredients = [list[int]() for _ in range(n_pizzas)]
    for pizza, ingredient in np.argwhere(pizzas != 0):
        pizzas_ingredients[pizza].append(ingredient)

    ingredients_customers_liked_in_pizzas = [
        [
            sorted(list(set(customer_likes) & set(pizzas_ingredients[pizza])))
            for pizza in pizzas_per_customer
        ]
        for customer_likes, pizzas_per_customer in zip(
            customers_likes, customers_pizzas
        )
    ]

    ingredients_customers_hated_in_pizzas = [
        [
            sorted(list(set(customer_hates) & set(pizzas_ingredients[pizza])))
            for pizza in pizzas_per_customer
        ]
        for customer_hates, pizzas_per_customer in zip(
            customers_hates, customers_pizzas
        )
    ]

    ingredient_names_customers_liked_in_pizzas = [
        [
            list(
                map(
                    lambda ingredient: ingredient_names[ingredient],
                    ingredients_customer_liked_in_pizza,
                )
            )
            for ingredients_customer_liked_in_pizza in ingredients_customer_liked_in_pizzas
        ]
        for ingredients_customer_liked_in_pizzas in ingredients_customers_liked_in_pizzas
    ]

    ingredient_names_customers_hated_in_pizzas = [
        [
            list(
                map(
                    lambda ingredient: ingredient_names[ingredient],
                    ingredients_customer_hated_in_pizza,
                )
            )
            for ingredients_customer_hated_in_pizza in ingredients_customer_hated_in_pizzas
        ]
        for ingredients_customer_hated_in_pizzas in ingredients_customers_hated_in_pizzas
    ]

    pizza_names_per_customers = [
        list(
            map(
                lambda pizza__n_slices_of_pizza: (
                    pizza_names[pizza__n_slices_of_pizza[0]],
                    pizza__n_slices_of_pizza[1],
                ),
                pizzas_per_customer.items(),
            )
        )
        for pizzas_per_customer in customers_pizzas
    ]

    with open(customer_slices_filename, "w+", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(
            [
                "customer_id",
                "pizza",
                "n_slices",
                "ingredients_liked",
                "ingredients_hated",
            ]
        )

        for customer, (
            pizza_names_per_customer,
            ingredients_liked_in_pizzas,
            ingredients_hated_in_pizzas,
        ) in enumerate(
            zip(
                pizza_names_per_customers,
                ingredient_names_customers_liked_in_pizzas,
                ingredient_names_customers_hated_in_pizzas,
            )
        ):
            for (pizza, n_slices), ingredients_liked, ingredients_hated in zip(
                pizza_names_per_customer,
                ingredients_liked_in_pizzas,
                ingredients_hated_in_pizzas,
            ):
                writer.writerow(
                    [
                        customer,
                        pizza,
                        n_slices,
                        ', '.join(ingredients_liked),
                        ', '.join(ingredients_hated),
                    ]
                )

    with open(pizza_order_filename, "w+", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["pizza", "n_slices"])

        for pizza, n_slices in pizza_names_with_count:
            writer.writerow([pizza, n_slices])
