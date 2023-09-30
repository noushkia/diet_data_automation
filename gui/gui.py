from tkinter import *
from patient_form.input_form import create_patient_form


def show_record_form():
    form_screen = Tk()
    form_screen.title("Add Patient Record")
    form_screen.geometry("800x800")

    create_patient_form(form_screen)


def main():
    # open a window
    screen = Tk()
    screen.title("Patient Manager")
    screen.geometry("800x800")

    # Adding a new record #
    add_record = Button(text="Add Patient Record", command=show_record_form)
    add_record.pack()

    screen.mainloop()
