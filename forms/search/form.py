import tkinter as tk

import openpyxl

from forms.basic_form import BasicForm, place_widgets
from forms.form_config import CHAR_INPUT_WIDTH, LABEL_WIDTH, COL1_X, COL2_X, COL3_X, COL4_X, VDIST


def load_titles():
    return {
        "id": "id",
        "name": "First Name Last Name",
    }


class SearchForm(BasicForm):
    def __init__(self, screen, titles, file_path):
        super().__init__(screen, titles)
        self.file_path = file_path
        self.results_text = None

    def create_form(self):
        x_pos = [COL1_X, COL2_X, COL3_X, COL4_X]

        pos_tracker = 0
        for key in self.titles.keys():
            input_key, input_entry = self._create_input_entry(key)

            entry_width = CHAR_INPUT_WIDTH

            label_width = LABEL_WIDTH
            label_x = x_pos[pos_tracker % 4]
            entry_x = x_pos[pos_tracker % 4 + 1]
            label_y = VDIST * (pos_tracker // 4)
            entry_y = label_y

            label = self._create_label(key, label_width)
            place_widgets(label, input_entry, label_x, label_y, entry_x, entry_y, entry_width)

            pos_tracker += 2

        # Create a text widget to display the results
        self.results_text = tk.Text(self.screen, height=10, width=60)
        self.results_text.place(relx=0.5, rely=0.6, anchor="center")

        tk.Button(self.screen, text="Search", command=lambda: self.search()).place(
            relx=.5,
            rely=.9,
            anchor="center")

    def search(self):
        input_id = self.screen.getvar(name="id")
        input_name = self.screen.getvar(name="name")

        # Open the Excel file
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook.active

        found_rows = []

        # Iterate over the rows in the sheet
        # todo: Set the id and name column based on the file?
        for row in sheet.iter_rows(values_only=True):
            row_id = row[0]
            row_name = row[1]

            # Check if the input matches the row data
            if input_id and input_id == row_id:
                found_rows.append(row)
            # todo: upgrade the name search functionality
            elif input_name and input_name.lower() == row_name.lower():
                found_rows.append(row)

        # Close the workbook
        workbook.close()

        # Do something with the found rows (e.g., display them)
        print(found_rows)

        # Display the found rows in the results text widget
        self.results_text.delete(1.0, tk.END)
        if found_rows:
            for row in found_rows:
                self.results_text.insert(tk.END, str(row) + "\n")
        else:
            self.results_text.insert(tk.END, "No results found.")  # 02_10_001


def create_search_form(screen):
    titles = load_titles()
    search_form = SearchForm(screen, titles, file_path="./db/patients/patient_summaries.xlsx")
    search_form.create_form()
