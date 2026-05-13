import tkinter as tk
from tkinter import messagebox
import os
import csv
import difflib
import platform
import subprocess

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

    def open_file(self, patient_id):
        # Files are stored in the same directory as the summaries but named by ID
        # Records are in ./db/patients/
        records_dir = os.path.dirname(self.file_path)
        file_path = os.path.join(records_dir, f"{patient_id}.docx")
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File not found: {file_path}")
            return
        
        try:
            if platform.system() == "Windows":
                os.startfile(os.path.abspath(file_path))
            elif platform.system() == "Darwin": # macOS
                subprocess.run(["open", file_path])
            else: # Linux
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

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

                    match_score = 0
                    match = False

                    if input_id and input_id in row_id:
                        match = True
                        match_score += 1.0

                    if input_name:
                        in_name_lower = input_name.lower()
                        row_name_lower = row_name.lower()
                        
                        if in_name_lower in row_name_lower:
                            match = True
                            match_score += 1.0
                        else:
                            ratio = difflib.SequenceMatcher(None, in_name_lower, row_name_lower).ratio()
                            if ratio > 0.4:
                                match = True
                                match_score += ratio
                    
                    if match:
                        found_rows.append((match_score, row))
        except Exception as e:
            messagebox.showerror("Error", f"Could not open database: {e}")
            return

        # Sort found_rows by match_score descending
        found_rows.sort(key=lambda x: x[0], reverse=True)
        final_rows = [row for score, row in found_rows]

        # Display the found rows in the results text widget
        self.results_text.delete(1.0, tk.END)
        if final_rows:
            header = f"{'ID':<15} | {'Name':<25} | {'Age':<5} | {'Date':<15}\n"
            self.results_text.insert(tk.END, header)
            self.results_text.insert(tk.END, "-" * 70 + "\n")
            for row in final_rows:
                patient_id = str(row.get('id', ''))
                name = str(row.get('name',''))
                display_name = reshape_text(name)
                age = str(row.get('age', ''))
                date = str(row.get('date', ''))

                # Note: align might be tricky with reshaped text, but let's try
                id_part = f"{patient_id:<15} | "
                name_part = f"{display_name:<25}"
                rest_part = f" | {age:<5} | {date:<15}\n"

                self.results_text.insert(tk.END, id_part)
                
                # Tag for hyperlink
                tag_name = f"link_{patient_id}"
                self.results_text.insert(tk.END, name_part, tag_name)
                self.results_text.tag_config(tag_name, foreground="blue", underline=True)
                
                # Bindings for the hyperlink
                self.results_text.tag_bind(tag_name, "<Button-1>", lambda e, pid=patient_id: self.open_file(pid))
                self.results_text.tag_bind(tag_name, "<Enter>", lambda e: self.results_text.config(cursor="hand2"))
                self.results_text.tag_bind(tag_name, "<Leave>", lambda e: self.results_text.config(cursor=""))
                
                self.results_text.insert(tk.END, rest_part)
        else:
            self.results_text.insert(tk.END, "No results found.")


def create_search_form(screen):
    titles = load_titles()
    search_form = SearchForm(screen, titles, file_path="./db/patients/patient_summaries.xlsx")
    search_form.create_form()
