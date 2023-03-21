#!/usr/bin/env python3

import numpy as np
from typing import Tuple
import csv


def read_pizza_file(filename: str) -> Tuple[np.ndarray, list, list, list]:
    """Return a tuple of:
    - a matrix of shape (n_pizzas, n_ingredients) where each row is a pizza and each column is an ingredient
    - a list of pizza names
    - a list of ingredient names
    - a list of pizza prices"""

    with open(filename, 'r') as f:
        r = csv.reader(f, delimiter=';')
        rows = list(r)[1:]

    pizzas_names = []
    prices_list = []
    all_ingredients_list = set()

    for row in rows:
        _, name, ingredients, price = row
        ingredients = [i.strip() for i in ingredients.split(',')]
        prices_list.append(float(price))
        pizzas_names.append(name)
        all_ingredients_list.update(ingredients)

    all_ingredients_list = list(all_ingredients_list)

    pizzas_ingredients_matrix = np.zeros((len(rows), len(all_ingredients_list)), dtype=np.int8)
    
    for i, row in enumerate(rows):
        _, name, ingredients, price = row
        ingredients = [i.strip()for i in ingredients.split(',')]
        for ingredient in ingredients:
            j = all_ingredients_list.index(ingredient)
            pizzas_ingredients_matrix[i, j] = 1

    return pizzas_ingredients_matrix, pizzas_names, all_ingredients_list, prices_list