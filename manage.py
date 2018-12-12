import telebot
from bot.modules import User, config
from telebot import types

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def activate(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Вход", callback_data="enter")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, 'Вход', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "Вход":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message_id,
                                  text="Для входа введите\n/auth login password")


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    user_id = call.message.chat.id
    user = User.User()
    user.auth_via_token(user_id)
    if call.message:
        if call.data == "dialogs":
            messages = user.get_dialogs(bot)
            for dialog in messages:
                info_about_dialog = 'id: ' + dialog['id'] + ' name: ' + dialog['name'] + '\nmessage: ' + dialog['last']
                bot.send_message(user.user_id, info_about_dialog)
        elif call.data == 'exit':
            user.out()
            bot.send_message(call.message.chat.id, "Вы вышли из своего аккаунта")


@bot.message_handler(commands=['auth', 'exit'])
def manage(message=None):
    if message:
        if 'auth' in message.text:
            user = User.User()
            text = message.text.split(' ')
            try:
                user.login, user.password = text[1], text[2]
            except IndexError:
                bot.send_message(message.chat.id, 'Вводи пароль в команде'
                                                  '/auth login password')
            else:
                user.authorize(bot, user, message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
