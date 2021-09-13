import datetime


def gregorian_to_jalali(date: datetime):
    """
    Convert gregorian date to Jalali date

    https://github.com/slashmili/python-jalali
    """
    g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

    gy = date.year - 1600
    gm = date.month - 1
    gd = date.day - 1

    g_day_no = 365 * gy + (gy + 3) // 4 - (gy + 99) // 100 + (gy + 399) // 400

    for i in range(gm):
        g_day_no += g_days_in_month[i]
    if gm > 1 and ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        # leap and after Feb
        g_day_no += 1
    g_day_no += gd

    j_day_no = g_day_no - 79

    j_np = j_day_no // 12053
    j_day_no %= 12053
    jy = 979 + 33 * j_np + 4 * int(j_day_no // 1461)

    j_day_no %= 1461

    if j_day_no >= 366:
        jy += (j_day_no - 1) // 365
        j_day_no = (j_day_no - 1) % 365

    for i in range(11):
        if not j_day_no >= j_days_in_month[i]:
            i -= 1
            break
        j_day_no -= j_days_in_month[i]

    jm = i + 2
    jd = j_day_no + 1

    j_date = datetime.date(jy, jm, jd)

    return j_date
