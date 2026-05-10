"""
    Add new patient record to the database.
    The database is a directory of .docx files.
    Each file is a record of a patient.
    The file name format is current year and month + 3-digit id.
    For example, 9901001.docx
    The id is generated automatically.
    The file is generated from a template (template.docx).
    The template is a Word document with placeholders.
    The placeholders are replaced with the data from the form.
    The placeholders are the same as the keys in the context dictionary.
    The context dictionary is generated from the form.
    The form is a tkinter window.
    The form is generated from the char_data dictionary.
"""
import os
import pathlib
import re
import csv

from docxtpl import DocxTemplate
import datetime

from date.date import gregorian_to_jalali

RECORDS_PATH = "./db/patients/"
SUMMARIES_FILE = "patient_summaries.csv"
FORMAT = ".docx"
INITIAL_ID = "001"


def calculate_bmi(weight: float, height: float) -> float:
    """
    Calculate BMI given the weight and height.
    :param weight: weight in kg
    :param height: height in cm
    :return: BMI
    """
    if height == 0:
        return 0
    return weight / ((height / 100) ** 2)


def add_patient_file(context):
    if not os.path.exists(RECORDS_PATH):
        os.makedirs(RECORDS_PATH)

    tpl = DocxTemplate("template.docx")
    
    try:
        weight = float(context.get("bmi_weight", 0) or 0)
        height = float(context.get("height", 0) or 1)
        bmi = calculate_bmi(weight, height)
        context["bmi"] = f"{bmi:.2f}"
    except (ValueError, TypeError):
        context["bmi"] = "N/A"

    tpl.render(context)
    tpl.save(RECORDS_PATH + str(context["id"]) + FORMAT)


def add_patient_summary(context):
    if not os.path.exists(RECORDS_PATH):
        os.makedirs(RECORDS_PATH)

    # Store patient summaries in a CSV file (Lighter than Excel)
    summary_data = {
        "id": context.get("id", ""),
        "name": context.get("name", ""),
        "father_name": context.get("father_name", ""),
        "age": context.get("age", ""),
        "national_id": context.get("national_id", ""),
        "mobile": context.get("mobile", ""),
        "birthplace": context.get("birthplace", ""),
        "occupation": context.get("occupation", ""),
        "height": context.get("height", ""),
        "weight": context.get("weight", ""),
        "date": context.get("date", ""),
    }

    summary_file_path = RECORDS_PATH + SUMMARIES_FILE
    file_exists = os.path.isfile(summary_file_path)

    # Append the new data to the CSV file
    try:
        with open(summary_file_path, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=summary_data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(summary_data)
    except Exception as e:
        print(f"Error saving CSV summary: {e}")


def generate_id():
    if not os.path.exists(RECORDS_PATH):
        os.makedirs(RECORDS_PATH)

    curr_date = gregorian_to_jalali(datetime.datetime.now())

    patients_files = [
        f for f in pathlib.Path(RECORDS_PATH).iterdir()
        if f.is_file() and re.match(fr"{str(curr_date.year)[2:4]}_{curr_date.month:02d}_\d{{3}}\.docx$", f.name)
    ]

    if not patients_files:
        return f"{str(curr_date.year)[2:4]}_{curr_date.month:02d}_{INITIAL_ID}"

    sorted_files = sorted(patients_files, key=lambda f: (
        int(f.stem.split("_")[2])
    ))

    latest_file = sorted_files[-1]

    try:
        last_year, last_month, last_id = latest_file.stem.split("_")
    except ValueError:  # .docx file name formats are invalid
        return f"{str(curr_date.year)[2:4]}_{curr_date.month:02d}_{INITIAL_ID}"

    # Check if the last record is from the current month
    if str(curr_date.year)[2:4] == last_year and f'{curr_date.month:02d}' == last_month:
        return f"{last_year}_{last_month}_{str(int(last_id) + 1).zfill(3)}"
    # If the last record is from another month
    else:
        return f"{str(curr_date.year)[2:4]}_{curr_date.month:02d}_{INITIAL_ID}"
