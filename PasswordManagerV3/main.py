import os
import sys
from PyQt6.QtWidgets import QApplication
from password_manager import PasswordManager

def get_stylesheet_path():
    if getattr(sys, 'frozen', False):
        app_path = sys._MEIPASS
    else:
        app_path = os.getcwd()
    return os.path.join(app_path, 'resources', 'styles.qss')

def load_stylesheet(app):
    stylesheet_path = get_stylesheet_path()
    try:
        with open(stylesheet_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    main_window = PasswordManager()
    main_window.show()
    sys.exit(app.exec())
