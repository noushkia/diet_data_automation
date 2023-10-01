import tkinter as tk
from abc import abstractmethod, ABC

from forms.form_config import LABEL_INPUT_HEIGHT, INPUT_HEIGHT


def place_widgets(label, input_entry, label_x, label_y, entry_x, entry_y, entry_width):
    label.place(x=label_x, y=label_y)
    input_entry.place(x=entry_x, y=entry_y, height=INPUT_HEIGHT, width=entry_width)


class BasicForm(ABC):
    def __init__(self, screen, titles):
        self.screen = screen
        self.titles = titles
        self.context = {}

    def _create_input_entry(self, key):
        input_key = tk.StringVar(name=key)
        input_entry = tk.Entry(self.screen, textvariable=input_key, justify=tk.RIGHT, borderwidth=1, relief="solid")
        return input_key, input_entry

    def _create_label(self, key, label_width):
        return tk.Label(self.screen, text=self.titles[key], bg="gray55", height=LABEL_INPUT_HEIGHT,
                        width=label_width, borderwidth=1, relief="solid")

    @abstractmethod
    def create_form(self):
        pass
