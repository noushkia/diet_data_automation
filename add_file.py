"""
Dynamically generate word documents using data from a graphic form - with 1 template file.
"""
from docxtpl import DocxTemplate


def add_patient_file(context):
    tpl = DocxTemplate("patient_data.docx")
    tpl.render(context)
    tpl.save("Patients/%s.docx" % str(context["id"]))
