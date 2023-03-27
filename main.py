import telebot
import config
from telebot import types
from random import randint
import lesson
import nz_parser as nz
import time


bot = telebot.TeleBot(config.TOKEN)
first_time = True
last_callback = {}
cooldown_time = 600


@bot.message_handler(commands=["start"])
def welcome(message):
    sti_hi = open("add/hi.webp", "rb")
    bot.send_sticker(message.chat.id, sti_hi)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    key1 = types.KeyboardButton("🎲Рандом від 1 до 100")
    key2 = types.KeyboardButton("😏ГДЗ")
    key3 = types.KeyboardButton("📄Розклад")
    key4 = types.KeyboardButton("⏰До кінця уроку")
    key5 = types.KeyboardButton("⏳Уроки на завтра (2 група)")
    key6 = types.KeyboardButton("❗Оновити бота")
    markup.add(key1, key2, key3, key4, key5, key6)
    bot.send_message(message.chat.id, "Привіт {0.first_name}!\nЯ <b>{1.first_name}</b> бот який буде тобі допомагати, "
                                      "бот буде дороблятися із часом. \nGithub: Flipper212".format(
                                        message.from_user, bot.get_me()), parse_mode="html", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def user_write(message):
    if message.chat.type == "private":
        if message.text == "📄Розклад":
            with open("add/lessons.webp", "rb") as sti:
                bot.send_photo(message.chat.id, sti)
        elif message.text == "⏰До кінця уроку":
            bot.send_message(message.chat.id, lesson.make_result(), parse_mode="html")
            # result_str, week[count_day][index], is_start, is_end, is_last
        elif message.text == "⏳Уроки на завтра (2 група)":
            if last_callback.get(message.from_user.id) is None or time.time() - last_callback[message.from_user.id] > cooldown_time:
                last_callback[message.from_user.id] = time.time()
                bot.send_message(message.chat.id, "Виконую...")
                try:
                    bot.send_message(message.chat.id, nz.make_string(), parse_mode="html")
                except telebot.apihelper.ApiTelegramException:
                    bot.send_message(message.chat.id, "Немає домашнього завдання🤩")
                except Exception:
                    bot.send_message(message.chat.id, "Щось пішло не так")
            else:
                bot.send_message(message.chat.id, "Раз на 10 хв😴")
        elif message.text == "❗Оновити бота":
            welcome(message)
        elif message.text == "🎲Рандом від 1 до 100":
            bot.send_message(message.chat.id, str(randint(1, 100)))
        elif message.text == "😏ГДЗ":
            markup = types.InlineKeyboardMarkup(row_width=2)
            key1 = types.InlineKeyboardButton("Алгебра", url = "https://vshkole.com/9-klass/reshebniki/algebra/ag-merzlyak-vb-polonskij-ms-yakir-2017-pogliblene-vivchennya")
            key2 = types.InlineKeyboardButton("Геометрія", url = "https://vshkole.com/9-klass/reshebniki/geometriya/ag-merzlyak-vb-polonskij-ms-yakir-2017-pogliblene-vivchennya")
            key3 = types.InlineKeyboardButton("Хімія", url = "https://vshkole.com/9-klass/reshebniki/himiya/ov-grigorovich-2017")
            key4 = types.InlineKeyboardButton("Біологія", url = "http://8next.com/9b_obp_u2017.html")
            key5 = types.InlineKeyboardButton("Укр мова", url = "https://4book.org/gdz-reshebniki-ukraina/9-klas/gdz-vidpovidi-ukrayinska-mova-9-klas-zabolotniy-2017")
            key6 = types.InlineKeyboardButton("географія(практикум)", url = "https://gdzonline.net/753-pugach-9-klas.html")
            markup.add(key1, key2, key3, key4, key5, key6)

            bot.send_message(message.chat.id, "🙈Вибирай:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "😓я не розпізнав команду")


bot.polling(none_stop=True)
