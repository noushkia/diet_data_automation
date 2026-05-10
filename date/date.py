import datetime
import tkinter as tk

import arabic_reshaper
import jdatetime
from bidi.algorithm import get_display

# Common Farsi-friendly fonts on Linux
FARSI_FONTS = ("DejaVu Sans", "FreeSans", "Arial", "Tahoma")


def get_best_font(size=11):
    return (FARSI_FONTS[0], size)


class JalaliDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def strftime(self, format_str):
        # Basic implementation of strftime for JalaliDate
        res = format_str.replace("%Y", str(self.year))
        res = res.replace("%m", f"{self.month:02d}")
        res = res.replace("%d", f"{self.day:02d}")
        return res

    def __str__(self):
        return self.strftime("%Y/%m/%d")


def gregorian_to_jalali(date_obj: datetime.date):
    """
    Convert gregorian date to Jalali date using jdatetime
    """
    j_date = jdatetime.date.fromgregorian(date=date_obj)
    return JalaliDate(j_date.year, j_date.month, j_date.day)


def is_farsi(text):
    """Check if the text contains Farsi/Arabic characters."""
    for char in text:
        if '\u0600' <= char <= '\u06FF':
            return True
    return False


def reshape_text(text):
    """Reshape and apply BiDi to Farsi text for correct display in Tkinter."""
    if not is_farsi(text):
        return text
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text


class JalaliDatePicker(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Select Jalali Date")
        self.callback = callback
        self.current_jdate = jdatetime.date.today()
        self.selected_date = None

        self.geometry("600x450")  # Increased again for safety
        self.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Header: Year and Month selectors
        header = tk.Frame(self)
        header.pack(fill="x", pady=10)

        tk.Button(header, text="<", command=self.prev_month, font=get_best_font(12)).pack(side="left", padx=5)

        self.month_label = tk.Label(header, text=reshape_text(self.current_jdate.strftime("%B %Y")),
                                    font=get_best_font(14))
        self.month_label.pack(side="left", expand=True)

        tk.Button(header, text=">", command=self.next_month, font=get_best_font(12)).pack(side="right", padx=5)

        # Days of week header
        days_header = tk.Frame(self)
        days_header.pack(fill="x")
        # In jdatetime Saturday is 0, Sunday is 1, ..., Friday is 6.
        # We display them from right to left.
        week_days = ["ش", "ی", "د", "س", "چ", "پ", "ج"]
        for day in week_days:
            tk.Label(days_header, text=reshape_text(day), width=5, font=get_best_font(12)).pack(side="right", padx=2)

        # Days grid
        self.days_frame = tk.Frame(self)
        self.days_frame.pack(fill="both", expand=True, pady=5)
        self.draw_calendar()

    def draw_calendar(self):
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        first_day = self.current_jdate.replace(day=1)
        # In jdatetime, Saturday is 0.
        start_day_index = first_day.weekday()

        # Calculate exactly how many days are in the current month
        if self.current_jdate.month == 12:
            next_month = jdatetime.date(self.current_jdate.year + 1, 1, 1)
        else:
            next_month = jdatetime.date(self.current_jdate.year, self.current_jdate.month + 1, 1)

        days_in_month = (next_month - jdatetime.timedelta(days=1)).day

        row = 0
        col_idx = start_day_index
        for day in range(1, days_in_month + 1):
            btn = tk.Button(self.days_frame, text=str(day), width=5, height=2,
                            font=get_best_font(11),
                            command=lambda d=day: self.select_day(d))
            # Saturday (0) should be at col 6 (right-most)
            # Sunday (1) should be at col 5
            # ...
            # Friday (6) should be at col 0 (left-most)
            btn.grid(row=row, column=6 - col_idx, padx=2, pady=2)
            col_idx += 1
            if col_idx > 6:
                col_idx = 0
                row += 1

        self.month_label.config(text=reshape_text(self.current_jdate.strftime("%B %Y")))

    def prev_month(self):
        month = self.current_jdate.month - 1
        year = self.current_jdate.year
        if month < 1:
            month = 12
            year -= 1
        self.current_jdate = self.current_jdate.replace(year=year, month=month, day=1)
        self.draw_calendar()

    def next_month(self):
        month = self.current_jdate.month + 1
        year = self.current_jdate.year
        if month > 12:
            month = 1
            year += 1
        self.current_jdate = self.current_jdate.replace(year=year, month=month, day=1)
        self.draw_calendar()

    def select_day(self, day):
        self.selected_date = self.current_jdate.replace(day=day)
        self.callback(self.selected_date.strftime("%Y/%m/%d"))
        self.destroy()
