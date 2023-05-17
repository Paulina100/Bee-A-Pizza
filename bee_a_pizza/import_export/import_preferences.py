"""Imports customer preferences"""

import csv
import numpy as np


def read_preferences_file(
    filename: str,
    all_ingredients_list: list[str],
) -> tuple[np.ndarray, np.ndarray]:
    with open(filename, "r", encoding="utf-8") as file:
        data_rows = list(csv.reader(file, delimiter=";"))[1:]

    n_customers = len(data_rows)

    customers_preferences_matrix = np.zeros(
        (n_customers, len(all_ingredients_list)), dtype=np.int8
    )

    n_slices = np.zeros(n_customers, dtype=np.int8)

    for i, row in enumerate(data_rows):
        _, n_slices_per_customer, ingredients_liked, ingredients_hated = row
        n_slices[i] = int(n_slices_per_customer)

        for ingredient in [i.strip() for i in ingredients_liked.split(",")]:
            try:
                j = all_ingredients_list.index(ingredient)
                customers_preferences_matrix[i, j] = 1
            except ValueError:
                print(f"Ingredient {ingredient} not recognized")

        for ingredient in [i.strip() for i in ingredients_hated.split(",")]:
            try:
                j = all_ingredients_list.index(ingredient)
                customers_preferences_matrix[i, j] = -1
            except ValueError:
                print(f"Ingredient {ingredient} not recognized")

    return n_slices, customers_preferences_matrix
