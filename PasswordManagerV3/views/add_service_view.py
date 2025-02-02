from views.base_view import BaseView
from PyQt6.QtWidgets import QLabel, QLineEdit, QMessageBox, QPushButton, QSizePolicy, QSpacerItem

class AddServiceView(BaseView):
    def __init__(self, main_window):
        super().__init__(main_window, back_destination="password_view")
        self.folder_label = QLabel("")
        
        self.service_name_input = QLineEdit()
        self.service_name_input.setPlaceholderText("Service Name")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.save_button = QPushButton("Save Entry")
        
        self.save_button.clicked.connect(self.save_entry)
        self.content_layout.addWidget(self.folder_label)
        self.content_layout.addWidget(self.service_name_input)
        self.content_layout.addWidget(self.username_input)
        self.content_layout.addWidget(self.password_input)
        
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.content_layout.addItem(spacer)
        self.content_layout.addWidget(self.save_button)

    def showEvent(self, event):
        super().showEvent(event)
        self.main_window.resize(500, 300)

    def refresh_view(self):
        folder_name = self.main_window.selected_folder
        self.folder_label.setText(f"Adding to Folder: {folder_name}" if folder_name else "No folder selected!")

    def save_entry(self):
        selected_folder = self.main_window.selected_folder
        if not selected_folder:
            QMessageBox.warning(self, "Warning", "No folder selected!")
            return

        service_name = self.service_name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not service_name or not username or not password:
            QMessageBox.warning(self, "Warning", "All fields are required!")
            return

        try:
            self.main_window.controller.add_service(
                selected_folder, service_name, username, password
            )
            self.service_name_input.clear()
            self.username_input.clear()
            self.password_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save entry: {e}")
