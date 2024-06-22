from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt

class LabelEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.class_label = QLabel("Class:", self)
        self.class_edit = QLineEdit(self)

        self.save_button = QPushButton("Save Label", self)
        self.save_button.clicked.connect(self.save_label)

        self.clear_button = QPushButton("Clear Label", self)
        self.clear_button.clicked.connect(self.clear_label)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.class_label)
        self.layout.addWidget(self.class_edit)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.clear_button)

        self.setLayout(self.layout)

    def save_label(self):
        class_name = self.class_edit.text()
        if class_name:
            QMessageBox.information(self, "Info", f"Saved label: {class_name}")
        else:
            QMessageBox.warning(self, "Warning", "Class name cannot be empty.")

    def clear_label(self):
        self.class_edit.clear()
