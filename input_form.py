from datetime import datetime
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from add_file import add_patient_file, generate_id

CHAR_INPUT_HEIGHT = 2
CHAR_INPUT_WIDTH = 10
TEXT_INPUT_HEIGHT = 4
TEXT_INPUT_WIDTH = 40
COL1_X = 15
COL2_X = 100
COL3_X = 240
COL4_X = 325


def register_user(screen, context, char_data, text_data):
    for key in char_data:
        context[key] = screen.getvar(name=key)

    for key, data in text_data.items():
        context[key] = data.get("1.0", END)

    try:
        add_patient_file(context)
        Label(screen, text="Record added successfully!", fg="green").pack()
    except Exception as ex:
        Label(screen, text=str(ex), fg="red").pack()


def generate_input_form(screen):
    char_inputs = ["name", "id", "date", "tel", "ref", "occupation", "age", "birthplace", "bmi", "height", "weight"]
    char_data = []

    text_inputs = ["complaint", "drug_history", "medical_history", "test_result", "plan"]
    text_data = {}
    text_data.fromkeys(text_inputs)

    context = {}
    context.fromkeys(char_inputs)
    context.fromkeys(text_inputs)

    x_pos = [COL1_X, COL3_X, COL2_X, COL4_X]

    for i, key in enumerate(char_inputs):
        title = key.capitalize()
        data = StringVar(name=key)
        data_entry = Entry(screen, textvariable=data)
        if key == "id":
            new_id = generate_id()
            data_entry.insert(END, new_id)
        elif key == "date":
            data_entry.insert(END, datetime.now().date().strftime("%d/%m/%Y"))

        Label(screen, text=title, bg="grey", height=CHAR_INPUT_HEIGHT, width=CHAR_INPUT_WIDTH, borderwidth=1,
              relief="solid").place(x=x_pos[i % 2], y=30 * (i // 2))
        data_entry.place(x=x_pos[i % 2 + 2], y=5 + 30 * (i // 2))
        char_data.append(key)

    for i, key in enumerate(text_inputs):
        title = key.replace('_', ' ').capitalize()
        data_entry = ScrolledText(screen, wrap=WORD, width=TEXT_INPUT_WIDTH, height=TEXT_INPUT_HEIGHT)
        Label(screen, text=title, bg="grey", height=TEXT_INPUT_HEIGHT, width=CHAR_INPUT_WIDTH, borderwidth=1,
              relief="solid").place(x=COL1_X, y=len(char_inputs) * 20 + 90 * i)
        data_entry.place(x=COL2_X, y=len(char_inputs) * 20 + 90 * i)
        text_data[key] = data_entry

    Button(screen, text="Add Record", command=lambda: register_user(screen, context, char_data, text_data)).place(
        relx=.5,
        rely=.9,
        anchor="center")
