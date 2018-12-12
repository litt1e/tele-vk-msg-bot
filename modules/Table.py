import sqlite3
from bot.modules import create_db

create_db.check()


class Table:
    def __init__(self):
        self.con = sqlite3.connect('users.db')
        self.cur = self.con.cursor()

    def check(self):
        """проверяет наличие пользователя в базе"""
        res = self.cur.execute("SELECT * FROM users").fetchall()
        return True if res else False

    def check_status(self, user_id):
        """проверяет статус пользователя"""
        res = self.cur.execute("SELECT status FROM users WHERE user_id = %s" % user_id).fetchall()
        return True if res[0] else False

    def add_user(self, user_id, user):
        """добавляет нового пользователя в базу"""
        self.cur.execute("INSERT INTO users (user_id, status, token)"
                         "VALUES %d, %d, %s" % (user_id, user.status, user.token))
        self.con.commit()

    def get_status(self, user_id):
        """возвращает текущий статус пользователя"""
        res = self.cur.execute("SELECT status FROM users WHERE user_id = %d" % user_id).fetchall()
        return res[0]

    def get_token(self, user_id):
        """возвращает токен из базы"""
        token = self.cur.execute("SELECT token FROM users WHERE user_id = %d" % user_id).fetchall()
        return token[0] if self.check_status(user_id) == 1 else False

    def userisback(self, user_id):
        self.cur.execute("UPDATE users"
                         "SET status = 1"
                         "WHERE user_id = %d" % user_id)

    def out(self, user_id):
        """выход"""
        self.cur.execute("UPDATE users"
                         "SET status = 0"
                         "WHERE user_id = %d" % user_id)
        self.con.commit()
