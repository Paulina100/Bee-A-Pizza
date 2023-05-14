import logging
import sys
from collections import defaultdict

from PyQt5.QtCore import QThread
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
    QGridLayout,
)


from bee_a_pizza.bees_algorithm.bees import bees_algorithm
from bee_a_pizza.app_components.canvas import MplCanvas
from bee_a_pizza.app_components.entry import NumberEntry
from bee_a_pizza.app_components.solving_thread import SolutionWorker
from bee_a_pizza.generators.order_generation import (
    generate_n_slices_per_customer,
    generate_preferences,
    get_preferences_by_slice,
)
from bee_a_pizza.import_export.import_pizzas import read_pizza_file
from bee_a_pizza.bees_algorithm.solution_evaluation import get_fitness


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

        # generation_parameters grid
        generation_parameters_grid = QGridLayout()
        left_layout.addLayout(generation_parameters_grid)

        n_customers_hbox = NumberEntry(
            "Number of customers",
            self.parameter_text_edited_action,
            default_value=15,
            min_value=1,
            max_value=1000,
            var_name="n_customers",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(n_customers_hbox, 0, 0)

        min_slices_hbox = NumberEntry(
            "Minimum number of slices",
            self.parameter_text_edited_action,
            default_value=2,
            min_value=1,
            var_name="min_slices",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(min_slices_hbox, 1, 0)

        # max_slices
        max_slices_hbox = NumberEntry(
            "Maximum number of slices",
            self.parameter_text_edited_action,
            default_value=8,
            min_value=1,
            var_name="max_slices",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(max_slices_hbox, 1, 1)

        # avg_likes
        avg_likes_hbox = NumberEntry(
            "Average number of liked ingredients",
            self.parameter_text_edited_action,
            default_value=3,
            min_value=1,
            var_name="avg_likes",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(avg_likes_hbox, 2, 0)

        # avg_dislikes
        avg_dislikes_hbox = NumberEntry(
            "Average number of disliked ingredients",
            self.parameter_text_edited_action,
            default_value=1,
            min_value=1,
            var_name="avg_dislikes",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(avg_dislikes_hbox, 2, 1)

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

        # solution_parameters grid
        solution_parameters_grid = QGridLayout()
        left_layout.addLayout(solution_parameters_grid)

        alpha_hbox = NumberEntry(
            "Alpha",
            self.parameter_text_edited_action,
            default_value=1,
            min_value=1,
            var_name="alpha",
            params=self.parameters,
            parse_function=float,
        )
        solution_parameters_grid.addLayout(alpha_hbox, 0, 0)

        beta_hbox = NumberEntry(
            "Beta",
            self.parameter_text_edited_action,
            default_value=1,
            min_value=1,
            var_name="beta",
            params=self.parameters,
            parse_function=float,
        )
        solution_parameters_grid.addLayout(beta_hbox, 0, 1)

        # scouts_number
        scouts_number_hbox = NumberEntry(
            "Number of scouts",
            self.parameter_text_edited_action,
            default_value=80,
            min_value=10,
            max_value=1000,
            var_name="scouts_n",
            params=self.parameters,
            parse_function=int,
        )
        solution_parameters_grid.addLayout(scouts_number_hbox, 1, 0)

        # best_solutions_number
        best_solutions_number_hbox = NumberEntry(
            "Number of best solutions",
            self.parameter_text_edited_action,
            default_value=50,
            min_value=1,
            max_value=1000,
            var_name="best_solutions_n",
            params=self.parameters,
            parse_function=int,
        )
        solution_parameters_grid.addLayout(best_solutions_number_hbox, 1, 1)

        # elite_solutions_number
        elite_solutions_number_hbox = NumberEntry(
            "Number of elite solutions",
            self.parameter_text_edited_action,
            default_value=10,
            min_value=5,
            max_value=1000,
            var_name="elite_solutions_n",
            params=self.parameters,
            parse_function=int,
        )
        solution_parameters_grid.addLayout(elite_solutions_number_hbox, 2, 0)

        # best_foragers_number
        best_foragers_number_hbox = NumberEntry(
            "Number of best foragers",
            self.parameter_text_edited_action,
            default_value=10,
            min_value=5,
            max_value=1000,
            var_name="best_foragers_n",
            params=self.parameters,
            parse_function=int,
        )
        solution_parameters_grid.addLayout(best_foragers_number_hbox, 2, 1)

        # elite_foragers_number
        elite_foragers_number_hbox = NumberEntry(
            "Number of elite foragers",
            self.parameter_text_edited_action,
            default_value=10,
            min_value=5,
            max_value=1000,
            var_name="elite_foragers_n",
            params=self.parameters,
            parse_function=int,
        )
        solution_parameters_grid.addLayout(elite_foragers_number_hbox, 3, 0)

        # local_search_cycles
        local_search_cycles_hbox = NumberEntry(
            "Number of local search cycles",
            self.parameter_text_edited_action,
            default_value=8,
            min_value=1,
            max_value=1000,
            var_name="local_search_cycles",
            params=self.parameters,
            parse_function=int,
        )
        solution_parameters_grid.addLayout(local_search_cycles_hbox, 3, 1)

        # generations_number
        generations_number_hbox = NumberEntry(
            "Number of generations",
            self.parameter_text_edited_action,
            default_value=150,
            min_value=1,
            max_value=1000,
            var_name="generations",
            params=self.parameters,
            parse_function=int,
        )
        solution_parameters_grid.addLayout(generations_number_hbox, 4, 0)

        # neighbour_swap_probability
        neighbour_swap_probability_hbox = NumberEntry(
            "Neighbour swap probability",
            self.parameter_text_edited_action,
            default_value=0.3,
            min_value=0,
            max_value=1,
            var_name="neighbour_swap_probability",
            params=self.parameters,
            parse_function=float,
        )
        solution_parameters_grid.addLayout(neighbour_swap_probability_hbox, 4, 1)

        # max cost
        max_cost_hbox = NumberEntry(
            "Max cost",
            self.parameter_text_edited_action,
            default_value=100,
            min_value=1,
            max_value=100000,
            var_name="max_cost",
            params=self.parameters,
            parse_function=float,
        )
        solution_parameters_grid.addLayout(max_cost_hbox, 5, 0)

        solve_button_hbox = QHBoxLayout()
        left_layout.addLayout(solve_button_hbox)

        self.solve_button = QPushButton("Solve")
        solve_button_hbox.addWidget(self.solve_button)
        # self.solve_button.clicked.connect(self.solve)
        self.solve_button.clicked.connect(self.solve_threaded)

        self.solve_button_error_label = QLabel("")
        solve_button_hbox.addWidget(self.solve_button_error_label)
        self.solve_button_error_label.setStyleSheet("color: red")

        # right layout
        self.canvas = MplCanvas(self, width=6, height=5, dpi=100)
        # self.canvas.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        main_layout.addWidget(self.canvas)

    def setup_ui(self):
        pass

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

    def solve_threaded(self):
        if self.parameters["slices"] is None or self.parameters["pizzas"] is None:
            self.solve_button_error_label.setText("Error: No slices generated")
            return

        self.solve_button_error_label.setText("Solving...")
        cost_function_coefficients = np.array(
            [self.parameters["alpha"], self.parameters["beta"]]
        )

        self.thread = QThread()
        self.worker = SolutionWorker(self.parameters)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        self.solve_button_error_label.setText("Solving...")
        self.solve_button.setEnabled(False)
        self.thread.finished.connect(lambda: self.finish_solve())

    def finish_solve(self):
        self.solve_button_error_label.setText("Solved!")
        self.solve_button.setEnabled(True)
        self.plot(self.worker.fitness_over_time)

    def plot(self, fitness_over_time):
        self.canvas.axes.clear()
        self.canvas.axes.plot(fitness_over_time)
        self.canvas.draw()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
