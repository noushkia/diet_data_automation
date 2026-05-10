import tkinter as tk
from abc import abstractmethod, ABC

try:
    from awesometkinter.bidirender import add_bidi_support
except ImportError:
    def add_bidi_support(w): pass

from forms.form_config import LABEL_INPUT_HEIGHT, INPUT_HEIGHT
from date.date import is_farsi, reshape_text

# Common Farsi-friendly fonts on Linux
FARSI_FONTS = ("DejaVu Sans", "FreeSans", "Arial", "Tahoma")


def place_widgets(label, input_entry, label_x, label_y, entry_x, entry_y, entry_width):
    label.place(x=label_x, y=label_y)
    input_entry.place(x=entry_x, y=entry_y, height=INPUT_HEIGHT, width=entry_width)


def get_best_font(size=11):
    # Just return the first one from the list for now
    return (FARSI_FONTS[0], size)


class BasicForm(ABC):
    def __init__(self, screen, titles):
        self.screen = screen
        self.titles = titles
        self.context = {}
        self.string_vars = {}
        self.entries = {}

    def _create_input_entry(self, key):
        input_key = tk.StringVar(name=key)
        self.string_vars[key] = input_key
        
        # Use a better font for Farsi characters
        font = get_best_font()
        input_entry = tk.Entry(self.screen, textvariable=input_key, justify=tk.RIGHT, 
                               borderwidth=1, relief="solid", font=font)
        self.entries[key] = input_entry
        
        # Add live RTL/BiDi support for connected letters
        add_bidi_support(input_entry)
        
        # Dynamic justification binding
        input_entry.bind("<KeyRelease>", lambda e, k=key: self._check_rtl(k))
        
        return input_key, input_entry

    def _check_rtl(self, key):
        entry = self.entries[key]
        text = self.string_vars[key].get()
        if is_farsi(text):
            entry.config(justify=tk.RIGHT)
        else:
            if key not in ["age", "id", "national_id", "mobile", "height", "weight", "bmi_weight", "tel"]:
                entry.config(justify=tk.LEFT)

    def _create_label(self, key, label_width):
        title = self.titles[key]
        display_text = reshape_text(title)
        return tk.Label(self.screen, text=display_text, bg="gray55", height=LABEL_INPUT_HEIGHT,
                        width=label_width, borderwidth=1, relief="solid", font=get_best_font(10))

    def register_numeric_validation(self, key):
        vcmd = (self.screen.register(self._validate_numeric), '%P')
        self.entries[key].config(validate='key', validatecommand=vcmd)

    def _validate_numeric(self, P):
        if P == "" or P.isdigit():
            return True
        return False

    def reset_form(self):
        for key in self.string_vars:
            self.string_vars[key].set("")

    @abstractmethod
    def create_form(self):
        pass
