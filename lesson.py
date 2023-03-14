import datetime
from lessons_and_time import lesson_time_start, lesson_time_end, week, lesson_time_end_str


def main():
    now_time = str(datetime.datetime.now().time())
    hour = int(now_time.split(":")[0])
    minute = int(now_time.split(":")[1])
    index = 0  # Номер уроку

    is_start = True  # Чи почалися уроки
    is_end = False  # Чи закінчилися уроки
    is_work_day = True  # Чи робочий день
    is_last = False  # Чи це останній урок
    count_day = datetime.datetime.now().isoweekday()  # порядок дня
    int_time = int(str(hour) + str(minute))

    #  Перевірка на робочий день
    if count_day in (6, 7):
        return [False, "not work day"]

    if int_time >= 1430 and 3 <= count_day <= 5 or int_time >= 1520 and 1 <= count_day <= 2:
        return [False, "lessons is over"]
    elif int_time < 830:
        lesson_end = lesson_time_start[0]
        is_start = False
    elif 830 <= int_time < 1430 and 2 < count_day < 6 or 830 <= int_time < 1520 and 0 < count_day < 3:
        while int(lesson_time_end[index]) < int_time:
            index += 1

    if is_start:
        lesson_end = str(lesson_time_end[index])

    f_hour = int(lesson_time_end_str[index].split(":")[0])
    f_minute = int(lesson_time_end_str[index].split(":")[1])
    print(f_hour, f_minute)
    if week[count_day+1][index] == week[count_day][-1]:
        is_last = True

    result_str = (f_hour * 3600 + f_minute * 60 - int(hour) * 3600 - int(minute) * 60)//60

    return [result_str, week[count_day-1][index], is_start, is_end, is_last, is_work_day]


main_return = main()


def make_result():
    if main_return[0] is False:
        if main_return[1] == "not work day":
            return "<b>Сьогодні не має уроків</b>🥰"
        elif main_return[1] == "lessons is over":
            return "<b>Уроки закінчились</b>🥰"

    elif main_return[2]:  # Якщо почались уроки
        if main_return[0] > 40 and main_return[4] is False:
            return f"<b>{main_return[1]}</b> почнеться через <b>{main_return[0] - 40} хв</b>"
        elif main_return[4] is False:
            return f"Урок закінчиться через <b>{main_return[0]} хв</b>, наступний <b>{main_return[1]}</b>"
        elif main_return[4]:
            return f"Урок закінчиться через <b>{main_return[0]} хв</b>, <b>Це останній Урок🥰</b>"

    elif main_return[2] is False:
        return f"<b>{main_return[1]}</b> почнеться через <b>{main_return[0] - 40} хв</b>"

    #  result_str, week[count_day][index], is_start, is_end, is_last, is_work_day
