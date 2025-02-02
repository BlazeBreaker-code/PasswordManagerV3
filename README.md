# Password Manager

A secure, user-friendly password manager built with **Python** and **PyQt6**. This application allows users to store, retrieve, and organize passwords in a safe and convenient way, with an added folder system for better organization and management of entries.

## Features
- **Add New Entry**: Easily add new password entries with service names, usernames, and corresponding passwords.
- **Retrieve Password**: Search for stored passwords based on the service name.
- **Folder System**: Organize passwords into folders for easier management and retrieval.
- **Dynamic Window Switching**: Navigate smoothly between different sections of the application.
- **Back Button**: Quickly return to the main menu from any section.

## Technologies Used
- **Python (v3.x)**
- **PyQt6** for building the graphical user interface (GUI)
- **JSON** for secure and simple data storage

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/password-manager.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Adding a New Password Entry
1. Open the application and click on "Add Entry" in the main menu.
2. Choose whether to add the entry to an existing folder or create a new folder.
3. Enter the service name (e.g., Gmail), username, and password.
4. Click Save to add the entry to the password manager.

## Retrieving a Password
1. Click on "Retrieve Password" from the main menu.
2. Select a folder (if you've organized your entries into folders).
3. Enter the service name (e.g., Gmail) to find the associated password.
