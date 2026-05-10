import tkinter as tk
from tkinter import messagebox

from forms.new_patient.form import create_patient_form, create_lite_patient_form
from forms.search.form import create_search_form


def show_record_form(parent):
    form_screen = tk.Toplevel(parent)
    form_screen.title("Add Patient Record - Full")
    form_screen.geometry("900x900")
    create_patient_form(form_screen)


def show_lite_record_form(parent):
    form_screen = tk.Toplevel(parent)
    form_screen.title("Add Patient Record - Lite")
    form_screen.geometry("500x400")
    create_lite_patient_form(form_screen)


def show_search_form(parent):
    form_screen = tk.Toplevel(parent)
    form_screen.title("Search")
    form_screen.geometry("800x400")
    create_search_form(form_screen)


def main():
    root = tk.Tk()
    root.title("Dietitian Patient Manager")
    root.geometry("400x500")

    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(expand=True, fill="both")

    title_label = tk.Label(main_frame, text="Patient Manager", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    btn_style = {"width": 25, "height": 2, "font": ("Arial", 12)}

    btn_full = tk.Button(main_frame, text="Add Patient (Full)", command=lambda: show_record_form(root), **btn_style)
    btn_full.pack(pady=10)

    btn_lite = tk.Button(main_frame, text="Add Patient (Lite)", command=lambda: show_lite_record_form(root), **btn_style)
    btn_lite.pack(pady=10)

    btn_search = tk.Button(main_frame, text="Search for Patient", command=lambda: show_search_form(root), **btn_style)
    btn_search.pack(pady=10)

    btn_exit = tk.Button(main_frame, text="Exit", command=root.quit, **btn_style, fg="red")
    btn_exit.pack(pady=10)

    root.mainloop()
