from PyQt5.QtCore import QObject, pyqtSignal
import time
import logging
import numpy as np
from bee_a_pizza.bees_algorithm.bees import bees_algorithm
from bee_a_pizza.bees_algorithm.solution_evaluation import get_cost


class SolutionWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, parameters):
        super().__init__()
        self.cost_over_time = []
        self.parameters = parameters
        self.solution = None

    def run(self):
        parameters = self.parameters
        logging.info("Starting solving thread")

        coefs = np.array([parameters["alpha"], parameters["beta"]])
        result, solutions_list = bees_algorithm(
            pizzas=parameters["pizzas"],
            slices=parameters["slices"],
            coefs=coefs,
            scouts_n=parameters["scouts_n"],
            best_solutions_n=parameters["best_solutions_n"],
            elite_solutions_n=parameters["elite_solutions_n"],
            best_foragers_n=parameters["best_foragers_n"],
            elite_foragers_n=parameters["elite_foragers_n"],
            local_search_cycles=parameters["local_search_cycles"],
            generations=parameters["generations"],
            pizza_swap_proba=parameters["pizza_swap_probability"],
        )
        logging.info("Finished solving thread")

        self.solution = result

        self.cost_over_time = [
            get_cost(
                results=solution,
                coefs=coefs,
                pizzas_ingredients=parameters["pizzas"],
                preferences=parameters["slices"],
            )
            for solution in solutions_list
        ]
        logging.info("Finished cost evaluation")
        self.finished.emit()
        logging.info("Finished emitting signal")
