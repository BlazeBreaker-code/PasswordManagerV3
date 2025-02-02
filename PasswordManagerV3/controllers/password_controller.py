import json

class PasswordController:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_folders(self):
        """Get a list of all folders."""
        return self.data_manager.get_folders()

    def get_folder_data(self, folder_name):
        """Get the services in a specific folder."""
        return self.data_manager.get_folder_data(folder_name)

    def add_folder(self, folder_name):
        """Add a new folder."""
        if not folder_name.strip():
            raise ValueError("Folder name cannot be empty.")
        self.data_manager.add_folder(folder_name)

    def delete_folder(self, folder_name):
        """Delete a folder through the data manager."""
        try:
            self.data_manager.delete_folder(folder_name)
            return True
        except ValueError as e:
            print(f"Debug: {e}")
            raise ValueError(str(e))
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise RuntimeError(f"Failed to delete folder: {e}")

    def delete_service(self, folder_name, service_name):
        """Delete a service from a folder."""
        self.data_manager.delete_service(folder_name, service_name)

    def add_service(self, folder_name, service_name, username, password):
        """Add a service to a folder."""
        if not folder_name or not service_name or not username or not password:
            raise ValueError("All fields are required.")
        self.data_manager.add_service(folder_name, service_name, username, password)

    def get_decrypted_password(self, folder_name, service_name):
        """Get a decrypted password for a specific service."""
        folder_data = self.data_manager.get_folder_data(folder_name)
        if service_name not in folder_data:
            raise ValueError(f"Service '{service_name}' not found in folder '{folder_name}'.")
        encrypted_password = folder_data[service_name]["password"]
        return self.data_manager.decrypt_password(encrypted_password)