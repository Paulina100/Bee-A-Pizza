"""
This module contains the main window of the application.
It is responsible for the layout of the application and
for the communication between the different components.
"""

import logging
import sys
import os
from collections import defaultdict

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QFont
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

from bee_a_pizza.app_components.canvas import MplCanvas
from bee_a_pizza.app_components.entry import NumberEntry
from bee_a_pizza.app_components.solving_thread import SolutionWorker
from bee_a_pizza.import_export.import_pizzas import read_pizza_file
from bee_a_pizza.import_export.import_preferences import read_preferences_file
from bee_a_pizza.import_export.export import export_generated_customers
from bee_a_pizza.generators.order_generation import (
    generate_n_slices_per_customer,
    generate_preferences,
    get_preferences_by_slice,
)


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super().__init__()

        self.parameters = defaultdict(lambda: None)
        self.solving_thread = None
        self.worker = None

        # main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.canvas = MplCanvas(self, width=6, height=5, dpi=100)
        # self.solve_button_error_label = QLabel("")

        self.setup_ui(main_widget)

    def setup_ui(self, main_widget):
        """Sets up the UI of the main window."""
        self.setWindowTitle("Bee a Pizza")
        self.setFixedSize(1600, 600)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # left layout
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)
        # right layout
        main_layout.addWidget(self.canvas)

        # LEFT LAYOUT
        # input pizza file
        header_label_1 = QLabel("Available pizzas")
        left_layout.addWidget(header_label_1)
        header_label_1.setFont(QFont("SansSerif", 15))

        choose_pizza_file_hbox = QHBoxLayout()
        left_layout.addLayout(choose_pizza_file_hbox)

        available_pizzas_file_label = QLabel("Input file: None")

        choose_pizza_file_button = QPushButton("Choose pizzas.csv file")
        choose_pizza_file_hbox.addWidget(choose_pizza_file_button)
        choose_pizza_file_button.clicked.connect(
            lambda: self.open_file_dialog(available_pizzas_file_label)
        )

        choose_pizza_file_hbox.addWidget(available_pizzas_file_label)

        # input preferences file
        header_label_2 = QLabel("Customer preferences")
        left_layout.addWidget(header_label_2)
        header_label_2.setFont(QFont("SansSerif", 15))

        choose_preferences_file_hbox = QHBoxLayout()
        left_layout.addLayout(choose_preferences_file_hbox)

        customer_preferences_file_label = QLabel("Input file: None")

        choose_preferences_file_button = QPushButton("Choose preferences.csv file")
        choose_preferences_file_hbox.addWidget(choose_preferences_file_button)
        choose_preferences_file_button.clicked.connect(
            lambda: self.open_preferences_file_dialog(customer_preferences_file_label)
        )

        choose_preferences_file_hbox.addWidget(customer_preferences_file_label)

        # left label 2
        generate_parameters_label = QLabel("Random customer preferences")
        left_layout.addWidget(generate_parameters_label)
        generate_parameters_label.setFont(QFont("SansSerif", 15))

        # generate slices parameters grid
        self.generate_slice_parameter_grid(left_layout)

        # slice generation button
        generate_slices_button_hbox = QHBoxLayout()
        left_layout.addLayout(generate_slices_button_hbox)

        self.generate_slices_button = QPushButton("Generate preferences")
        generate_slices_button_hbox.addWidget(self.generate_slices_button)

        generate_slices_button_error_label = QLabel("")
        generate_slices_button_hbox.addWidget(generate_slices_button_error_label)
        generate_slices_button_error_label.setStyleSheet("color: red")

        self.generate_slices_button.clicked.connect(
            lambda: self.generate_slices(generate_slices_button_error_label)
        )

        # left label 3
        solution_parameters_label = QLabel("Solution parameters")
        left_layout.addWidget(solution_parameters_label)
        solution_parameters_label.setFont(QFont("SansSerif", 15))

        # solution parameters grid
        self.generate_solve_parameter_grid(left_layout)

        solve_button_hbox = QHBoxLayout()
        left_layout.addLayout(solve_button_hbox)

        solve_button = QPushButton("Solve")
        solve_button_hbox.addWidget(solve_button)

        solve_button_error_label = QLabel("")
        solve_button_hbox.addWidget(solve_button_error_label)

        solve_button.clicked.connect(
            lambda: self.solve_threaded(solve_button, solve_button_error_label)
        )

        # save solution
        save_solution_hbox = QHBoxLayout()
        left_layout.addLayout(save_solution_hbox)

        choose_directory_to_save_solution_button = QPushButton(
            "Choose directory to save solution"
        )
        choose_directory_to_save_solution_button.clicked.connect(
            self.choose_directory_to_save_solution_to
        )
        save_solution_hbox.addWidget(choose_directory_to_save_solution_button)

        save_solution_button = QPushButton("Save")
        save_solution_button.clicked.connect(
            lambda: self.save_solution(save_solution_error_label)
        )
        save_solution_hbox.addWidget(save_solution_button)

        save_solution_error_label = QLabel("")
        save_solution_hbox.addWidget(save_solution_error_label)

    def generate_slice_parameter_grid(self, left_layout):
        """Generates the grid for the slice generation parameters."""
        generation_parameters_grid = QGridLayout()
        left_layout.addLayout(generation_parameters_grid)

        n_customers_hbox = NumberEntry(
            "Number of customers",
            default_value=15,
            min_value=1,
            max_value=1000,
            var_name="n_customers",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(n_customers_hbox, 0, 0)

        min_slices_hbox = NumberEntry(
            "Minimum number of slices",
            default_value=2,
            min_value=1,
            var_name="min_slices",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(min_slices_hbox, 1, 0)

        # max_slices
        max_slices_hbox = NumberEntry(
            "Maximum number of slices",
            default_value=8,
            min_value=1,
            var_name="max_slices",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(max_slices_hbox, 1, 1)

        # avg_likes
        avg_likes_hbox = NumberEntry(
            "Average number of liked ingredients",
            default_value=3,
            min_value=1,
            var_name="avg_likes",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(avg_likes_hbox, 2, 0)

        # avg_dislikes
        avg_dislikes_hbox = NumberEntry(
            "Average number of disliked ingredients",
            default_value=1,
            min_value=1,
            var_name="avg_dislikes",
            params=self.parameters,
        )
        generation_parameters_grid.addLayout(avg_dislikes_hbox, 2, 1)

    def generate_solve_parameter_grid(self, left_layout):
        """Generate parameters grid for solve tab"""
        solution_parameters_grid = QGridLayout()
        left_layout.addLayout(solution_parameters_grid)

        alpha_hbox = NumberEntry(
            "Alpha",
            default_value=1,
            min_value=1,
            var_name="alpha",
            params=self.parameters,
            parse_function=float,
        )
        solution_parameters_grid.addLayout(alpha_hbox, 0, 0)

        beta_hbox = NumberEntry(
            "Beta",
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
            default_value=150,
            min_value=1,
            max_value=1000,
            var_name="generations",
            params=self.parameters,
            parse_function=int,
        )
        solution_parameters_grid.addLayout(generations_number_hbox, 4, 0)

        # pizza_swap_probability
        pizza_swap_probability_hbox = NumberEntry(
            "Pizza swap probability",
            default_value=0.3,
            min_value=0,
            max_value=1,
            var_name="pizza_swap_probability",
            params=self.parameters,
            parse_function=float,
        )
        solution_parameters_grid.addLayout(pizza_swap_probability_hbox, 4, 1)


    def open_file_dialog(self, error_label):
        """Open file dialog and read pizzas from file if possible"""
        fname = QFileDialog.getOpenFileName(self, "Open file", ".", "CSV files (*.csv)")
        logging.debug(fname)
        try:
            fname = fname[0]
            (
                pizzas,
                pizza_names,
                ingredient_names,
                pizza_prices,
            ) = read_pizza_file(fname)
        except FileNotFoundError as error:
            logging.info(error)
            return
        except Exception as error:
            logging.info(error)
            error_label.setStyleSheet("color: red")
            error_label.setText("Error during reading file")
            return

        self.parameters["input_file"] = fname
        self.parameters["pizzas"] = pizzas
        self.parameters["pizza_names"] = pizza_names
        self.parameters["ingredient_names"] = ingredient_names
        self.parameters["pizza_prices"] = pizza_prices

        logging.debug("Pizzas shape: %s", str(self.parameters["pizzas"].shape))
        error_label.setStyleSheet("")
        error_label.setText(f"Input file: {fname}")

    def open_preferences_file_dialog(self, error_label):
        """Open file dialog and read preferences from file if possible"""
        if "pizzas" not in self.parameters or self.parameters["pizzas"] is None:
            error_label.setText("Error: No pizzas file read")
            error_label.setStyleSheet("color: red")
            return

        fname = QFileDialog.getOpenFileName(self, "Open file", ".", "CSV files (*.csv)")
        logging.debug(fname)
        try:
            fname = fname[0]
            n_slices, preferences = read_preferences_file(
                fname, self.parameters["ingredient_names"]
            )
        except FileNotFoundError as error:
            logging.info(error)
            return
        except Exception as error:
            logging.info(error)
            error_label.setStyleSheet("color: red")
            error_label.setText("Error during reading file")
            return

        self.parameters["n_slices"] = n_slices
        self.parameters["preferences"] = preferences
        try:
            self.parameters["slices"] = get_preferences_by_slice(preferences, n_slices)
        except Exception as error:
            logging.info(error)
            error_label.setStyleSheet("color: red")
            error_label.setText("Error during generating slices")

        logging.debug("n_slices shape: %s", str(self.parameters["n_slices"].shape))
        logging.debug(
            "preferences shape: %s", str(self.parameters["preferences"].shape)
        )
        logging.debug("slices shape: %s", str(self.parameters["slices"].shape))
        error_label.setStyleSheet("")
        error_label.setText(f"Input file: {fname}")

    def generate_slices(self, generate_slices_button_error_label):
        """Generate slices(preferences) for the given parameters"""
        if self.parameters["pizzas"] is None:
            logging.info("Error: No pizzas loaded")
            self.generate_slices_button_error_label.setText("Error: No pizzas loaded")
            return
        generate_slices_button_error_label.setText("")
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
        logging.info("Slices generated: %s", str(self.parameters["slices"].shape))
        generate_slices_button_error_label.setText("Successfully generated slices.")
        print("good so far")

    def solve_threaded(self, solve_button, solve_button_error_label):
        """Solves the problem in a separate thread given pizza, slice and solver parameters"""
        if self.parameters["slices"] is None or self.parameters["pizzas"] is None:
            solve_button_error_label.setText("Error: No slices generated")
            solve_button_error_label.setStyleSheet("color: red")
            return

        solve_button_error_label.setStyleSheet("")
        solve_button_error_label.setText("Solving...")

        self.solving_thread = QThread()
        self.worker = SolutionWorker(self.parameters)
        self.worker.moveToThread(self.solving_thread)
        self.solving_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.solving_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.solving_thread.finished.connect(self.solving_thread.deleteLater)

        self.solving_thread.start()

        solve_button_error_label.setText("Solving...")
        solve_button.setEnabled(False)
        self.solving_thread.finished.connect(
            lambda: self.finish_solve(solve_button, solve_button_error_label)
        )

    def finish_solve(self, solve_button, solve_button_error_label):
        """Called when the thread finishes, to update the GUI"""
        solve_button_error_label.setText("Solved!")
        solve_button.setEnabled(True)
        self.parameters["solution"] = self.worker.solution
        self.plot(self.worker.cost_over_time)

    def plot(self, cost_over_time):
        """Plot the cost over time"""
        self.canvas.axes.clear()
        self.canvas.axes.plot(cost_over_time)
        self.canvas.axes.set_title("Fitness over time")
        self.canvas.axes.set_xlabel('Iteration')
        self.canvas.axes.set_ylabel('Cost function')
        self.canvas.draw()

    def choose_directory_to_save_solution_to(self):
        dirname = QFileDialog.getExistingDirectory(self, "Open directory", ".")
        logging.debug(dirname)
        self.parameters["dir_solution_name"] = dirname

    def save_solution(self, error_label):
        if (
            "dir_solution_name" not in self.parameters
            or self.parameters["dir_solution_name"] is None
        ):
            error_label.setText("Choose directory first")
            error_label.setStyleSheet("color: red")
            return

        if "solution" not in self.parameters or self.parameters["solution"] is None:
            error_label.setText("Nothing to save")
            error_label.setStyleSheet("color: red")
            return

        dirname = self.parameters["dir_solution_name"]

        try:
            export_generated_customers(
                pizzas=self.parameters["pizzas"],
                n_slices_per_customers=self.parameters["n_slices"],
                preferences=self.parameters["preferences"],
                solution=self.parameters["solution"],
                pizza_names=self.parameters["pizza_names"],
                ingredient_names=self.parameters["ingredient_names"],
                customer_slices_filename=os.path.join(dirname, "customers.csv"),
                pizza_order_filename=os.path.join(dirname, "order.csv"),
            )

            error_label.setText("Saved to " + dirname)
            error_label.setStyleSheet("")

            logging.info("Exported and saved to %s", dirname)
        except Exception as e:
            error_label.setText("Error during exporting")
            error_label.setStyleSheet("color: red")
            logging.info(str(e))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
