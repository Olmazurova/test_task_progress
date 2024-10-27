import math
import time
import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db  # ссылка на БД
        self.__cur = db.cursor()  # через экземпляр класса курсор мы работаем с БД

    def get_menu(self):
        sql = '''SELECT * FROM mainmenu'''  # выборка всех записей из таблицы меню
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def add_achieve(self, title, points, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO achievements VALUES (NULL, ?, ?, ?, ?)',
                               (title, text, points, tm))  # заполнение таблицы, запрос + данные из кортежа
            self.__db.commit()  # сохранение записи в БД
        except sqlite3.Error as e:
            print("Ошибка добавления достижения в БД " + str(e))
            return False

        return True

    def get_achieve(self, achievId):
        try:
            self.__cur.execute(f'SELECT title, text, points FROM achievements WHERE id = {achievId} LIMIT 1')
            res = self.__cur.fetchone() # метод взять одну запись
            if res:
                return res

        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))

        return (False, False)

    def get_achiev_anonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, points FROM achievements ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return []
