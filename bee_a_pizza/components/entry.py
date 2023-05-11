from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


class IntNumberEntry(QHBoxLayout):
    def __init__(
        self,
        label_text: str,
        function,
        default_value: int = 0,
        min_value: int = 0,
        max_value: int = 1000,
        var_name: str = None,
        params: dict = None,
    ):
        super().__init__()

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

        var_name = var_name if var_name else label_text.lower().replace(" ", "_")
        params[var_name] = default_value

        self.text_edit.textEdited.connect(
            lambda: function(
                self.text_edit,
                self.error_label,
                label_text,
                min_value,
                max_value,
                var_name,
            )
        )
