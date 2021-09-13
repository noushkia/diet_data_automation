from tkinter import *
from input_form import generate_input_form


def show_record_form():
    form_screen = Tk()
    form_screen.title("Add Record")
    form_screen.geometry("500x800")

    generate_input_form(form_screen)


def start_up():
    # open a window
    screen = Tk()
    screen.title("Test title")
    screen.geometry("500x500")

    # Button for adding a new record
    add_record = Button(text="Add patient record", command=show_record_form)
    add_record.pack()

    screen.mainloop()
