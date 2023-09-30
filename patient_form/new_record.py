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

from docxtpl import DocxTemplate
from os import listdir
from os.path import isfile, join
import datetime
from date.date import gregorian_to_jalali

RECORDS_PATH = "db/patients/"
FORMAT = ".docx"
INITIAL_ID = "001"


def add_patient_file(context):
    tpl = DocxTemplate("template.docx")
    tpl.render(context)
    tpl.save(RECORDS_PATH + str(context["id"]) + FORMAT)


def generate_id():
    # find files with .docx extension
    patients_files = [f for f in pathlib.Path(RECORDS_PATH).iterdir() if f.is_file() and f.name.endswith(FORMAT)]

    # Convert to jalali date
    curr_date = gregorian_to_jalali(datetime.datetime.now())

    # Check if there are no records
    if not patients_files:
        return f"{str(curr_date.year)[2:4]}_{curr_date.month:02d}_{INITIAL_ID}"

    latest_file = max(patients_files, key=os.path.getmtime)
    last_year, last_month, last_id = latest_file.stem.split("_")

    # Check if the last record is from the current month
    if str(curr_date.year)[2:4] == last_year and f'{curr_date.month:02d}' == last_month:
        return f"{last_year}_{last_month}_{str(int(last_id) + 1).zfill(3)}"
    # If the last record is from another month
    else:
        return f"{str(curr_date.year)[2:4]}_{curr_date.month:02d}_{INITIAL_ID}"
