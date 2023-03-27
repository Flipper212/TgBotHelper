import datetime
from lessons_and_time import lesson_time_start, lesson_time_end, week, lesson_time_end_str
from pytz import timezone


def main():
    now_time = str(datetime.datetime.now(timezone('Europe/Kiev')).time())
    hour = now_time.split(":")[0]
    minute = now_time.split(":")[1]
    index = 0  # Номер уроку

    is_start = True  # Чи почалися уроки
    is_end = False  # Чи закінчилися уроки
    is_work_day = True  # Чи робочий день
    is_last = False  # Чи це останній урок

    count_day = datetime.datetime.now().isoweekday()  # порядок дня
    int_time = int(hour + minute)

    #  Перевірка на робочий день
    if count_day in (6, 7):
        return [False, "not work day"]

    elif int_time >= 1430 and 3 <= count_day <= 5 or int_time >= 1520 and 1 <= count_day <= 2:
        return [False, "lessons is over"]
    elif 830 <= int_time < 1430 and 2 < count_day < 6 or 830 <= int_time < 1520 and 0 < count_day < 3:
        if int_time in lesson_time_end:
            while int_time > lesson_time_start[index]:
                index += 1
        else:
            while int_time > lesson_time_end[index]:
                index += 1
    elif int_time < 830:
        lesson_end = lesson_time_start[0]
        is_start = False
        f_hour = 8
        f_minute = 30

    if is_start:
        f_hour = int(lesson_time_end_str[index].split(":")[0])
        f_minute = int(lesson_time_end_str[index].split(":")[1])
    if week[count_day-1][index] == week[count_day-1][-1]:
        is_last = True

    result_str = (f_hour * 3600 + f_minute * 60 - int(hour) * 3600 - int(minute) * 60)//60

    if is_last:
        return [result_str, week[count_day-1][-1], is_start, is_end, is_last, is_work_day]
    elif int_time in lesson_time_end:
        return [result_str, week[count_day - 1][index], is_start, is_end, is_last, is_work_day]
    else:
        return [result_str, week[count_day - 1][index+1], is_start, is_end, is_last, is_work_day]


def make_result():
    main_return = main()
    if main_return[0] is False:
        if main_return[1] == "not work day":
            return "<b>Сьогодні не має уроків</b>🥰"
        elif main_return[1] == "lessons is over":
            return "<b>Уроки закінчились</b>🥰"

    elif main_return[2]:  # Якщо почались уроки
        if main_return[4] is False:
            if main_return[0] > 40:
                return f"<b>{main_return[1]}</b> почнеться через <b>{main_return[0] - 40} хв</b>"
            elif main_return[0] < 40:
                return f"Урок закінчиться через <b>{main_return[0]} хв</b>, наступний <b>{main_return[1]}</b>"
            elif main_return[0] == 40:
                return f"Урок закінчиться через <b>{40} хв</b>, наступний <b>{main_return[1]}</b>"
        elif main_return[4]:
            return f"Урок закінчиться через <b>{main_return[0]} хв</b>, <b>Це останній Урок🥰</b>"

    elif main_return[2] is False:
        return f"<b>{main_return[1]}</b> почнеться через <b>{main_return[0]} хв</b>"
    #  result_str, week[count_day][index], is_start, is_end, is_last, is_work_day
