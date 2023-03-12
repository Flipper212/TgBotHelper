import telebot
import config
from telebot import types
from random import randint
import lesson


bot = telebot.TeleBot(config.TOKEN)
print(111111, lesson.result)


@bot.message_handler(commands=["start"])
def welcome(message):
    sti_hi = open("add/hi.webp", "rb")
    bot.send_sticker(message.chat.id, sti_hi)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    key1 = types.KeyboardButton("🎲Рандом від 1 до 100")
    key2 = types.KeyboardButton("🥰Як справи")
    key3 = types.KeyboardButton("😏ГДЗ")
    key4 = types.KeyboardButton("📄Розклад")
    key5 = types.KeyboardButton("♦BETA:До кінця уроку")
    markup.add(key1, key2, key3, key4, key5)
    bot.send_message(message.chat.id, "Привіт {0.first_name}!\nЯ <b>{1.first_name}</b> бот який буде тобі допомагати,ей бот буде дороблятися із часом. \nGithub: Flipper212".format(
        message.from_user, bot.get_me()), parse_mode="html", reply_markup=markup)


@bot.message_handler(content_types = ["text"])
def user_write(message):
    if message.chat.type == "private":
        if message.text == "📄Розклад":
            with open("add/lessons.webp", "rb") as sti:
                bot.send_photo(message.chat.id, sti)
        elif message.text == "♦BETA:До кінця уроку":
            if lesson.main()[-1] is False:
                bot.send_message(message.chat.id, "<b>Сьогодні не має уроків</b>🥰", parse_mode="html")
            elif lesson.main()[0] > 40:
                bot.send_message(message.chat.id,
                                 f"<b>{lesson.main()[1]}</b> почнеться через <b>{40 - lesson.main()[0]}</b> хв ",
                                 parse_mode="html")
            elif lesson.main()[2]:
                bot.send_message(message.chat.id, f"Урок закінчиться через <b>{lesson.main()[0]}</b> хв, наступний <b>{lesson.main()[1]}</b>", parse_mode="html")
            elif lesson.main()[3]:
                bot.send_message(message.chat.id, "<b>Уроки закінчились</b>🥰", parse_mode="html")
        elif message.text == "🎲Рандом від 1 до 100":
            bot.send_message(message.chat.id, str(randint(1, 100)))
        elif message.text == "🥰Як справи":
            #InlineButton
            markup = types.InlineKeyboardMarkup(row_width=2)
            key1 = types.InlineKeyboardButton("Все добре", callback_data="good")
            key2 = types.InlineKeyboardButton("Не дуже", callback_data="bad")
            markup.add(key1, key2)

            bot.send_message(message.chat.id, "Чудово, ти як?", reply_markup=markup)
        elif message.text == "😏ГДЗ":
            markup = types.InlineKeyboardMarkup(row_width=2)
            key1 = types.InlineKeyboardButton("Алгебра", callback_data="alg", url="https://vshkole.com/9-klass/reshebniki/algebra/ag-merzlyak-vb-polonskij-ms-yakir-2017-pogliblene-vivchennya")
            key2 = types.InlineKeyboardButton("Геометрія", callback_data="geom", url="https://vshkole.com/9-klass/reshebniki/geometriya/ag-merzlyak-vb-polonskij-ms-yakir-2017-pogliblene-vivchennya")
            key3 = types.InlineKeyboardButton("Хімія", callback_data="xim", url="https://vshkole.com/9-klass/reshebniki/himiya/ov-grigorovich-2017")
            key4 = types.InlineKeyboardButton("Біологія", callback_data="bio", url="http://8next.com/9b_obp_u2017.html")
            key5 = types.InlineKeyboardButton("Укр мова", callback_data="ukr_lan", url="https://4book.org/gdz-reshebniki-ukraina/9-klas/gdz-vidpovidi-ukrayinska-mova-9-klas-zabolotniy-2017")
            key6 = types.InlineKeyboardButton("географія(практикум)", callback_data="geog", url="https://gdzonline.net/753-pugach-9-klas.html")
            markup.add(key1, key2, key3, key4, key5, key6)

            bot.send_message(message.chat.id, "🙈Вибирай:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "😓я не розпізнав команду")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == "good":
                bot.send_message(call.message.chat.id, "Це добре😋")
            elif call.data == "bad":
                bot.send_message(call.message.chat.id, "Це погано😔")

            #remove inline button
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🥰 Як справи", reply_markup=None)

            #show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Дякую за використання😊")
    except Exception as error:
        print(repr(error))

bot.polling(none_stop=True)