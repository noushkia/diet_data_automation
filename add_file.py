"""
Dynamically generate word documents using data from a graphic form - with 1 template file.
"""
from docxtpl import DocxTemplate
from os import listdir
from os.path import isfile, join
from datetime import datetime

PATH = "Patients/"
FORMAT = ".docx"
INITIAL_ID = "100"


def add_patient_file(context):
    tpl = DocxTemplate("patient_data.docx")
    tpl.render(context)
    tpl.save(PATH + str(context["id"]) + FORMAT)


def generate_id():
    # find files with .docx extension
    patients_files = [f for f in listdir(PATH) if isfile(join(PATH, f)) and f.__contains__(FORMAT)]

    # check the last added file for id and date it was added and generate the id respectively
    if not patients_files:
        return str(datetime.now().year)[2:4] + f'{datetime.now().month:02d}' + INITIAL_ID
    last_id = patients_files[-1]
    if str(datetime.now().year)[2:4] == last_id[0:2] and f'{datetime.now().month:02d}' == last_id[2:4]:
        return last_id[0:4] + str(int(last_id[4:7])+1)
    else:
        return str(datetime.now().year)[2:4] + f'{datetime.now().month:02d}' + INITIAL_ID
