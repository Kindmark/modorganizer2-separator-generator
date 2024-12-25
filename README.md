# ModOrganizer-SeparatorGenerator

A tool for creating separators for categorization within Mod Organizer 2, making it easier to manage large collections of mods.

This is my first major work in Python, teaching myself the language by converting a Powershell script I made into a Python script (with an easy UI!). And feedback is welcome!

## Features

- Create and manage categories and subcategories for mod organization.
- Customize category headers and appearance.
- Apply themes and color accents to the interface.
- Generate output files for use in Mod Organizer 2.
- Load and save configurations in JSON format.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Furglitch/ModOrganizer-SeparatorGenerator.git
    ```
2. Navigate to the project directory:
    ```sh
    cd ModOrganizer-SeparatorGenerator
    ```

## Usage

### Running the Script

1. Ensure you have Python installed on your system.
2. Run the application:
    ```sh
    python interface.py
    ```

### Building to an Executable with PyInstaller

1. Install PyInstaller if you haven't already:
    ```sh
    pip install pyinstaller
    ```
2. Build the executable:
    ```sh
    pyinstaller -n 'Mod Organizer Separator Generator' --onefile -w interface.py backend.py --add-data "resources;resources" -i 'resources/icon.ico
    ```
3. The executable will be located in the `dist` directory.

## Settings

Any changes you make in the settings menu can be saved with the click of a button. This file is automatically created at launch and updated in the `%APPDATA%/Furglitch/MO2SE/MO2SE.json` directory. 

## Logging

The application logs almost everything to files located in the `%APPDATA%/Furglitch/MO2SE/logs` directory. These logs can be used for troubleshooting and debugging. Please include when reporting an issue.

## Contributing

Contributions, critiques, and bug reports are welcome! If you have any suggestions or improvements, please create a pull request or open an issue.

## License

This project is licensed under the GNU General Public License v3.0.
