from bs4 import BeautifulSoup as Bs4
from time import sleep
from datetime import datetime
from undetected_chromedriver import Chrome


def browser(next_week):
    driver = Chrome(executable_path="add/chromedriver", headless=True)
    driver.get("https://nz.ua/login")
    sleep(.5)

    username_input = driver.find_element(by="name", value="LoginForm[login]")
    username_input.send_keys("semenyuk_stanislav4")

    password_input = driver.find_element(by="name", value="LoginForm[password]")
    password_input.send_keys("632140ar")

    button = driver.find_element(by="css selector", value="#login-form > fieldset > div:nth-child(5) > a.ms-button.form-submit-btn")
    button.click()
    sleep(0.5)

    driver.get("https://nz.ua/school16699/schedule/diary")
    sleep(1)

    if next_week:
        next_w = driver.find_element(by="css selector", value="#page > div.main.clear > div.content > div > div:nth-child(2) > div > a.pnl-next")
        next_w.click()
        sleep(1)

    result = driver.page_source
    driver.quit()

    return result


def get_args():
    now_day = datetime.now().isoweekday()
    next_day = now_day if now_day in (1, 2, 3, 4) else 0
    lesson_count = 8 if now_day in (1, 2) else 7
    next_week = not next_day

    source = Bs4(browser(next_week), "lxml")

    today_part = source.find_all("div", class_="dn-item")[next_day]
    lessons = today_part.find_all("div", class_="part-left")
    homework_page = today_part.find_all("div", class_="part-right")

    for i in range(lesson_count):
        try:
            yield lessons_name(lessons[i]), homework_get(homework_page[i])
        except IndexError:
            yield None, None


def lessons_name(less):
    try:
        return less.contents[0].strip()
    except IndexError:
        return None


def homework_get(hom):
    try:
        return hom.text.split("Д/з: ")[1].strip()
    except IndexError:
        return None


def make_string():
    string = ""
    for i in get_args():
        if i[1] is not None and i[0] is not None:
            string += f"<b>{i[0]}</b>: {i[1]}\n\n"
    return string
