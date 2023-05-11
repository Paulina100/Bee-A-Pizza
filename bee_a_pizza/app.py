import sys
import logging
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QMainWindow,
    QLabel,
    QTextEdit,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QFileDialog,
    QLineEdit,
)

from collections import defaultdict

from import_export.import_pizzas import read_pizza_file

from components.entry import IntNumberEntry
from components.canvas import MplCanvas

from generators.order_generation import (
    generate_n_slices_per_customer,
    generate_preferences,
    get_preferences_by_slice,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.parameters = defaultdict(None)
        self.parameters = defaultdict(None)

        self.setWindowTitle("Bee a Pizza")
        self.setFixedSize(1200, 600)

        # main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # main layout
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # left layout
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        # left button 1
        left_button_1 = QPushButton("Choose pizza input .csv file")
        left_layout.addWidget(left_button_1)
        left_button_1.clicked.connect(self.open_file_dialog)
        self.parameters["input_file"] = None

        # left label 1
        self.left_label_1 = QLabel("Input file: None")
        left_layout.addWidget(self.left_label_1)

        n_customers_hbox = IntNumberEntry(
            "Number of customers",
            self.int_parameter_text_edited_action,
            default_value=15,
            min_value=1,
            max_value=1000,
            var_name="n_customers",
            params=self.parameters,
        )
        left_layout.addLayout(n_customers_hbox)

        print(self.parameters)

        min_slices_hbox = IntNumberEntry(
            "Minimum number of slices",
            self.int_parameter_text_edited_action,
            default_value=2,
            min_value=1,
            var_name="min_slices",
            params=self.parameters,
        )
        left_layout.addLayout(min_slices_hbox)

        # max_slices
        max_slices_hbox = IntNumberEntry(
            "Maximum number of slices",
            self.int_parameter_text_edited_action,
            default_value=8,
            min_value=1,
            var_name="max_slices",
            params=self.parameters,
        )
        left_layout.addLayout(max_slices_hbox)

        # avg_likes
        avg_likes_hbox = IntNumberEntry(
            "Average number of liked ingredients",
            self.int_parameter_text_edited_action,
            default_value=3,
            min_value=1,
            var_name="avg_likes",
            params=self.parameters,
        )
        left_layout.addLayout(avg_likes_hbox)

        # avg_dislikes
        avg_dislikes_hbox = IntNumberEntry(
            "Average number of disliked ingredients",
            self.int_parameter_text_edited_action,
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

        # right layout
        canvas = MplCanvas(self, width=5, height=4, dpi=100)
        canvas.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        main_layout.addWidget(canvas)

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

        self.left_label_1.setText(f"Input file: {self.fname}")

    def int_parameter_text_edited_action(
        self, text_edit, error_label, parameter_name, min_value, max_value, var_name
    ):
        parameter_text = text_edit.text()
        try:
            parameter = int(parameter_text)
        except ValueError as e:
            logging.info(e)
            error_label.setText(f"Error: {parameter_name} must be an integer")
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
        if self.parameters["input_file"] is None:
            logging.info("Error: No input file")
            self.generate_button_error_label.setText("Error: No input file")
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
        self.generate_button_error_label.setText("Successfully generated slices.")
        print("good so far")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()
