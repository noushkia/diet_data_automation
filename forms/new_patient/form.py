from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from date.date import gregorian_to_jalali, JalaliDatePicker
from forms.basic_form import BasicForm, place_widgets

from forms.form_config import CHAR_INPUT_WIDTH, LONG_CHAR_INPUT_WIDTH, LABEL_WIDTH, COL1_X, COL2_X, COL3_X, COL4_X, \
    VDIST
from forms.new_patient.utils import generate_id, add_patient_file, add_patient_summary

TEXT_INPUTS = {"meal_times", "sleep", "complaint", "allergies", "drug_history", "medical_history", "test_result",
               "plan", "meal_pref"}

NUMERIC_FIELDS = {"age", "national_id", "mobile", "ssn", "phone_number", "height", "bmi_weight", "weight", "normal_weight"}


def load_titles(lite=False):
    if lite:
        return {
            "id": "شماره پرونده",
            "name": "نام و نام خانوادگی",
            "age": "سن",
            "ssn": "کد ملی",
            "fathers_name": "نام پدر",
            "phone_number": "شماره تماس",
            "date": "تاریخ",
        }
    return {
        "name": "Name",
        "id": "File No.",
        "tel": "Tel.",
        "date": "Date",
        "occupation": "Occupation",
        "ref": "Referrer",
        "birthplace": "Place of Birth",
        "age": "Age",
        "email": "Email Address",
        "height": "Height (cm)",
        "bmi_weight": "BMI Weight (kg)",
        "weight": "Weight",
        "normal_weight": "Normal Weight",
        "physical": "Physical Activity",
        "goal": "Goal of Diet",
        "meal_times": "Meal Times",
        "meal_pref": "Meal Preference",
        "sleep": "Sleep Sched.",
        "complaint": "CC",
        "allergies": "Allergies",
        "drug_history": "Drug History",
        "medical_history": "PMH",
        "test_result": "Test Result",
        "plan": "Plans",
    }


class PatientForm(BasicForm):
    def __init__(self, screen, titles, lite=False):
        super().__init__(screen, titles)
        self.lite = lite

    def create_form(self):
        x_pos = [COL1_X, COL2_X, COL3_X, COL4_X]

        pos_tracker = 0
        for key in self.titles.keys():
            input_key, input_entry = self._create_input_entry(key)

            if key == "id":
                new_id = generate_id()
                input_entry.insert(tk.END, new_id)
            elif key == "date":
                input_entry.insert(tk.END, gregorian_to_jalali(datetime.now()).strftime("%Y/%m/%d"))
                # Add calendar button
                cal_btn = tk.Button(self.screen, text="📅", 
                                    command=lambda k=key: JalaliDatePicker(self.screen, self.string_vars[k].set))
                
                # We'll place it manually after the widget is placed
                self.date_cal_btn = cal_btn

            if key in NUMERIC_FIELDS:
                self.register_numeric_validation(key)

            entry_width = CHAR_INPUT_WIDTH
            # Text inputs are wider than char inputs
            if key in TEXT_INPUTS:
                pos_tracker += pos_tracker % 4
                entry_width = LONG_CHAR_INPUT_WIDTH

            label_width = LABEL_WIDTH
            if self.lite:
                # Swapped for RTL: Label on right (270), Entry on left (50)
                entry_x = 50
                label_x = 270
                label_y = 50 + (pos_tracker * 40)
                entry_y = label_y
                entry_width = 200
            else:
                label_x = x_pos[pos_tracker % 4]
                entry_x = x_pos[pos_tracker % 4 + 1]
                label_y = VDIST * (pos_tracker // 4)
                entry_y = label_y

            label = self._create_label(key, label_width)
            place_widgets(label, input_entry, label_x, label_y, entry_x, entry_y, entry_width)
            
            if key == "date":
                self.date_cal_btn.place(x=entry_x + entry_width + 5, y=entry_y, height=35)

            if self.lite:
                pos_tracker += 1
            else:
                pos_tracker += 4 if key in TEXT_INPUTS else 2

        tk.Button(self.screen, text="Add Record", command=lambda: self._add_record(), 
                  width=20, height=2, font=("Arial", 12, "bold")).place(
            relx=.5,
            rely=.9,
            anchor="center")

    def _add_record(self):
        # fetch inputted data
        for key in self.titles.keys():
            self.context[key] = self.string_vars[key].get()

        # Fill missing keys for template if it's lite version
        if self.lite:
            all_full_titles = load_titles(lite=False)
            for k in all_full_titles:
                if k not in self.context:
                    self.context[k] = ""

        try:
            # For lite version, we might need to handle BMI differently or set defaults
            if not self.lite:
                add_patient_file(self.context)
            else:
                # Set dummy values for height/weight if they are not in lite form but needed by add_patient_file
                if "height" not in self.context or not self.context["height"]:
                    self.context["height"] = "1" # Avoid division by zero
                if "bmi_weight" not in self.context or not self.context["bmi_weight"]:
                    self.context["bmi_weight"] = "0"
                add_patient_file(self.context, template_name="template_lite.docx")
            
            add_patient_summary(self.context)
            messagebox.showinfo("Success", "Record Added Successfully")
            
            # Reset form and regenerate ID/Date
            self.reset_form()
            new_id = generate_id()
            self.string_vars["id"].set(new_id)
            self.string_vars["date"].set(gregorian_to_jalali(datetime.now()).strftime("%Y/%m/%d"))
            
        except Exception as ex:
            messagebox.showerror("Error", str(ex))


def create_patient_form(screen):
    titles = load_titles(lite=False)
    patient_form = PatientForm(screen, titles, lite=False)
    patient_form.create_form()


def create_lite_patient_form(screen):
    titles = load_titles(lite=True)
    patient_form = PatientForm(screen, titles, lite=True)
    patient_form.create_form()
