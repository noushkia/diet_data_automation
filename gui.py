from tkinter import *
from input_form import generate_input_form


def show_record_form():
    form_screen = Tk()
    form_screen.title("اضافه کردن پرونده")
    form_screen.geometry("700x800")

    generate_input_form(form_screen)


def start_up():
    # open a window
    screen = Tk()
    screen.title("مدیر پرونده")
    screen.geometry("700x700")

    # Button for adding a new record
    add_record = Button(text="اضافه کردن پرونده بیمار", command=show_record_form)
    add_record.pack()

    screen.mainloop()
