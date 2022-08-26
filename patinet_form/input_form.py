from datetime import datetime
from tkinter import *
from add_file import add_patient_file, generate_id
from date.date import gregorian_to_jalali

VDIST = 36
CHAR_INPUT_HEIGHT = 2
CHAR_INPUT_WIDTH = 25
LONG_CHAR_INPUT_WIDTH = 50
TEXT_INPUT_HEIGHT = 4
TEXT_INPUT_WIDTH = 40
COL1_X = 15
COL2_X = COL1_X + 75 * (CHAR_INPUT_WIDTH / 10)
COL3_X = COL2_X + 140
COL4_X = COL3_X + 75 * (CHAR_INPUT_WIDTH / 10)


def register_user(screen, context, char_data):
    for key in char_data:
        context[key] = screen.getvar(name=key)

    try:
        add_patient_file(context)
        Label(screen, text="!پرونده با موفقیت اضافه شد", fg="green").pack()
    except Exception as ex:
        Label(screen, text=str(ex), fg="red").pack()


def generate_input_form(screen):
    farsi_title = {
        "id": "id",
        "name": "نام و نام خانوادگی",
        "city": "محل سکونت",
        "date": "تاریخ",
        "age": "سن",
        "occupation": "شغل",
        "education": "تحصیلات",
        "height": "قد",
        "curr_weight": "وزن فعلی",
        "prev_weight": "وزن قبل بارداری",
        "goal": "هدفتون از رژیم گرفتن چیست",
        "week": "چندمین هفته بارداری هستید",
        "twins": "بارداری دو قلو یا تک جنین",
        "prev_preg": " تعداد بارداری های قبلی",
        "curr_children": "اکنون چند فرزند دارید",
        "natural": "آیا بارداری شما طبیعی بوده یا با روشهای درمان ناباروری، باردار شده اید",
        "sickness": "آیا بیماری دارید",
        "abortion": "آیا در 6 ماه اخیر سقط داشتید",
        "workout": "آیا روزی نیم ساعت پیاده روی تند یا ورزش دارید یا خیر",
        "diabetes": "سابقه دیابت درخودتون یا خانواده دارید",
        "medicine": "دارویی مصرف می کنید",
        "supplement": "مکمل غذایی مصرف می کنید",
        "email": "آدرس ایمیلتان",
        "allergies": "به غذای خاصی حساسیت دارید",
        "bad_food": "از غذایی بدتون میاد",
        "fav_food": "چه غذاهایی را بیشتر دوست دارید",
        "sleep_sched": "معمولا چه ساعتی از خواب بیدار می شوید و  چه ساعتی می خوابید",
        "meal_time": "صبحانه، نهار و شام را چه ساعتی میل می کنید",
    }

    char_inputs = ["id", "name", "city", "date", "age", "occupation", "education", "height", "curr_weight",
                   "prev_weight", "goal", "week", "twins", "prev_preg", "curr_children", "natural",
                   "sickness", "abortion", "workout", "diabetes", "medicine", "supplement",
                   "email", "allergies", "bad_food", "fav_food", "sleep_sched", "meal_time"]

    long_char_inputs = {"natural", "workout", "sleep_sched", "meal_time", "diabetes"}
    char_data = []

    context = {}
    context.fromkeys(char_inputs)

    x_pos = [COL1_X, COL3_X, COL2_X, COL4_X]

    j = 0
    for i, key in enumerate(char_inputs):
        data = StringVar(name=key)
        data_entry = Entry(screen, textvariable=data, justify=RIGHT)
        if key == "id":
            new_id = generate_id()
            data_entry.insert(END, new_id)
        elif key == "date":
            data_entry.insert(END, gregorian_to_jalali(datetime.now()).strftime("%Y/%m/%d"))

        label_width = CHAR_INPUT_WIDTH
        label_x = 500 - x_pos[j % 2]
        label_y = VDIST * (j // 2)
        entry_width = 135
        entry_x = 550 - x_pos[j % 2 + 2]
        entry_y = 5 + VDIST * (j // 2)

        if key in long_char_inputs:
            label_width = LONG_CHAR_INPUT_WIDTH
            label_x = 325 - COL1_X
            entry_width = 200
            entry_x = COL2_X - 100
            j += 1
            if not j % 2:
                label_y = VDIST * (j // 2)
                entry_y = 5 + VDIST * (j // 2)
                j += 1

        Label(screen, text=farsi_title[key], bg="gray55", height=CHAR_INPUT_HEIGHT, width=label_width, borderwidth=1,
              relief="solid").place(x=label_x, y=label_y)
        data_entry.place(x=entry_x, y=entry_y, height=25, width=entry_width)
        char_data.append(key)
        j += 1

    Button(screen, text="اضافه کردن پرونده بیمار", command=lambda: register_user(screen, context, char_data)).place(
        relx=.5,
        rely=.9,
        anchor="center")
