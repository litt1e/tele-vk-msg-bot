import sqlite3
import os


def check():
    path = os.getcwd()
    if 'users.db' not in os.listdir(path):
        con = sqlite3.connect('users.db')
        cur = con.cursor()

        cur.execute("CREATE TABLE users ( "
                    "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                    "user_id INTEGER NOT NULL,"
                    "status INTEGER NOT NULL, "
                    "token TEXT NOT NULL)")
        con.commit()


if __name__ == '__main__':
    check()
