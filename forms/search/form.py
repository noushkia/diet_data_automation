import tkinter as tk
from tkinter import messagebox
import os
import csv

from forms.basic_form import BasicForm, place_widgets
from forms.form_config import CHAR_INPUT_WIDTH, LABEL_WIDTH, COL1_X, COL2_X, COL3_X, COL4_X, VDIST
from date.date import reshape_text


def load_titles():
    return {
        "id": "ID / شماره پرونده",
        "name": "Name / نام",
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
            label_y = VDIST * (pos_tracker // 4 + 1)
            entry_y = label_y

            label = self._create_label(key, label_width)
            place_widgets(label, input_entry, label_x, label_y, entry_x, entry_y, entry_width)

            pos_tracker += 2

        # Create a text widget to display the results
        self.results_text = tk.Text(self.screen, height=15, width=80)
        self.results_text.place(relx=0.5, rely=0.6, anchor="center")

        tk.Button(self.screen, text="Search", command=lambda: self.search(), width=20, height=2).place(
            relx=.5,
            rely=.9,
            anchor="center")

    def search(self):
        # We now check for CSV or XLSX but prefer CSV for lite version
        csv_path = self.file_path.replace(".xlsx", ".csv")
        
        if not os.path.exists(csv_path):
            messagebox.showwarning("Warning", f"No patient records found (database file missing: {csv_path}).")
            return

        input_id = self.string_vars["id"].get().strip()
        input_name = self.string_vars["name"].get().strip()

        if not input_id and not input_name:
            messagebox.showinfo("Info", "Please enter ID or Name to search.")
            return

        found_rows = []
        try:
            with open(csv_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row_id = str(row.get("id", ""))
                    row_name = str(row.get("name", ""))

                    match = False
                    if input_id and input_id in row_id:
                        match = True
                    if input_name and input_name.lower() in row_name.lower():
                        match = True
                    
                    if match:
                        found_rows.append(row)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open database: {e}")
            return

        # Display the found rows in the results text widget
        self.results_text.delete(1.0, tk.END)
        if found_rows:
            header = f"{'ID':<15} | {'Name':<25} | {'Age':<5} | {'Date':<15}\n"
            self.results_text.insert(tk.END, header)
            self.results_text.insert(tk.END, "-" * 70 + "\n")
            for row in found_rows:
                name = str(row.get('name',''))
                display_name = reshape_text(name)
                # Note: align might be tricky with reshaped text, but let's try
                res_str = f"{str(row.get('id','')):<15} | {display_name:<25} | {str(row.get('age','')):<5} | {str(row.get('date','')):<15}\n"
                self.results_text.insert(tk.END, res_str)
        else:
            self.results_text.insert(tk.END, "No results found.")


def create_search_form(screen):
    titles = load_titles()
    search_form = SearchForm(screen, titles, file_path="./db/patients/patient_summaries.xlsx")
    search_form.create_form()
