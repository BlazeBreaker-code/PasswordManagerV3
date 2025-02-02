from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel, QMainWindow, QMessageBox, QSizePolicy, QStackedWidget, QVBoxLayout,
    QPushButton, QGridLayout, QWidget, QInputDialog
)
from models.password_data import PasswordData
from controllers.password_controller import PasswordController
from views.add_service_view import AddServiceView
from views.password_view import PasswordView

class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.data_manager = PasswordData()
        self.controller = PasswordController(self.data_manager)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self._selected_folder = None
        self.delete_folder_button = None
        self.deletion_mode = False

        self.last_size = self.size()
        self.main_menu_size = None

        self.initialize_views()

    @property
    def selected_folder(self):
        return self._selected_folder

    @selected_folder.setter
    def selected_folder(self, folder_name):
        self._selected_folder = folder_name

    def resizeEvent(self, event):
        self.last_size = self.size()
        super().resizeEvent(event)

    def initialize_views(self):
        self.views = {
            "main_menu": self.create_main_menu(),
            "add_service": AddServiceView(self),
            "password_view": PasswordView(self)
        }
        for view in self.views.values():
            self.stack.addWidget(view)
        self.stack.setCurrentWidget(self.views["main_menu"])

        main_menu_layout = self.views["main_menu"].layout().itemAt(0).layout()
        self.update_folder_buttons(main_menu_layout)
        self.main_menu_size = self.size()
        self.resize(self.last_size)

    def navigate_to(self, view_name):
        if self.stack.currentWidget() == self.views["main_menu"]:
            self.main_menu_size = self.size()

        if view_name in self.views and hasattr(self.views[view_name], "refresh_view"):
            self.views[view_name].refresh_view()
        
        self.setMinimumSize(200, 200)
        self.setMaximumSize(10000, 10000)
        self.stack.setCurrentWidget(self.views[view_name])
        
        if view_name == "main_menu" and self.main_menu_size is not None:
            self.resize(self.main_menu_size)
        else:
            self.resize(self.last_size)

    def restore_main_menu_size(self):
        if self.main_menu_size is not None:
            self.resize(self.main_menu_size)

    def create_main_menu(self):
        main_menu = QWidget()
        layout = QVBoxLayout(main_menu)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        layout.addLayout(grid_layout)

        create_button = QPushButton("➕ Create New Folder")
        create_button.setStyleSheet("padding: 10px; font-size: 14px;")
        create_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        create_button.clicked.connect(self.add_new_folder)
        layout.addWidget(create_button)

        self.delete_folder_button = QPushButton("🗑️ Enable Deletion Mode")
        self.delete_folder_button.setCheckable(True)
        self.delete_folder_button.setStyleSheet("padding: 10px; font-size: 14px;")
        self.delete_folder_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.delete_folder_button.clicked.connect(self.toggle_deletion_mode)
        layout.addWidget(self.delete_folder_button)

        return main_menu

    def update_folder_buttons(self, grid_layout):
        while grid_layout.count():
            item = grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        folder_list = self.controller.get_folders()
        row, col = 0, 0

        for folder_name in folder_list:
            button = QPushButton(folder_name)
            button.setFixedSize(200, 50)
            button.clicked.connect(lambda checked, folder=folder_name: self.on_folder_button_click(folder))
            grid_layout.addWidget(button, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.views["main_menu"].layout().update()

    def toggle_deletion_mode(self):
        self.deletion_mode = not self.deletion_mode
        self.delete_folder_button.setChecked(self.deletion_mode)
        self.delete_folder_button.setText("Disable Deletion Mode" if self.deletion_mode else "🗑️ Enable Deletion Mode")

    def on_folder_button_click(self, folder_name):
        if self.deletion_mode:
            self.delete_folder(folder_name)
        else:
            self.selected_folder = folder_name
            self.navigate_to("password_view")

    def delete_folder(self, folder_name):
        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the '{folder_name}' folder? This will delete all stored services within it.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            try:
                self.controller.delete_folder(folder_name)
                QMessageBox.information(self, "Success", f"Folder '{folder_name}' deleted successfully!")

                if self.selected_folder == folder_name:
                    self.selected_folder = None

                grid_layout = self.views["main_menu"].layout().itemAt(0).layout()
                self.update_folder_buttons(grid_layout)
                self.views["main_menu"].layout().update()
                self.restore_main_menu_size()

            except ValueError as e:
                QMessageBox.warning(self, "Error", f"Could not delete folder: {e}")

    def add_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Create Folder", "Enter folder name:")
        if ok and folder_name.strip():
            try:
                self.controller.add_folder(folder_name.strip())
                grid_layout = self.views["main_menu"].layout().itemAt(0).layout()
                self.update_folder_buttons(grid_layout)
                self.views["main_menu"].layout().update()
                self.restore_main_menu_size()
            except ValueError:
                QMessageBox.warning(self, "Warning", "Folder already exists")
