import fdb as fdb
import os

db_path = os.getenv('DB_PATH')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_charset = os.getenv('DB_CHARSET')

class DBConnector():
    def __init__(self):
        try:
            self.dataset = fdb.connect(
                dsn=db_path,
                user=db_user,
                password=db_password,
                charset=db_charset)
            self.cursor = self.dataset.cursor()
            print("Успешное подключение!")
        except fdb.Error as e:
            print(f("Ошибка: {e}"))
    def close(self):
        if self.connection:
            self.connection.close()
_db_connector = None
def get_db_connection():
    global _db_connector
    if _db_connector is None:
        _db_connector = DBConnector()
    return _db_connector


class BaseDBView():
    def __init__(self):
        self.connector = get_db_connection()