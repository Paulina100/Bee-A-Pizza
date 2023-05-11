import logging
import sys
from collections import defaultdict

import PyQt5.QtGui as QtGui
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMainWindow,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
)

from bees_algorithm.bees import bees_algorithm
from components.canvas import MplCanvas
from components.entry import NumberEntry
from generators.order_generation import (
    generate_n_slices_per_customer,
    generate_preferences,
    get_preferences_by_slice,
)
from import_export.import_pizzas import read_pizza_file
from bees_algorithm.solution_evaluation import get_fitness


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.parameters = defaultdict(lambda: None)

        self.setWindowTitle("Bee a Pizza")
        self.setFixedSize(1600, 600)

        # main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # main layout
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # left layout
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        # left label 0
        left_label_0 = QLabel("Available pizzas")
        left_layout.addWidget(left_label_0)
        left_label_0.setFont(QtGui.QFont("SansSerif", 15))

        choose_pizza_hbox = QHBoxLayout()
        left_layout.addLayout(choose_pizza_hbox)
        # left button 1
        left_button_1 = QPushButton("Choose pizza input .csv file")
        choose_pizza_hbox.addWidget(left_button_1)
        left_button_1.clicked.connect(self.open_file_dialog)
        self.parameters["input_file"] = None

        # left label 1
        self.left_label_1 = QLabel("Input file: None")
        choose_pizza_hbox.addWidget(self.left_label_1)

        # left label 2
        left_label_2 = QLabel("Slice needs")
        left_layout.addWidget(left_label_2)
        left_label_2.setFont(QtGui.QFont("SansSerif", 15))

        # left label 3
        self.left_label_3 = QLabel("Load slice needs")
        left_layout.addWidget(self.left_label_3)
        self.left_label_3.setFont(QtGui.QFont("SansSerif", 15))

        # left label 4
        self.left_label_4 = QLabel("Generation parameters")
        left_layout.addWidget(self.left_label_4)
        self.left_label_4.setFont(QtGui.QFont("SansSerif", 15))

        n_customers_hbox = NumberEntry(
            "Number of customers",
            self.parameter_text_edited_action,
            default_value=15,
            min_value=1,
            max_value=1000,
            var_name="n_customers",
            params=self.parameters,
        )
        left_layout.addLayout(n_customers_hbox)

        print(self.parameters)

        min_slices_hbox = NumberEntry(
            "Minimum number of slices",
            self.parameter_text_edited_action,
            default_value=2,
            min_value=1,
            var_name="min_slices",
            params=self.parameters,
        )
        left_layout.addLayout(min_slices_hbox)

        # max_slices
        max_slices_hbox = NumberEntry(
            "Maximum number of slices",
            self.parameter_text_edited_action,
            default_value=8,
            min_value=1,
            var_name="max_slices",
            params=self.parameters,
        )
        left_layout.addLayout(max_slices_hbox)

        # avg_likes
        avg_likes_hbox = NumberEntry(
            "Average number of liked ingredients",
            self.parameter_text_edited_action,
            default_value=3,
            min_value=1,
            var_name="avg_likes",
            params=self.parameters,
        )
        left_layout.addLayout(avg_likes_hbox)

        # avg_dislikes
        avg_dislikes_hbox = NumberEntry(
            "Average number of disliked ingredients",
            self.parameter_text_edited_action,
            default_value=1,
            min_value=1,
            var_name="avg_dislikes",
            params=self.parameters,
        )
        left_layout.addLayout(avg_dislikes_hbox)

        # slice generator button
        generator_button_hbox = QHBoxLayout()
        left_layout.addLayout(generator_button_hbox)

        generate_slices_button = QPushButton("Generate slices")
        generator_button_hbox.addWidget(generate_slices_button)
        generate_slices_button.clicked.connect(self.generate_slices)

        self.generate_button_error_label = QLabel("")
        generator_button_hbox.addWidget(self.generate_button_error_label)
        self.generate_button_error_label.setStyleSheet("color: red")

        # left label 5
        left_label_5 = QLabel("Solution parameters: -likes*alpha + dislikes*beta")
        left_layout.addWidget(left_label_5)
        left_label_5.setFont(QtGui.QFont("SansSerif", 15))

        alpha_hbox = NumberEntry(
            "Alpha",
            self.parameter_text_edited_action,
            default_value=1,
            min_value=1,
            var_name="alpha",
            params=self.parameters,
            parse_function=float,
        )
        left_layout.addLayout(alpha_hbox)

        beta_hbox = NumberEntry(
            "Beta",
            self.parameter_text_edited_action,
            default_value=1,
            min_value=1,
            var_name="beta",
            params=self.parameters,
            parse_function=float,
        )
        left_layout.addLayout(beta_hbox)

        solve_button_hbox = QHBoxLayout()
        left_layout.addLayout(solve_button_hbox)

        solve_button = QPushButton("Solve")
        solve_button_hbox.addWidget(solve_button)
        solve_button.clicked.connect(self.solve)

        self.solve_button_error_label = QLabel("")
        solve_button_hbox.addWidget(self.solve_button_error_label)
        self.solve_button_error_label.setStyleSheet("color: red")

        # right layout
        self.canvas = MplCanvas(self, width=6, height=5, dpi=100)
        self.canvas.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        main_layout.addWidget(self.canvas)

    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", ".", "CSV files (*.csv)")
        logging.debug(fname)
        try:
            self.fname = fname[0]
            (
                pizzas,
                pizza_names,
                ingredient_names,
                pizza_prices,
            ) = read_pizza_file(self.fname)
        except FileNotFoundError as e:
            logging.info(e)
            return

        self.parameters["input_file"] = self.fname
        self.parameters["pizzas"] = pizzas
        self.parameters["pizza_names"] = pizza_names
        self.parameters["ingredient_names"] = ingredient_names
        self.parameters["pizza_prices"] = pizza_prices

        logging.debug("Pizzas shape: " + str(self.parameters["pizzas"].shape))

        self.left_label_1.setText(f"Input file: {self.fname}")

    def parameter_text_edited_action(
        self,
        text_edit,
        error_label,
        parameter_name,
        min_value,
        max_value,
        var_name,
        parse_func=int,
    ):
        parameter_text = text_edit.text()
        try:
            parameter = parse_func(parameter_text)
        except ValueError as e:
            logging.info(e)
            error_label.setText(
                f"Error: {parameter_name} must be "
                + ("an integer" if parse_func == int else "a float")
            )
            return

        # Checking constraints
        if parameter < 0:
            error_label.setText(f"Error: {parameter_name} must be positive")
            logging.info(f"Error: {parameter_name} must be positive")
            self.parameters[parameter_name] = None
            return
        if parameter < min_value:
            error_label.setText(f"Error: {parameter_name} must be at least {min_value}")
            logging.info(f"Error: {parameter_name} must be at least {min_value}")
            self.parameters[parameter_name] = None
            return
        if parameter > max_value:
            error_label.setText(f"Error: {parameter_name} must be at most {max_value}")
            logging.info(f"Error: {parameter_name} must be at most {max_value}")
            self.parameters[parameter_name] = None
            return

        self.parameters[var_name] = parameter
        error_label.setText("")

    def generate_slices(self):
        if self.parameters["pizzas"] is None:
            logging.info("Error: No pizzas loaded")
            self.generate_button_error_label.setText("Error: No pizzas loaded")
            return
        self.generate_button_error_label.setText("")
        print(self.parameters)
        self.parameters["n_slices"] = generate_n_slices_per_customer(
            min_slices=self.parameters["min_slices"],
            max_slices=self.parameters["max_slices"],
            n_customers=self.parameters["n_customers"],
        )
        self.parameters["preferences"] = generate_preferences(
            n_customers=self.parameters["n_customers"],
            n_ingredients=len(self.parameters["ingredient_names"]),
            avg_likes=self.parameters["avg_likes"],
            avg_dislikes=self.parameters["avg_dislikes"],
        )
        self.parameters["slices"] = get_preferences_by_slice(
            self.parameters["preferences"], self.parameters["n_slices"]
        )
        logging.info("Slices generated: " + str(self.parameters["slices"].shape))
        self.generate_button_error_label.setText("Successfully generated slices.")
        print("good so far")

    def solve(self):
        logging.info("Solving...")
        if self.parameters["slices"] is None:
            logging.info("Error: No slices generated")
            self.solve_button_error_label.setText("Error: No slices generated")
            return
        self.solve_button_error_label.setText("Solving...")
        coefs = np.array([self.parameters["alpha"], self.parameters["beta"]])
        result, solutions_list = bees_algorithm(
            pizzas=self.parameters["pizzas"],
            slices=self.parameters["slices"],
            pizza_prices=np.array(self.parameters["pizza_prices"]),
            coefs=coefs,
            max_cost=1000,
            # scouts_n=self.parameters["scouts_n"],
            # best_solutions_n=self.parameters["best_solutions_n"],
            # elite_solutions_n=self.parameters["elite_solutions_n"],
            # best_foragers_n=self.parameters["best_foragers_n"],
            # elite_foragers_n=self.parameters["elite_foragers_n"],
            # local_search_cycles=self.parameters["local_search_cycles"],
            # generations=self.parameters["generations"],
            # neighbor_swap_proba=self.parameters["neighbor_swap_proba"],
        )
        self.solve_button_error_label.setText("Solved!")
        logging.info("Solved!")

        # TODO fix error - bad shape
        # fitness_over_time = [
        #     get_fitness(
        #         results=sol,
        #         coefs=coefs,
        #         pizzas_ingredients=self.parameters["pizzas"],
        #         preferences=self.parameters["preferences"],
        #     )
        #     for sol in solutions_list
        # ]
        # self.canvas.axes.clear()
        # self.canvas.axes.plot(fitness_over_time)
        # self.canvas.draw()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
