Password Manager
A secure, user-friendly password manager built with Python and PyQt6. This application allows users to store, retrieve, and organize passwords in a safe and convenient way, with an added folder system for better organization and management of entries.

Features
Add New Entry: Easily add new password entries with service names, usernames, and corresponding passwords.
Retrieve Password: Search for stored passwords based on the service name.
Folder System: Organize passwords into folders for easier management and retrieval.
Dynamic Window Switching: Navigate smoothly between different sections of the application.
Back Button: Quickly return to the main menu from any section.
Technologies Used
Python (v3.x)
PyQt6 for building the graphical user interface (GUI)
JSON for secure and simple data storage
Installation
Clone the repository:

bash
Copy
git clone https://github.com/yourusername/password-manager.git
Install dependencies:

bash
Copy
pip install -r requirements.txt
Run the application:

bash
Copy
python main.py
Usage
Adding a New Password Entry
Open the application and click on "Add Entry" in the main menu.
Choose whether to add the entry to an existing folder or create a new folder.
Enter the service name (e.g., Gmail), username, and password.
Click Save to add the entry to the password manager.
Retrieving a Password
Click on "Retrieve Password" from the main menu.
Select a folder (if you've organized your entries into folders).
Enter the service name (e.g., Gmail) to find the associated password
