import atexit
import os
import requests
import sys
import time
from urllib import response
from datetime import datetime
from cryptography.fernet import Fernet
import json

if getattr(sys, 'frozen', False):
    app_path = sys._MEIPASS
    persistent_path = os.path.dirname(sys.executable)
else:
    app_path = os.getcwd()
    persistent_path = app_path

key_path = os.path.join(app_path, 'data', 'Key.key')
if not os.path.exists(key_path):
    sys.exit(1)

try:
    with open(key_path, "rb") as key_file:
        key = key_file.read()
except Exception as e:
    sys.exit(1)

cipher = Fernet(key)

json_path = os.path.join(app_path, 'data', 'passwords.json')
if not os.path.exists(json_path):
    sys.exit(1)

class PasswordData:
    def __init__(self, file_path=None):
        self.file_path = os.path.join(persistent_path, 'data', 'passwords.json') if file_path is None else file_path
        self.data = self.load_data()
        # Backup the passwords and then clean up the backups (this is a stacked operation).
        atexit.register(self.cleanup_backups_in_firebase)
        atexit.register(self.backup_password_to_firebase)

    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            raise ValueError("Password file is corrupted.")

    def save_data(self):
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.data, file, indent=4)
        except Exception as e:
            sys.exit(1)

    def get_folders(self):
        return list(self.data.keys())

    def get_folder_data(self, folder_name):
        return self.data.get(folder_name, {})

    def add_folder(self, folder_name):
        if folder_name in self.data:
            raise ValueError(f"Folder '{folder_name}' already exists.")
        self.data[folder_name] = {}
        self.save_data()

    def delete_folder(self, folder_name):
        if folder_name not in self.data:
            raise ValueError(f"Folder '{folder_name}' does not exist.")
        del self.data[folder_name]
        self.save_data()

    def delete_service(self, folder_name, service_name):
        if folder_name not in self.data or service_name not in self.data[folder_name]:
            raise ValueError(f"Service '{service_name}' does not exist in folder '{folder_name}'.")
        del self.data[folder_name][service_name]
        self.save_data()

    def add_service(self, folder_name, service_name, username, password):
        if folder_name not in self.data:
            raise ValueError(f"Folder '{folder_name}' does not exist.")
        if service_name in self.data[folder_name]:
            raise ValueError(f"Service '{service_name}' already exists in folder '{folder_name}'.")
        encrypted_password = self.encrypt_password(password)
        self.data[folder_name][service_name] = {
            "username": username,
            "password": encrypted_password
        }
        self.save_data()

    def encrypt_password(self, plain_text_password):
        return cipher.encrypt(plain_text_password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        try:
            return cipher.decrypt(encrypted_password.encode()).decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt the password: {e}")

    @staticmethod
    def generate_timestamp_filename():
        """Generate a timestamp-based filename."""
        timestamp = int(time.time())
        # Formatted so it is readable.
        readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
        return readable_time

    def backup_password_to_firebase(self):
        try:
            filename = self.generate_timestamp_filename() + "_passwords"

            password_data = self.data
            url = f"https://passwordmanager-surajm99-default-rtdb.firebaseio.com/{filename}.json"
            response = requests.put(url, data=json.dumps(password_data))

            if response.status_code == 200:
                print("Password data successfully uploaded to Firebase!")
            else:
                print(f"Failed to upload data. Status Code: {response.status_code}, Error: {response.text}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def cleanup_backups_in_firebase(self):
        try:
            url = "https://passwordmanager-surajm99-default-rtdb.firebaseio.com/.json"
            response = requests.get(url)

            data = response.json()
            filenames = list(data.keys())
            
            if len(filenames) > 5:
                filenames.sort()
                for filename in filenames[:-5]:
                    delete_url = f"https://passwordmanager-surajm99-default-rtdb.firebaseio.com/{filename}.json"
                    try:
                        delete_response = requests.delete(delete_url)
                        if delete_response.status_code == 200:
                            print(f"Successfully deleted old backup: {filename}")
                        else:
                            print(f"Failed to delete {filename}. Status Code: {delete_response.status_code}, Error: {delete_response.text}")
                    except Exception as e:
                        print(f"An error occurred: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")