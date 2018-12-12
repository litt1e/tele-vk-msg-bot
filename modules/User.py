import vk_api
from bot.modules import Table
import json
from telebot import types


class User:
    def __init__(self):
        self.login = 'login'
        self.password = 'password'
        self.user_id = 0
        self.vk = vk_api.VkApi()
        self.status = 0
        self.table = Table.Table()
        self.token = 'token'

    def authorize(self, bot, user, message):
        self.user_id = message.chat.id
        session = vk_api.VkApi(self.login, self.password)
        try:
            session.auth()
        except vk_api.exceptions.Captcha:
            bot.send_message(message.chat.id, "Логин или пароль не верны")
        else:
            self.vk = session.get_api()
            self.status = 1
            with open('vk_config.v2.json', 'r') as file:
                data = json.loads(file.read())
                self.token = data[self.login]['token']['app6222115']['scope_140492255']['access_token']

            if not self.table.check():
                self.table.add_user(message.chat.id, user)
            else:
                self.table.userisback(self.user_id)
                bot.send_message(message.chat.id, "Снова здрасьте")

            keyboard = types.InlineKeyboardMarkup()
            first_btn = types.InlineKeyboardButton(text='Диалоги', callback_data='dialogs')
            second_btn = types.InlineKeyboardButton(text='Выход', callback_data='exit')
            keyboard.add(first_btn)
            keyboard.add(second_btn)
            bot.send_message(message.chat.id, text='Успешная авторизация!\nТеперь удалите это сообщение.\nМеню:',
                             reply_markup=keyboard)

    def auth_via_token(self, user_id):
        """авторизация по токену, находящемуся в бд"""
        self.token = self.table.get_token(user_id)
        self.user_id = user_id
        session = vk_api.VkApi(token=self.token)
        session._auth_token()
        self.vk = session.get_api()
        self.status = 1

    def out(self):
        """выход"""
        self.table.out(self.user_id)

    def get_dialogs(self, bot):
        if self.status == 0:
            bot.send_message(self.user_id, "Сначала надо авторизироваться!\n"
                                           "/auth login password")
        elif self.status == 1:
            bot.send_message(self.user_id, "Сообщения загружаются.\n"
                                           "Это может занять некоторое время.")
            data = self.vk.messages.getDialogs()
            dialogs = []
            for dialog in data:
                lastmsg = ""

                if not dialog["message"]["body"]:
                    try:
                        lastmsg = dialog["message"]["attachments"][0]["type"]
                    except KeyError:
                        if dialog["message"]["action"]:
                            lastmsg = dialog["message"]["action"]
                    else:
                        lastmsg = dialog["message"]["attachments"][0]["type"]
                else:
                    lastmsg = dialog["message"]["body"]

                if dialog["message"]["title"]:
                    id = dialog["message"]["chat_id"]
                    name = dialog["message"]["title"]
                    dialogs.append({'id':id, 'name':name, 'last':lastmsg})

                elif dialog["message"]["user_id"] < 0:
                    id = dialog['message']['user_id']
                    name = self.vk.groups.getById(group_id=id)[0]['name']
                    dialogs.append({'id': id, 'name': name, 'last': lastmsg})

                else:
                    id = dialog['message']['user_id']
                    name = self.vk.users.get(user_id=id)
                    name = name[0]['first_name'] + " " + name[0]['last_name']
                    dialogs.append({'id': id, 'name': name, 'last': lastmsg})

            return dialogs
