"""
Dynamically generate word documents using data from a CSV - with 1 template file.
"""
from datetime import datetime
from docxtpl import DocxTemplate


def add_patient_file(n):
    tpl = DocxTemplate("patient_data.docx")  # In same directory
    context = {1: {"name": "کیانوش عرشی", "id": 1, "date": datetime.now(), "tel": "09392299714",
                   "ref": "Kamyar", "occupation": "Student", "age": 21, "birthplace": "Tehran", "bmi": 20,
                   "height": 180, "weight": 63, "complaint": "گشنشه", "drug_history": "None", "medical_history": "None",
                   "test_result": "positive", "plan": "None"}}
    tpl.render(context[n])
    tpl.save("Patients/%s.docx" % str(context[n]["id"]))


if __name__ == '__main__':
    add_patient_file(1)

    print("Done! - Now check your files")
