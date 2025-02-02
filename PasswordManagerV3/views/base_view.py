from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

class BaseView(QWidget):
    def __init__(self, main_window, back_destination="main_menu", include_back_button=True):
        super().__init__()
        self.main_window = main_window
        self.back_destination = back_destination
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.content_layout = QVBoxLayout()
        self.layout.addLayout(self.content_layout)
        if include_back_button:
            self.add_back_button()

    def add_back_button(self):
        back_button = QPushButton("Back")
        back_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        back_button.clicked.connect(self.navigate_back)
        self.layout.addWidget(back_button)

    def navigate_back(self):
        if self.back_destination == "main_menu":
            self.main_window.restore_main_menu_size()
        self.main_window.navigate_to(self.back_destination)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
