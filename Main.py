import telebot
import Const
import sqlite3

bot = telebot.TeleBot(Const.token)


@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.language_code == "ru-RU":
        bot.send_message(message.chat.id, Const.ru_text[0])
    else:
        bot.send_message(message.chat.id, Const.en_text[0])


@bot.message_handler(content_types=["text"])
def handle_text(message):
    """
    if message.from_user.language_code == "ru-RU":
        lang = Const.ru_text
    else:
        lang = Const.en_text
    """
    conn = sqlite3.connect('commands.db')
    c = conn.cursor()
    c.execute('SELECT * FROM commands WHERE command="' + message.text.lower() + '" OR name="' + message.text.lower() +
              '" OR command="'+message.text.upper()+'"')
    c = c.fetchall()

    if len(c) > 1:
        bot.send_message(message.chat.id, 'По вашему запросу найдено несколько команд ('+str(len(c))+'):')
    for row in c:
            if not(str(row[0]).find(" + ") == -1):
                command = "<b>Комбинация клавиш " + str(row[0])
            elif str(row[0]).isupper():
                command = "<b>Клавиша " + str(row[0]) + " (комбинация клавиш Shift + "+str(row[0]).lower()+")"
            else:
                command = "<b>Клавиша " + str(row[0])

            command = command + "\nНазвание: </b>" + str(row[1]) + "\n<b>Выполняемое действие: </b>" + str(row[2])
            if not((str(row[3]) == '') or (str(row[3]) == 'None')):
                command = command + "\n<b>Дополнительное описание: </b>" + str(row[3])
            bot.send_message(message.chat.id, command, parse_mode='HTML')
    if len(c) == 0:
        bot.send_message(message.chat.id, 'Такая команда отсутствует в БД :(')

bot.polling(none_stop=True, interval=0)
