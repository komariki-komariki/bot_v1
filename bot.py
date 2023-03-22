import telebot
from telebot import types
from entrepreneur import zakl_ip
from tokens import telegram
from yl import zakl
from ofdata_api import Count



TOKEN = telegram
bot = telebot.TeleBot(TOKEN)
users = [1787812736, 5042194140, 1194496297, 976949796, 1078681916]
users_dict = {'1787812736': ['Илья Сергеевич', 'komaroff.ilya.s@gmail.com'],
              '5042194140': ['Константин Борисович', 'kostik201428@gmail.com'],
              '1194496297': ['Вадим Юрьевич', 'zayats-vadim@mail.ru'],
              '976949796': ['Алексей Васильевич', 'alexsej.kondrin@gmail.com'],
              '1078681916': ['Андрей Сергеевич', 'asbaturin@mail.ru'],


}

class Task():
    isRunning = False
    names = ['контрагент', 'работодатель', 'счет', 'эквайринг']
    forms = ''
    inns = ''
    adress = ''
    def __init__(self):
        return

@bot.message_handler(func=lambda message: message.chat.id not in users)
def some(message):
    user_id = message.from_user.id
    print(user_id)
    bot.send_message(message.chat.id, 'У вас нет доступа')

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    if not Task.isRunning:
        chat_id = message.chat.id
        names = users_dict[str(message.from_user.id)][0]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Эквайринг")
        btn2 = types.KeyboardButton("Контрагент")
        btn3 = types.KeyboardButton("Счет")
        btn4 = types.KeyboardButton("Работодатель")
        markup.add(btn1, btn2, btn3, btn4)
        msg = bot.send_message(chat_id, f'Чего желаете, {names}?', reply_markup=markup)
        emails = users_dict[str(message.from_user.id)][1]
        print(emails, names)
        bot.register_next_step_handler(msg, ask_form)
        Task.isRunning = True

def ask_form(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if text in Task.names:
        Task.forms = text
        msg = bot.send_message(chat_id, 'Какой ИНН?')
        bot.register_next_step_handler(msg, ask_inn)
    else:
        msg = bot.send_message(chat_id, 'Такое не умею')
        bot.register_next_step_handler(msg, ask_form)
        return

def ask_inn(message):
    emails = users_dict[str(message.from_user.id)][1]
    names = users_dict[str(message.from_user.id)][0]
    chat_id = message.chat.id
    text = message.text.lower()
    if len(text) == 10:
        Task.inns = text
        if Task.forms == 'работодатель':
            Task.forms = 'employer'
        if Task.forms == 'контрагент':
            Task.forms = 'counter'
        if Task.forms == 'эквайринг':
            Task.forms = 'ekv'
        if Task.forms == 'счет':
            Task.forms = 'score'
        send_txt = zakl(Task.inns, Task.forms, emails)
        if send_txt == 'Успешно':
            bot.send_message(chat_id, f'{names}, все готово, письмо отправлено на {emails}')
            bot.send_message(chat_id, Count.ost)
        else:
            bot.send_message(chat_id, send_txt)
        Task.isRunning = False
    elif len(text) == 12:
        Task.inns = text
        if Task.forms == 'работодатель':
            Task.forms = 'employer'
        if Task.forms == 'контрагент':
            Task.forms = 'counter'
        if Task.forms == 'эквайринг':
            Task.forms = 'ekv'
        if Task.forms == 'счет':
            Task.forms = 'score'
        send_txt = zakl_ip(Task.inns, Task.forms, emails)
        if send_txt == 'Успешно':
            bot.send_message(chat_id, f'{names}, все готово, письмо отправлено на {emails}')
            bot.send_message(chat_id, Count.ost)
        else:
            bot.send_message(chat_id, send_txt)
        Task.isRunning = False
    else:
        msg = bot.send_message(chat_id, 'Введи корректный ИНН')
        bot.register_next_step_handler(msg, ask_inn)
        return

if __name__ == '__main__':
    bot.polling(none_stop=True)