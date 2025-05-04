# Mod Organizer 2 Separator Generator (MO2SG)
<p align="center"><img src="preview.png"></img></p>

A tool for creating separators for categorization within Mod Organizer 2, making it easier to manage large collections of mods.

> This is my first major work in Python, teaching myself the language by converting a Powershell script I made into a Python script (with an easy UI!). And feedback is welcome!

## Features
- Create and manage categories and subcategories for mod organization.
- Customize category headers and appearance.
- Apply themes and color accents to the interface.
- Generate output files for use in Mod Organizer 2.
- Load and save configurations in JSON format.
- Support for both Windows and Linux

## Installation
### Windows

>#### Easy
> 1. Download the latest [release](https://github.com/Furglitch/ModOrganizer-SeparatorGenerator/releases) 
> 2. Run it!
>
>#### Harder - Build It Yourself!
> 1. Clone the repository and enter it:
> ```powershell
> git clone https://github.com/Furglitch/ModOrganizer-SeparatorGenerator.git
> cd ModOrganizer-SeparatorGenerator
> ```
> 2. Install the requirements
> ```powershell
> pip install -r requirements.txt
> ```
> 3a. Build the executable!
> ```powershell
> pyinstaller -n "MO2SG" --onefile -w interface.py backend.py --add-data "resources;resources" -i "resources/icon.ico"
> ```
> 3b. Run interface.py
> ```bash
> python interface.py
> ```
> You will find the executible in the dist folder.

### Linux

>
> 1. Clone the repository and enter it:
> ```bash
> git clone https://github.com/Furglitch/ModOrganizer-SeparatorGenerator.git
> cd ModOrganizer-SeparatorGenerator
> ```
> 2. Install the requirements
> ```bash
> pip install -r requirements.txt
> ```
> Note: Depending on your distro, you may have to install these through a package manager. (i.e. AUR: `yay -Sy python-pillow tk`)
> 
> 3. Run interface.py
> ```bash
> python interface.py
> ```
> Note: There is also an executable `run.sh` file that does this, if you prefer double-clicking.
>
> Unfortunately, I've yet to figure out how to create an executable file for Linux.<br>
> If you prefer one, you can download the [release](https://github.com/Furglitch/ModOrganizer-SeparatorGenerator/releases) and run it with [Wine](https://www.winehq.org/)

## Usage

### Interface Breakdown
- The Menu Bar is for:
  - Files:
    - Import and Export of the in-progress settings
    - Settings tweaks (themeing, category separator styling, automatic text casing)
  - View:
    - collapsing and expanding categories
  - Examples:
    - Loading preset examples (my personal separator presets)
  - About:
    - Links back to the GitHub and a copy of the License.
- The Category Tree is where you can see your current list, allowing you to adjust as needed using the button bar.
- The Options Bar contains the various options for 
  - The left side lets you set the name of your category/subcategory, and which category a subcategory would fall under.
  - The right side lets you change the gradient, which changes the colors of the category separators, for a nice visual flair to your list.
- The Button Bar has all your adjustment options.
  - Move arrows move the separator selected in the category up and down the list. This is respective to their type, and will not move categories into other categories, or subcategories out of their own subcategories.
  - The 'Add/Remove Separator' buttons do just as they say, add or remove separators to your in-progress list, based on the settings in the left side of the Options Bar.
  - 'Generate Files' generates the files that need to be added to your MO2 instance root folder. It will allow you to change the output destination.

### IMPORTANT - MUST READ
- The generated files (a `mods` folder and a `profiles` folder) *must* be placed in the root folder of your MO2 instance, otherwise the changes will not take effect.
- It is well advised to use this with a **fresh** install of Mod Organizer 2. Using it with an existing MO2 instance will **DESTROY** your current modlist order.
- If you are insistent on putting it in an existing instance, remove all the folders in the existing `mods` folder that end with `_separator`. For the profiles folder, I'd make a backup of the existing modlist.txt within `/profiles/{PROFILENAME}`. When the new modlist.txt is added, you can copy over the names of the mods from the old txt, or sort them in the MO2 interface.
- This program generates files for the 'Default' instance profile. If you wish to rename it, change the name of the `Default` folder within the `profiles` folder


## Settings
Any changes you make in the settings menu can be saved with the click of a button.</br>
**Windows:** `%APPDATA%/Furglitch/MO2SG`</br>
**Linux:** `$HOME/.config/furglitch/MO2SG`</br>
This file is automatically created at launch and updated in the following directory:</br>

## Logging
The application logs almost everything to files located in the following directory:</br>
**Windows:** `%APPDATA%/Furglitch/MO2SG/logs`</br>
**Linux:** `$HOME/.config/furglitch/MO2SG/logs`</br>
These logs can be used for troubleshooting and debugging. Please include when reporting an issue.</br>

## Contributing
Contributions, critiques, and bug reports are welcome! If you have any suggestions or improvements, please create a pull request or open an issue.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
