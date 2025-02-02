import os
import sys
from cryptography.fernet import Fernet

def load_key(file_path="data/key.key"):
    if getattr(sys, 'frozen', False):
        app_path = sys._MEIPASS
    else:
        app_path = os.getcwd()
    full_file_path = os.path.join(app_path, file_path)
    if not os.path.exists(full_file_path):
        generate_key(full_file_path)
    with open(full_file_path, "rb") as key_file:
        return Fernet(key_file.read())

def generate_key(file_path="data/key.key"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    key = Fernet.generate_key()
    with open(file_path, "wb") as key_file:
        key_file.write(key)
