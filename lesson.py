import datetime


monday = ["Фізкультура", "Географія", "Геометрія", "Геометрія", "Фізика", "Історія", "Укр літ", "СК"]
tuesday = ["Алгебра", "Алгебра", "Історія", "Трудове", "Англ/Укр мова", "Фізика", "Заруб літ", "Інформатика/Англ мова"]
wednesday = ["Алгебра", "Алгебра", "Укр мова/Інформ", "Укр літ", "Інформ/Укр мова", "Фізкультура", "Фізика"]
thursday = ["Мистецтво", "ОЗ", "Геометрія", "Укр мова/Інформ", "Англ мова", "Хімія", "Біологія"]
friday = ["Право", "Алгебра", "Хімія", "Географія", "Біологія", "Історія", "Фізкультура"]
week = [None, monday, tuesday, wednesday, thursday, friday]
# None забирає індекс 0

lesson_time = {"8:30": "9:10", "9:20": "10:00", "10:10": "10:50", "11:00": "11:40", "12:00": "12:40",
                   "13:00": "13:40", "13:50": "14:30", "14:40": "15:20"}
lesson_time_int = {"830": "910", "920": "1000", "1010": "1050", "1100": "1140", "1200": "1240",
                   "1300": "1340", "1350": "1430", "1440": "1520"}


def main():
    now_time = str(datetime.datetime.now().time())
    hour = now_time.split(":")[0]
    minute = now_time.split(":")[1]
    index = 0
    lesson_fix_time = None

    is_start = True
    is_end = False
    is_work_day = True
    global count_day
    count_day = 1#datetime.datetime.now().weekday()

    if count_day in (0, 6):
        return False

    if 0 < count_day < 6:
        if str(hour)[0] == "0":
            time_str = int("".join([str(hour)[1:], str(minute)]))
        else:
            time_str = int("".join([str(hour), str(minute)]))
    if time_str < 830:
        lesson_fix_time = list(lesson_time.keys())[0]
        is_start = False
    elif 830 <= time_str < 1430 and 2 < count_day < 6 or 830 <= time_str < 1520 and 0 < count_day < 3:
        while int(list(lesson_time_int.values())[index]) < time_str:
            index += 1
    elif time_str > 1430 and 2 < count_day < 6:
        is_end = True
    elif time_str > 1520 and 0 < count_day < 3:
        is_end = True

    if is_start:
        lesson_fix_time = list(lesson_time.values())[index]

    f_hour = lesson_fix_time.split(":")[0]
    f_minute = lesson_fix_time.split(":")[1]

    try:
        f_hour = int(f_hour)
    except ValueError:
        f_hour = int(f_hour[-1])

    try:
        f_minute = int(f_minute)
    except ValueError:
        f_hour = int(f_minute[-1])

    try:
        hour = int(hour)
    except ValueError:
        hour = int(hour[-1])

    try:
        minute = int(minute)
    except ValueError:
        hour = int(minute[-1])

    result_str = (int(f_hour) * 3600 + int(f_minute) * 60 - int(hour) * 3600 - int(minute) * 60)//60
    return [result_str, week[count_day][index+1], is_start, is_end]
