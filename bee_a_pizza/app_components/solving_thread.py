from PyQt5.QtCore import QObject, pyqtSignal
import time
import logging
import numpy as np
from bee_a_pizza.bees_algorithm.bees import bees_algorithm
from bee_a_pizza.bees_algorithm.solution_evaluation import get_fitness


class SolutionWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, parameters):
        super().__init__()
        self.fitness_over_time = []
        self.parameters = parameters
        self.solution = None

    def run(self):
        parameters = self.parameters
        logging.info("Starting solving thread")

        coefs = np.array([parameters["alpha"], parameters["beta"]])
        result, solutions_list = bees_algorithm(
            pizzas=parameters["pizzas"],
            slices=parameters["slices"],
            max_cost=parameters["max_cost"],
            pizza_prices=parameters["pizza_prices"],
            coefs=coefs,
            scouts_n=parameters["scouts_n"],
            best_solutions_n=parameters["best_solutions_n"],
            elite_solutions_n=parameters["elite_solutions_n"],
            best_foragers_n=parameters["best_foragers_n"],
            elite_foragers_n=parameters["elite_foragers_n"],
            local_search_cycles=parameters["local_search_cycles"],
            generations=parameters["generations"],
            neighbor_swap_proba=parameters["neighbour_swap_probability"],
        )
        logging.info("Finished solving thread")

        self.solution = result

        self.fitness_over_time = [
            get_fitness(
                results=solution,
                coefs=coefs,
                pizzas_ingredients=parameters["pizzas"],
                preferences=parameters["slices"],
            )
            for solution in solutions_list
        ]
        logging.info("Finished fitness evaluation")
        self.finished.emit()
        logging.info("Finished emitting signal")
