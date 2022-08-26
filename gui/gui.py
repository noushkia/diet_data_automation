from tkinter import *
from patinet_form.input_form import generate_input_form


def show_record_form():
    form_screen = Tk()
    form_screen.title("Add doc")
    form_screen.geometry("700x800")

    generate_input_form(form_screen)


def start_up():
    # open a window
    screen = Tk()
    screen.title("Doc manage")
    screen.geometry("700x700")

    # Button for adding a new record
    add_record = Button(text="Add Patient Record", command=show_record_form)
    add_record.pack()

    screen.mainloop()
