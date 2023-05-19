#!/usr/bin/env python3
"""
App which main purpose is to evenly distribute pizza among users
"""

import csv
from typing import List, Tuple
import numpy as np


def read_pizza_file(
    filename: str,
) -> Tuple[np.ndarray, List[str], List[str], List[float]]:
    """Return a tuple of:
    - a matrix of shape (n_pizzas, n_ingredients) where each row is a pizza
        and each column is an ingredient
    - a list of pizza names
    - a list of ingredient names
    - a list of pizza prices"""

    with open(filename, "r", encoding="utf-8") as file:
        data_rows = list(csv.reader(file, delimiter=";"))[1:]

    pizzas_names: List[str] = []
    prices_list: List[float] = []

    all_ingredients_list = get_ingredients(data_rows)

    pizzas_ingredients_matrix = np.zeros(
        (len(data_rows), len(all_ingredients_list)), dtype=np.int8
    )

    for i, row in enumerate(data_rows):
        if len(row) == 4:
            _, name, ingredients, price = row
        else:
            raise ValueError("Wrongly formatted csv")

        prices_list.append(float(price))
        pizzas_names.append(name)
        for ingredient in [i.strip() for i in ingredients.split(",")]:
            j = all_ingredients_list.index(ingredient)
            pizzas_ingredients_matrix[i, j] = 1

    return pizzas_ingredients_matrix, pizzas_names, all_ingredients_list, prices_list


def get_ingredients(data_rows: List[List[str]]) -> List[str]:
    """Return sorted list of ingredients from pizza data rows."""
    all_ingredients_set = set()

    for row in data_rows:
        _, _, ingredients, _ = row
        ingredients_list = [i.strip() for i in ingredients.split(",")]
        all_ingredients_set.update(ingredients_list)

    return sorted(list(all_ingredients_set))
