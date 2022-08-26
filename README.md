# diet_data_automation

## Requirements
    Install the following packages:
    `sudo apt-get install python3-tk
    `pip install -r requirements.txt

## Introduction
This is a project to automate the process of adding data to the nutritionists patients database.
The app currently has the following features:
    1. Add New Patient Data
    2. Export Data to CSV
    3. Import Data from CSV

### Adding New Patient Data
This feature allows the user to add new patient data to the database.
The user can add a new patient by entering the patient's data into the form generated using TKinter.
After entering the data, the user can click the "Add Patient" button to add the patient to the database.
This action generates a .xlsx file based on the given template and stores it in the db directory.

### Export Data to CSV

### Import Data from CSV

## Generating Executable File
To generate .exe file simply type the following command in the terminal:

`pyinstaller.exe --onefile --icon=icon.ico main.py`
