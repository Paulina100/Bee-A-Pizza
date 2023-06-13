from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit
import logging


class NumberEntry(QHBoxLayout):
    def __init__(
        self,
        label_text: str,
        var_name: str,
        params: dict,
        default_value: int | float = 1,
        min_value: int = 0,
        max_value: int = 1000,
        parse_function=int,
    ):
        super().__init__()

        self.parameter_name = label_text
        self.min_value = min_value
        self.max_value = max_value
        self.parse_function = parse_function
        self.var_name = var_name if var_name else label_text.lower().replace(" ", "_")
        params[var_name] = default_value

        self.label = QLabel(label_text + ": ")
        self.addWidget(self.label)

        self.text_edit = QLineEdit()
        self.addWidget(self.text_edit)
        self.text_edit.setFixedHeight(30)
        self.text_edit.setText(str(default_value))
        self.text_edit.setPlaceholderText(str(default_value))

        self.error_label = QLabel("")
        self.addWidget(self.error_label)
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("color: red")

        self.text_edit.textEdited.connect(
            lambda: self.parameter_text_edited_action(params)
        )

    def parameter_text_edited_action(
        self,
        parameters: dict,
    ):
        """Validate parameter text edit and update parameters dict"""
        parameter_text = self.text_edit.text()
        try:
            parameter = self.parse_function(parameter_text)
        except ValueError as error:
            logging.info(error)
            self.error_label.setText(
                f"Error: {self.parameter_name} must be "
                + ("an integer" if self.parse_function == int else "a float")
            )
            return

        # Checking constraints
        if parameter < 0:
            self.error_label.setText(f"Error: {self.parameter_name} must be positive")
            logging.info("Error: %s must be positive", self.parameter_name)
            parameters[self.parameter_name] = None
            return
        if parameter < self.min_value:
            self.error_label.setText(
                f"Error: {self.parameter_name} must be at least {self.min_value}"
            )
            logging.info(
                "Error: %s must be at least %f", self.parameter_name, self.min_value
            )
            parameters[self.parameter_name] = None
            return
        if parameter > self.max_value:
            self.error_label.setText(
                f"Error: {self.parameter_name} must be at most {self.max_value}"
            )
            logging.info(
                "Error: %s must be at most %f", self.parameter_name, self.max_value
            )
            parameters[self.parameter_name] = None
            return

        parameters[self.var_name] = parameter
        self.error_label.setText("")
