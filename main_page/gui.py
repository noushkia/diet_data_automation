from tkinter import *

from forms.new_patient.form import create_patient_form
from forms.search.form import create_search_form


def show_record_form():
    form_screen = Tk()
    form_screen.title("Add Patient Record")
    form_screen.geometry("800x800")

    create_patient_form(form_screen)


def show_search_form():
    form_screen = Tk()
    form_screen.title("Search")
    form_screen.geometry("800x400")

    create_search_form(form_screen)


def show_patients_analysis():
    analysis_screen = Tk()
    analysis_screen.title("Patients Analysis")
    analysis_screen.geometry("800x800")
    pass


def show_patients_list():
    list_screen = Tk()
    list_screen.title("Patients List")
    list_screen.geometry("800x800")
    pass


def main():
    # open a window
    screen = Tk()
    screen.title("Patient Manager")
    screen.geometry("800x800")

    # Adding a new record #
    add_record = Button(text="Add Patient Record", command=show_record_form)
    add_record.pack()

    # Searching for records
    # search_record = Button(text="Search for Patient", command=show_search_form)
    # search_record.pack()

    screen.mainloop()
