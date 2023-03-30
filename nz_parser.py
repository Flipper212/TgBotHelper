from bs4 import BeautifulSoup as Bs4
from time import sleep
import undetected_chromedriver as uc
from datetime import datetime


def browser():
    options = uc.ChromeOptions()
    driver = uc.Chrome(chrome_executable_path="add/chromedriver", options=options, headless=True, version_main=90)
    driver.get("https://nz.ua/login")
    sleep(1)
    username_input = driver.find_element(by="name", value="LoginForm[login]")
    username_input.send_keys("semenyuk_stanislav4")

    password_input = driver.find_element(by="name", value="LoginForm[password]")
    password_input.send_keys("632140ar")

    button = driver.find_element(by="css selector", value="#login-form > fieldset > div:nth-child(5) > a.ms-button.form-submit-btn")
    button.click()

    sleep(0.5)
    driver.get("https://nz.ua/school16699/schedule/diary")
    sleep(2)
    result = driver.page_source
    driver.quit()
    return result


def get_args():
    now_day = datetime.now().isoweekday()
    next_day = now_day + 1 if now_day in (1, 2, 3, 4) else 1
    lesson_count = 8 if now_day in (1, 2) else 7

    source = browser()
    soup = Bs4(source, "lxml")
    today_part = soup.find_all("div", class_="dn-item")[next_day-1]
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
        return hom.text.strip().split("Д/з: ")[1]
    except IndexError:
        return None


def make_string():
    string = ""
    for i in get_args():
        if i[1] is not None and i[0] is not None:
            string += f"<b>{i[0]}</b>: {i[1]}\n\n"
    return string
