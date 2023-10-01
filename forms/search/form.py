import tkinter as tk

from forms.basic_form import BasicForm, place_widgets
from forms.form_config import CHAR_INPUT_WIDTH, LABEL_WIDTH, COL1_X, COL2_X, COL3_X, COL4_X, VDIST


def load_titles():
    return {
        "id": "id",
        "name": "First Name Last Name",
    }


class SearchForm(BasicForm):
    def __init__(self, screen, titles):
        super().__init__(screen, titles)

    def create_form(self):
        x_pos = [COL1_X, COL2_X, COL3_X, COL4_X]

        pos_tracker = 0
        for key in self.titles.keys():
            input_key, input_entry = self._create_input_entry(key)

            entry_width = CHAR_INPUT_WIDTH

            label_width = LABEL_WIDTH
            label_x = x_pos[pos_tracker % 4]
            entry_x = x_pos[pos_tracker % 4 + 1]
            label_y = VDIST * (pos_tracker // 4)
            entry_y = label_y

            label = self._create_label(key, label_width)
            place_widgets(label, input_entry, label_x, label_y, entry_x, entry_y, entry_width)

            pos_tracker += 2

        tk.Button(self.screen, text="Add Record", command=lambda: self.search()).place(
            relx=.5,
            rely=.9,
            anchor="center")

    def search(self):
        # todo
        pass


def create_search_form(screen):
    titles = load_titles()
    search_form = SearchForm(screen, titles)
    search_form.create_form()
