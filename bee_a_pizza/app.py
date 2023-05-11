import sys
import typing
import matplotlib
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QTextEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QLineEdit

from import_export.import_pizzas import read_pizza_file


# matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        

        self.setWindowTitle("Bee a Pizza")
        self.setFixedSize(1000, 600)

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
        # left_button_1.setFixedWidth(400)
        left_button_1.clicked.connect(self.open_file_dialog)

        # left label 1
        self.left_label_1 = QLabel("Input file: None")
        left_layout.addWidget(self.left_label_1)

        # n_customers
        n_customers_hbox = QHBoxLayout()
        left_layout.addLayout(n_customers_hbox)
        n_customers_label = QLabel("Number of customers:")
        n_customers_hbox.addWidget(n_customers_label)
        self.n_customers_text_edit = QLineEdit()
        n_customers_hbox.addWidget(self.n_customers_text_edit)
        self.n_customers_text_edit.setFixedHeight(30)
        self.n_customers_text_edit.setText("15")
        self.n_customers_text_edit.setPlaceholderText("15")
        self.n_customers_text_edit.textEdited.connect(self.n_customers_text_edited_action)    

        # min_slices
        min_slices_hbox = QHBoxLayout()
        left_layout.addLayout(min_slices_hbox)
        min_slices_label = QLabel("Minimum number of slices:")
        min_slices_hbox.addWidget(min_slices_label)
        self.min_slices_text_edit = QLineEdit()
        min_slices_hbox.addWidget(self.min_slices_text_edit)
        self.min_slices_text_edit.setFixedHeight(30)
        self.min_slices_text_edit.setText("2")
        self.min_slices_text_edit.setPlaceholderText("2")    
        self.min_slices_text_edit.textEdited.connect(self.min_slices_text_edited_action)

        # max_slices
        max_slices_hbox = QHBoxLayout()
        left_layout.addLayout(max_slices_hbox)
        max_slices_label = QLabel("Maximum number of slices:")
        max_slices_hbox.addWidget(max_slices_label)
        self.max_slices_text_edit = QLineEdit()
        max_slices_hbox.addWidget(self.max_slices_text_edit)
        self.max_slices_text_edit.setFixedHeight(30)
        self.max_slices_text_edit.setText("8")
        self.max_slices_text_edit.setPlaceholderText("8")
        self.max_slices_text_edit.textEdited.connect(self.max_slices_text_edited_action)


        # right layout
        canvas = MplCanvas(self, width=5, height=4, dpi=100)
        canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        main_layout.addWidget(canvas)

    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.',"CSV files (*.csv)")
        self.fname = fname[0]
        self.pizzas, self.pizza_names, self.ingredient_names, self.pizza_prices = read_pizza_file(self.fname)
        self.left_label_1.setText(f"Input file: {self.fname}")
        print(self.pizza_names)

    def n_customers_text_edited_action(self):
        print(self.n_customers_text_edit.text())

    def min_slices_text_edited_action(self):
        print(self.min_slices_text_edit.text())

    def max_slices_text_edited_action(self):
        print(self.max_slices_text_edit.text())



app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()








