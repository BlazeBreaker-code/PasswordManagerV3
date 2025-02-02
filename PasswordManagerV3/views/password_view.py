from PyQt6.QtWidgets import (
    QApplication, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from views.base_view import BaseView


class PasswordView(BaseView):
    def __init__(self, main_window):
        super().__init__(main_window, back_destination="main_menu")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.content_layout.addWidget(self.scroll_area)

        self.add_service_button = QPushButton("Add Service")
        self.add_service_button.clicked.connect(lambda: self.main_window.navigate_to("add_service"))
        self.content_layout.addWidget(self.add_service_button, 0, alignment=Qt.AlignmentFlag.AlignBottom)

    def showEvent(self, event):
        """Ensure the view updates and resizes when it first appears."""
        super().showEvent(event)
        self.refresh_view()

    def refresh_view(self):
        """Refresh the view whenever it's navigated to and resize accordingly."""
        folder_name = self.main_window.selected_folder
        if folder_name:
            folder_data = self.main_window.controller.get_folder_data(folder_name)
            self.populate_passwords(folder_data)
            self.resize_window(len(folder_data))
        else:
            self.clear_layout(self.scroll_layout)

    def populate_passwords(self, folder_data):
        """Populate the view with passwords for the selected folder."""
        self.clear_layout(self.scroll_layout)

        for service, credentials in folder_data.items():
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(10, 10, 10, 10)
            row_layout.setSpacing(15)

            service_label = QLabel(f"🔑 {service}")
            service_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            service_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            username_button = QPushButton(f"👤 {credentials.get('username', 'No Username')}")
            username_button.setStyleSheet("text-align: left; padding-left: 10px;")
            username_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            username_button.clicked.connect(
                lambda _, username=credentials.get("username", ""): self.copy_to_clipboard(username)
            )

            password_button = QPushButton("🔒 Copy Password")
            password_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            password_button.clicked.connect(
                lambda _, password=credentials.get("password", ""): self.copy_to_clipboard(
                    self.main_window.data_manager.decrypt_password(password)
                )
            )

            delete_button = QPushButton("❌")
            delete_button.setFixedWidth(50)
            delete_button.clicked.connect(lambda _, service=service: self.delete_service(service))

            row_layout.addWidget(service_label, 3)
            row_layout.addWidget(username_button, 2)
            row_layout.addWidget(password_button, 1)
            row_layout.addWidget(delete_button, 1)

            self.scroll_layout.addLayout(row_layout)

    def resize_window(self, row_count):
        """Dynamically adjust the window size based on the number of password entries."""
        min_height = 250
        max_height = 600
        row_height = 60 
        button_height = 100
        padding = 40

        calculated_height = (row_count * row_height) + button_height + padding
        new_height = max(min_height, min(calculated_height, max_height))

        min_width = 500
        max_width = 1000
        base_width = 300
        button_width = 180 * 2
        label_width = max(
            self.scroll_layout.itemAt(i).itemAt(0).widget().sizeHint().width()
            for i in range(row_count)
        ) if row_count > 0 else 0

        calculated_width = base_width + label_width + button_width
        new_width = max(min_width, min(calculated_width, max_width))

        self.main_window.resize(new_width, new_height)

    def delete_service(self, service_name):
        """Delete a service from the selected folder."""
        folder_name = self.main_window.selected_folder
        if not folder_name:
            QMessageBox.warning(self, "Error", "No folder selected!")
            return

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the service '{service_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            self.main_window.controller.delete_service(folder_name, service_name)
            QMessageBox.information(self, "Success", f"Service '{service_name}' deleted.")

            folder_data = self.main_window.controller.get_folder_data(folder_name)
            self.populate_passwords(folder_data)
            self.resize_window(len(folder_data))

    def copy_to_clipboard(self, text):
        """Copy text to the clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
