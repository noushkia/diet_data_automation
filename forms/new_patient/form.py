from datetime import datetime
import tkinter as tk

from date.date import gregorian_to_jalali

from utils import add_patient_file, add_patient_summary, generate_id

from forms.form_config import CHAR_INPUT_WIDTH, LONG_CHAR_INPUT_WIDTH, LABEL_WIDTH, LABEL_INPUT_HEIGHT, COL1_X, \
    COL2_X, COL3_X, COL4_X, VDIST, INPUT_HEIGHT


def load_titles():
    return {
        "id": "id",
        "name": "First Name Last Name",
        "city": "City",
        "date": "Visit Date",
        "age": "Age",
        "occupation": "Occupation",
        "education": "Education",
        "height": "Height",
        "curr_weight": "Current Weight",
        "prev_weight": "Pre-pregnancy Weight",
        "goal": "Goal of Diet",
        "week": "Week of Pregnancy",
        "twins": "Single or Twins",
        "prev_preg": "Previous Pregnancies",
        "curr_children": "Current Children",
        "natural": "Natural or C-section",
        "sickness": "Significant Sickness",
        "abortion": "Abortion",
        "workout": "Daily Workout",
        "diabetes": "Diabetes",
        "medicine": "Medicine",
        "supplement": "Supplements",
        "email": "Email Address",
        "allergies": "Allergies",
        "bad_food": "Foods You Dislike",
        "fav_food": "Foods You Like",
        "sleep_sched": "Sleep Schedule",
        "meal_time": "Meal Times"
    }


def place_widgets(label, input_entry, label_x, label_y, entry_x, entry_y, entry_width):
    label.place(x=label_x, y=label_y)
    input_entry.place(x=entry_x, y=entry_y, height=INPUT_HEIGHT, width=entry_width)


class PatientForm:
    def __init__(self, screen, titles):
        self.screen = screen
        self.titles = titles
        self.context = {}

    def _create_input_entry(self, key):
        input_key = tk.StringVar(name=key)
        input_entry = tk.Entry(self.screen, textvariable=input_key, justify=tk.RIGHT, borderwidth=1, relief="solid",
                               )
        return input_key, input_entry

    def _create_label(self, key, label_width):
        return tk.Label(self.screen, text=self.titles[key], bg="gray55", height=LABEL_INPUT_HEIGHT,
                        width=label_width, borderwidth=1, relief="solid")

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

            entry_width = CHAR_INPUT_WIDTH
            # Text inputs are wider than char inputs
            if key in TEXT_INPUTS:
                pos_tracker += pos_tracker % 4
                entry_width = LONG_CHAR_INPUT_WIDTH

            label_width = LABEL_WIDTH
            label_x = x_pos[pos_tracker % 4]
            entry_x = x_pos[pos_tracker % 4 + 1]
            label_y = VDIST * (pos_tracker // 4)
            entry_y = label_y

            label = self._create_label(key, label_width)
            place_widgets(label, input_entry, label_x, label_y, entry_x, entry_y, entry_width)

            pos_tracker += 4 if key in TEXT_INPUTS else 2

        tk.Button(self.screen, text="Add Record", command=lambda: self._add_record()).place(
            relx=.5,
            rely=.9,
            anchor="center")

    def _add_record(self):
        # fetch inputted data
        for key in self.titles.keys():
            self.context[key] = self.screen.getvar(name=key)

        try:
            add_patient_file(self.context)
            add_patient_summary(self.context)
            tk.Label(self.screen, text="Record Added Successfully", fg="green").pack()
            self.screen.destroy()
        except Exception as ex:
            tk.Label(self.screen, text=str(ex), fg="red").pack()


def create_patient_form(screen):
    titles = load_titles()
    patient_form = PatientForm(screen, titles)
    patient_form.create_form()
